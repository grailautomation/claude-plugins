#!/usr/bin/env ruby
# frozen_string_literal: true

require "json"
require "open3"
require "optparse"

options = {
  strict: false,
  json: false
}

OptionParser.new do |parser|
  parser.banner = "Usage: ruby scripts/check_cli_integrations.rb [--strict] [--json]"
  parser.on("--strict", "Exit non-zero when a required CLI has no direct command or runner") do
    options[:strict] = true
  end
  parser.on("--json", "Emit JSON instead of a text table") do
    options[:json] = true
  end
end.parse!

INTEGRATIONS = [
  {
    key: "bigquery",
    command: "bq",
    owner: "Google Cloud SDK",
    required: true,
    verify_args: ["version"],
    verify_output: "BigQuery CLI",
    notes: "Use bq for BigQuery query/list/show/load/extract workflows."
  },
  {
    key: "hex",
    command: "hex",
    owner: "Hex CLI",
    required: false,
    verify_args: ["--version"],
    verify_pattern: "\\Ahex \\d+\\.\\d+\\.\\d+",
    install_hint: "Install from brew install hex-inc/hex-cli/hex or https://hex.tech/install.sh; the npm package named hex is unrelated.",
    notes: "Pilot hex for workspace/project/cell/run/connection reads and controlled draft operations; keep MCP for Agent thread create/continue workflows."
  },
  {
    key: "notion",
    command: "ntn",
    owner: "Notion CLI",
    required: false,
    verify_args: ["--version"],
    verify_pattern: "\\Antn \\d+\\.\\d+\\.\\d+",
    install_hint: "Install from https://ntn.dev or npm install --global ntn; use ntn doctor for setup/auth health.",
    notes: "Pilot ntn for Notion page, data-source, file, and raw API workflows; keep MCP for Notion AI search and database-view workflows."
  },
  {
    key: "guru",
    command: "guru",
    owner: "@getguru/cli",
    required: true,
    runners: ["pnpm", "npx"],
    verify_args: ["--help"],
    verify_output: "Guru API",
    notes: "Use guru for Guru search and card workflows; prefer one-off pnpm/npx before global install."
  },
  {
    key: "google-workspace",
    command: "gws",
    owner: "Google Workspace CLI",
    required: true,
    verify_args: ["--version"],
    verify_pattern: "\\Agws 0\\.(2[2-9]|[3-9]\\d)\\.",
    notes: "Use gws v0.22.5 or newer for Gmail, Calendar, Drive, Docs, Sheets, Slides, Tasks, Pub/Sub, and Workspace workflows."
  },
  {
    key: "linear",
    command: "linear",
    owner: "@kyaukyuai/linear-cli",
    required: false,
    runners: ["pnpm", "npx"],
    verify_args: ["capabilities", "--json"],
    verify_outputs: ["\"schemaVersion\"", "\"automationTier\"", "\"linear-cli\""],
    install_hint: "Prefer pnpm dlx @kyaukyuai/linear-cli for pilots; do not treat the older @linear/cli or upstream @schpet/linear-cli as equivalent.",
    notes: "Pilot issue/project/comment/document reads and dry-run writes; keep Linear MCP until low-risk apply receipts and workflow coverage are validated."
  },
  {
    key: "servicenow",
    command: "snc",
    owner: "ServiceNow CLI (snc)",
    required: false,
    verify_args: ["--help"],
    verify_outputs: ["ServiceNow", "record"],
    install_hint: "Install the ServiceNow snc client from ServiceNow Store or github.com/ServiceNow/servicenow-cli; npm snc is unrelated and @servicenow/cli exposes now-cli for app development only.",
    notes: "Pilot snc for generic ServiceNow record query/get/create/update/delete workflows; keep MCP for instance-specific MCP servers and Now Assist-style workflows."
  },
  {
    key: "context7",
    command: "ctx7",
    owner: "Context7 CLI",
    required: true,
    runners: ["pnpm", "npx"],
    verify_args: ["--version"],
    verify_pattern: "\\A\\d+\\.\\d+\\.\\d+",
    notes: "Use ctx7 for library resolution and docs lookup; pnpm dlx or npx is acceptable."
  },
  {
    key: "cloudflare-cf",
    command: "cf",
    owner: "Cloudflare cf CLI",
    required: true,
    runners: ["pnpm", "npx"],
    verify_args: ["--version"],
    verify_output: "Cloudflare CLI",
    notes: "Use cf for Cloudflare zones, DNS, Registrar, Accounts, and generated API-backed commands."
  },
  {
    key: "cloudflare-wrangler",
    command: "wrangler",
    owner: "Cloudflare Wrangler",
    required: true,
    runners: ["pnpm", "npx"],
    verify_args: ["--version"],
    verify_pattern: "\\A\\d+\\.\\d+\\.\\d+",
    notes: "Use wrangler for Workers, Pages, KV, R2, D1, Queues, and local development."
  }
].freeze

