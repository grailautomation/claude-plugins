#!/usr/bin/env ruby
# frozen_string_literal: true

require "json"
require "open3"
require "optparse"
require "tempfile"
require "timeout"

options = {
  json: false,
  only: nil,
  strict: false,
  timeout: 120
}

OptionParser.new do |parser|
  parser.banner = "Usage: ruby scripts/smoke_cli_integrations.rb [--only key[,key]] [--strict] [--json]"
  parser.on("--only LIST", "Run only comma-separated smoke checks") do |value|
    options[:only] = value.split(",").map(&:strip).reject(&:empty?)
  end
  parser.on("--strict", "Exit non-zero for warnings as well as failures") do
    options[:strict] = true
  end
  parser.on("--json", "Emit JSON instead of a text table") do
    options[:json] = true
  end
  parser.on("--timeout SECONDS", Integer, "Per-command timeout in seconds") do |value|
    options[:timeout] = value
  end
end.parse!

Result = Struct.new(:key, :status, :detail, keyword_init: true)

def executable_path(command)
  ENV.fetch("PATH", "").split(File::PATH_SEPARATOR).each do |directory|
    path = File.join(directory, command)
    return path if File.file?(path) && File.executable?(path)
  end

  nil
end

def command_prefix(command, package: nil)
  path = executable_path(command)
  return [path] if path

  return nil unless package

  if (pnpm = executable_path("pnpm"))
    [pnpm, "dlx", package]
  elsif (npx = executable_path("npx"))
    [npx, "-y", package]
  end
end

def run_command(argv, env: {}, timeout:)
  stdout = nil
  stderr = nil
  status = nil
  Timeout.timeout(timeout) do
    stdout, stderr, status = Open3.capture3(env, *argv)
  end
  { ok: status.success?, exit_status: status.exitstatus, stdout: stdout, stderr: stderr }
rescue Timeout::Error
  { ok: false, exit_status: nil, stdout: "", stderr: "timed out after #{timeout}s" }
rescue SystemCallError => e
  { ok: false, exit_status: nil, stdout: "", stderr: e.message }
end

def failure_detail(result)
  output = [result[:stderr], result[:stdout]].join("\n").strip
  output.empty? ? "exit #{result[:exit_status] || "unknown"}" : output.lines.first(4).join.strip
end

def redact_email(value)
  value.to_s
       .gsub(/user:[A-Za-z0-9._%+-]+@/, "user:<redacted>@")
       .gsub(/serviceAccount:[A-Za-z0-9._%+-]+@/, "serviceAccount:<redacted>@")
       .gsub(/[A-Za-z0-9._%+-]+@/, "<redacted>@")
end

def pass(key, detail)
  Result.new(key: key, status: "pass", detail: detail)
end

def warn(key, detail)
  Result.new(key: key, status: "warn", detail: detail)
end

def fail_result(key, detail)
  Result.new(key: key, status: "fail", detail: detail)
end

def smoke_bigquery(timeout)
  key = "bigquery"
  op_ref = ENV["GCP_SERVICE_ACCOUNT_OP_REF"]
  return fail_result(key, "set GCP_SERVICE_ACCOUNT_OP_REF=op://<vault>/<item>/<field>") if op_ref.to_s.empty?
  return fail_result(key, "1Password CLI `op` is not on PATH") unless executable_path("op")
  return fail_result(key, "BigQuery CLI `bq` is not on PATH") unless executable_path("bq")

  secret = run_command(["op", "read", op_ref], timeout: timeout)
  return fail_result(key, "could not read service-account JSON from 1Password: #{failure_detail(secret)}") unless secret[:ok]

  begin
    credential = JSON.parse(secret.fetch(:stdout))
  rescue JSON::ParserError => e
    return fail_result(key, "1Password value is not valid JSON: #{e.message}")
  end

  return fail_result(key, "credential type is #{credential["type"].inspect}, expected service_account") unless credential["type"] == "service_account"
  return fail_result(key, "credential is missing client_email") if credential["client_email"].to_s.empty?

  Tempfile.create(["gcp-service-account", ".json"]) do |file|
    file.write(secret.fetch(:stdout))
    file.flush
    File.chmod(0o600, file.path)
    env = { "CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE" => file.path }
    result = run_command(
      ["bq", "query", "--dry_run", "--use_legacy_sql=false", "--format=json", "SELECT 1 AS ok"],
      env: env,
      timeout: timeout
    )
    return fail_result(key, "bq dry-run failed: #{failure_detail(result)}") unless result[:ok]

    begin
      payload = JSON.parse(result.fetch(:stdout))
    rescue JSON::ParserError => e
      return fail_result(key, "bq dry-run did not emit JSON: #{e.message}")
    end

    principal = payload["principal_subject"].to_s
    user_email = payload["user_email"].to_s
    service_account = credential.fetch("client_email")
    unless principal.include?(service_account) || user_email == service_account
      return fail_result(key, "bq did not run as the service-account principal: #{redact_email(principal.empty? ? user_email : principal)}")
    end

    bytes = payload.dig("statistics", "query", "totalBytesProcessed")
    pass(key, "dry-run ok as service account; bytes_processed=#{bytes}")
  end
