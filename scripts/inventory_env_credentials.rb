#!/usr/bin/env ruby
# frozen_string_literal: true

require "json"
require "open3"
require "optparse"
require "set"

options = {
  vault: ".env",
  json: false
}

OptionParser.new do |parser|
  parser.banner = "Usage: ruby scripts/inventory_env_credentials.rb [--vault NAME] [--json]"
  parser.on("--vault NAME", "1Password vault name to inspect, default: .env") do |value|
    options[:vault] = value
  end
  parser.on("--json", "Emit JSON instead of a text table") do
    options[:json] = true
  end
end.parse!

CANDIDATES = [
  {
    key: "bigquery",
    verdict: "replace-now",
    refs: ["GCP_SERVICE_ACCOUNT"],
    status_when_present: "testable"
  },
  {
    key: "cloudflare",
    verdict: "replace-now",
    refs: ["CLOUDFLARE_ACCOUNT_ID", "CLOUDFLARE_API_TOKEN", "CLOUDFLARE_USER_API_TOKEN"],
    status_when_present: "testable"
  },
  {
    key: "context7",
    verdict: "replace-now",
    refs: ["CONTEXT7_API_KEY"],
    status_when_present: "optional-auth"
  },
  {
    key: "github",
    verdict: "replace-now",
    refs: ["GITHUB_PERSONAL_ACCESS_TOKEN"],
    status_when_present: "testable"
  },
  {
    key: "google-workspace",
    verdict: "replace-now",
    refs: [],
    status_when_present: "uses-local-gws-auth"
  },
  {
    key: "guru",
    verdict: "replace-now",
    refs: [],
    status_when_present: "uses-local-guru-auth"
  },
  {
    key: "hex",
    verdict: "pilot-blocked",
    refs: ["HEX_API_TOKEN"],
    status_when_present: "testable"
  },
  {
    key: "intercom",
    verdict: "pilot",
    refs: ["INTERCOM_ACCESS_TOKEN", "INTERCOM_API_TOKEN"],
    status_when_present: "testable"
  },
  {
    key: "linear",
    verdict: "pilot",
    refs: ["LINEAR_API_KEY"],
    status_when_present: "testable"
  },
  {
    key: "namecheap",
    verdict: "wrapper-candidate",
    refs: ["NAMECHEAP_API_KEY", "NAMECHEAP_API_USER", "NAMECHEAP_USERNAME"],
    status_when_present: "testable"
  },
  {
    key: "notion",
    verdict: "pilot-keep-mcp",
    refs: ["NOTION_API_KEY"],
    status_when_present: "testable"
  },
  {
    key: "servicenow",
    verdict: "pilot-blocked",
    refs: ["SERVICENOW_INSTANCE_URL", "SERVICENOW_TOKEN", "SERVICENOW_USERNAME", "SERVICENOW_PASSWORD"],
    status_when_present: "testable"
  },
  {
    key: "slack",
    verdict: "wrapper-candidate",
    refs: ["SLACK_MCP_XOXP_TOKEN"],
    status_when_present: "mcp-token-present"
  },
  {
    key: "workato",
    verdict: "public-plugin",
    refs: ["WORKATO_API_TOKEN"],
    status_when_present: "testable"
  }
].freeze

def op_available?
  ENV.fetch("PATH", "").split(File::PATH_SEPARATOR).any? do |directory|
    path = File.join(directory, "op")
    File.file?(path) && File.executable?(path)
  end
end

abort "1Password CLI `op` is not on PATH" unless op_available?

stdout, stderr, status = Open3.capture3("op", "item", "list", "--vault", options.fetch(:vault), "--format", "json")
abort "op item list failed: #{stderr.strip}" unless status.success?

items = JSON.parse(stdout)
titles = items.map { |item| item.fetch("title") }.to_set

results = CANDIDATES.map do |candidate|
  refs = candidate.fetch(:refs)
  present = refs.select { |ref| titles.include?(ref) }
  missing = refs - present
  status =
    if refs.empty?
      candidate.fetch(:status_when_present)
    elsif missing.empty?
      candidate.fetch(:status_when_present)
    elsif present.any?
      "partial"
    else
      "blocked-missing-credential"
    end

  {
    key: candidate.fetch(:key),
    verdict: candidate.fetch(:verdict),
    status: status,
    present_refs: present,
    missing_refs: missing
  }
end

if options[:json]
  puts JSON.pretty_generate(results)
else
  puts "Credential availability inventory for vault #{options.fetch(:vault).inspect}"
  puts
  results.each do |result|
    puts "#{result.fetch(:status).ljust(28)} #{result.fetch(:key).ljust(18)} #{result.fetch(:verdict)}"
    refs = result.fetch(:present_refs)
    puts "    present: #{refs.join(", ")}" if refs.any?
    missing = result.fetch(:missing_refs)
    puts "    missing: #{missing.join(", ")}" if missing.any?
  end
  puts
  puts "This script prints item names only. It never reads or prints secret values."
end