def executable_path(command)
  ENV.fetch("PATH", "").split(File::PATH_SEPARATOR).each do |directory|
    path = File.join(directory, command)
    return path if File.file?(path) && File.executable?(path)
  end

  nil
end

def runner_paths(runners)
  Array(runners).filter_map do |runner|
    path = executable_path(runner)
    { runner: runner, path: path } if path
  end
end

def verify_command(path, integration)
  verify_args = integration[:verify_args]
  verify_output = integration[:verify_output]
  verify_outputs = integration[:verify_outputs]
  verify_pattern = integration[:verify_pattern]
  return { ok: true, output: nil } unless verify_args && (verify_output || verify_outputs || verify_pattern)

  stdout, stderr, status = Open3.capture3(path, *verify_args)
  output = [stdout, stderr].join("\n")
  expected_strings = Array(verify_outputs || verify_output)
  strings_ok = expected_strings.empty? || expected_strings.all? { |expected| output.include?(expected) }
  pattern_ok = verify_pattern.nil? || output.match?(Regexp.new(verify_pattern))
  { ok: status.success? && strings_ok && pattern_ok, output: output.strip }
rescue SystemCallError
  { ok: false, output: nil }
end

results = INTEGRATIONS.map do |integration|
  path = executable_path(integration.fetch(:command))
  runners = runner_paths(integration[:runners])
  verification = path ? verify_command(path, integration) : { ok: false, output: nil }
  verified_path = path if path && verification[:ok]
  status =
    if verified_path
      "installed"
    elsif runners.any?
      "runner-available"
    else
      "missing"
    end

  integration.merge(
    path: verified_path,
    rejected_path: verified_path ? nil : path,
    verification_output: verification[:output],
    available_runners: runners,
    status: status
  )
end

if options[:json]
  puts JSON.pretty_generate(results)
else
  puts "CLI integration availability"
  puts
  results.each do |result|
    command = result.fetch(:command)
    marker =
      case result.fetch(:status)
      when "installed" then "OK"
      when "runner-available" then "RUNNER"
      else "MISSING"
      end

    install_state =
      if result[:path]
        result[:path]
      elsif result[:available_runners].any?
        state = "can use #{result[:available_runners].map { |runner| runner[:runner] }.join('/')}"
        if result[:rejected_path]
          state += "; ignored #{result[:rejected_path]} because it did not verify as #{result[:owner]}"
        end
        state
      else
        "not found on PATH"
      end

    required = result[:required] ? "required" : "optional"
    puts "#{marker.ljust(7)} #{command.ljust(10)} #{required.ljust(8)} #{result[:owner]}"
    puts "        #{install_state}"
    puts "        install: #{result[:install_hint]}" if result[:install_hint]
    puts "        #{result[:notes]}"
  end

  puts
  puts "This script does not install CLIs. Use --strict to fail when required commands or runners are missing."
end

strict_failures = results.select { |result| result[:required] && result[:status] == "missing" }
exit 1 if options[:strict] && strict_failures.any?
