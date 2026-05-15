#!/usr/bin/env ruby
# frozen_string_literal: true

require "json"
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
    notes: "Use bq for BigQuery query/list/show/load/extract workflows."
  },
  {
    key: "hex",
    command: "hex",
    owner: "Hex CLI",
    required: false,
    notes: "Pilot hex for Hex projects, apps, cells, runs, users, groups, and connections before removing MCP."
  },
  {
    key: "notion",
    command: "ntn",
    owner: "Notion CLI",
    required: false,
    notes: "Pilot ntn for Notion pages, data sources, Markdown, and API JSON workflows before removing MCP."
  },
  {
    key: "guru",
    command: "guru",
    owner: "@getguru/cli",
    required: true,
    runners: ["pnpm", "npx"],
    notes: "Use guru for Guru search and card workflows; prefer one-off pnpm/npx before global install."
  },
  {
    key: "servicenow",
    command: "snc",
    owner: "ServiceNow CLI",
    required: false,
    notes: "Pilot snc for generic ServiceNow table/record ITSM workflows before removing MCP."
  },
  {
    key: "context7",
    command: "ctx7",
    owner: "Context7 CLI",
    required: true,
    runners: ["pnpm", "npx"],
    notes: "Use ctx7 for library resolution and docs lookup; pnpm dlx or npx is acceptable."
  },
  {
    key: "cloudflare-cf",
    command: "cf",
    owner: "Cloudflare cf CLI",
    required: true,
    runners: ["pnpm", "npx"],
    notes: "Use cf for Cloudflare zones, DNS, Registrar, Accounts, and generated API-backed commands."
  },
  {
    key: "cloudflare-wrangler",
    command: "wrangler",
    owner: "Cloudflare Wrangler",
    required: true,
    runners: ["pnpm", "npx"],
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

results = INTEGRATIONS.map do |integration|
  path = executable_path(integration.fetch(:command))
  runners = runner_paths(integration[:runners])
  status =
    if path
      "installed"
    elsif runners.any?
      "runner-available"
    else
      "missing"
    end

  integration.merge(
    path: path,
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
        "can use #{result[:available_runners].map { |runner| runner[:runner] }.join('/')}"
      else
        "not found on PATH"
      end

    required = result[:required] ? "required" : "optional"
    puts "#{marker.ljust(7)} #{command.ljust(10)} #{required.ljust(8)} #{result[:owner]}"
    puts "        #{install_state}"
    puts "        #{result[:notes]}"
  end

  puts
  puts "This script does not install CLIs. Use --strict to fail when required commands or runners are missing."
end

strict_failures = results.select { |result| result[:required] && result[:status] == "missing" }
exit 1 if options[:strict] && strict_failures.any?