end

def smoke_context7(timeout)
  key = "context7"
  prefix = command_prefix("ctx7", package: "ctx7")
  return fail_result(key, "ctx7 is unavailable and neither pnpm nor npx can run it") unless prefix

  result = run_command(
    [*prefix, "library", "react", "How to clean up useEffect with async operations", "--json"],
    timeout: timeout
  )
  return fail_result(key, "ctx7 library lookup failed: #{failure_detail(result)}") unless result[:ok]

  payload = JSON.parse(result.fetch(:stdout))
  return fail_result(key, "ctx7 returned an empty result set") unless payload.is_a?(Array) && payload.any?

  pass(key, "library lookup ok; first_id=#{payload.first["id"]}")
rescue JSON::ParserError => e
  fail_result(key, "ctx7 did not emit JSON: #{e.message}")
end

def smoke_guru(timeout)
  key = "guru"
  prefix = command_prefix("guru", package: "@getguru/cli")
  return fail_result(key, "guru is unavailable and neither pnpm nor npx can run @getguru/cli") unless prefix

  help = run_command([*prefix, "--help"], timeout: timeout)
  return fail_result(key, "guru help failed: #{failure_detail(help)}") unless help[:ok] && [help[:stdout], help[:stderr]].join.include?("Guru API")

  auth = run_command([*prefix, "auth", "status"], timeout: timeout)
  return pass(key, "help ok; auth status ok") if auth[:ok]

  warn(key, "help ok; auth status is not configured or failed")
end

def smoke_cf(timeout)
  key = "cloudflare-cf"
  prefix = command_prefix("cf", package: "cf")
  return fail_result(key, "cf is unavailable and neither pnpm nor npx can run it") unless prefix

  result = run_command([*prefix, "--version"], timeout: timeout)
  return fail_result(key, "cf --version failed: #{failure_detail(result)}") unless result[:ok]
  return fail_result(key, "cf --version did not verify as Cloudflare CLI") unless [result[:stdout], result[:stderr]].join.include?("Cloudflare CLI")

  pass(key, "version check ok")
end

def smoke_wrangler(timeout)
  key = "cloudflare-wrangler"
  prefix = command_prefix("wrangler", package: "wrangler")
  return fail_result(key, "wrangler is unavailable and neither pnpm nor npx can run it") unless prefix

  result = run_command([*prefix, "--version"], timeout: timeout)
  return fail_result(key, "wrangler --version failed: #{failure_detail(result)}") unless result[:ok]
  return fail_result(key, "wrangler --version did not emit a version") unless [result[:stdout], result[:stderr]].join.match?(/\d+\.\d+\.\d+/)

  pass(key, "version check ok")
end

SMOKES = {
  "bigquery" => method(:smoke_bigquery),
  "context7" => method(:smoke_context7),
  "guru" => method(:smoke_guru),
  "cloudflare-cf" => method(:smoke_cf),
  "cloudflare-wrangler" => method(:smoke_wrangler)
}.freeze

selected = options[:only] || SMOKES.keys
unknown = selected - SMOKES.keys
abort "Unknown smoke check(s): #{unknown.join(", ")}" if unknown.any?

results = selected.map { |key| SMOKES.fetch(key).call(options.fetch(:timeout)) }

if options[:json]
  puts JSON.pretty_generate(results.map(&:to_h))
else
  puts "CLI live smoke checks"
  puts
  results.each do |result|
    marker =
      case result.status
      when "pass" then "PASS"
      when "warn" then "WARN"
      else "FAIL"
      end
    puts "#{marker.ljust(5)} #{result.key.ljust(20)} #{result.detail}"
  end
end

failures = results.select { |result| result.status == "fail" }
warnings = results.select { |result| result.status == "warn" }
exit 1 if failures.any? || (options[:strict] && warnings.any?)
