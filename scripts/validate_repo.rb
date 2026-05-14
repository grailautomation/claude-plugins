#!/usr/bin/env ruby
# frozen_string_literal: true

require "json"
require "pathname"
require "set"
require "uri"
require "yaml"

ROOT = Pathname.new(File.expand_path("..", __dir__))

errors = []

error = lambda do |path, message|
  errors << [path, message]
end

repo_path = lambda do |relative_path|
  ROOT + relative_path
end

read_json = lambda do |relative_path|
  JSON.parse(repo_path.call(relative_path).read)
rescue JSON::ParserError => e
  error.call(relative_path, "invalid JSON: #{e.message}")
  nil
end

read_yaml = lambda do |relative_path, content|
  YAML.safe_load(content, aliases: true)
rescue Psych::Exception => e
  error.call(relative_path, "invalid YAML: #{e.message}")
  nil
end

extract_frontmatter = lambda do |relative_path|
  content = repo_path.call(relative_path).read
  lines = content.lines

  unless lines.first&.strip == "---"
    error.call(relative_path, "missing YAML frontmatter")
    return nil
  end

  body = []
  lines.drop(1).each do |line|
    return body.join if line.strip == "---"

    body << line
  end

  error.call(relative_path, "missing closing YAML frontmatter fence")
  nil
end

git_files_output = IO.popen(
  ["git", "-C", ROOT.to_s, "ls-files", "-co", "--exclude-standard"],
  &:read
)
files = git_files_output.lines.map(&:chomp).reject(&:empty?).sort

json_cache = {}
files.grep(/\.json\z/).each do |relative_path|
  json_cache[relative_path] = read_json.call(relative_path)
end

files.grep(/\.(ya?ml)\z/).each do |relative_path|
  read_yaml.call(relative_path, repo_path.call(relative_path).read)
end

codex_plugin_files = files.select { |path| path.include?("/.codex-plugin/") }
codex_plugin_files.each do |relative_path|
  next if relative_path.end_with?("/.codex-plugin/plugin.json")

  error.call(relative_path, "only plugin.json belongs under .codex-plugin/")
end

skill_files = files.select { |path| path.match?(%r{\A[^/]+/skills/[^/]+/SKILL\.md\z}) }
skill_files.each do |relative_path|
  frontmatter = extract_frontmatter.call(relative_path)
  next unless frontmatter

  metadata = read_yaml.call(relative_path, frontmatter)
  unless metadata.is_a?(Hash)
    error.call(relative_path, "frontmatter must be a mapping")
    next
  end

  skill_dir_name = relative_path.split("/")[-2]
  declared_name = metadata["name"]
  description = metadata["description"]

  if declared_name.to_s.strip.empty?
    error.call(relative_path, "frontmatter must include name")
  elsif declared_name != skill_dir_name
    error.call(relative_path, "frontmatter name must match skill directory '#{skill_dir_name}'")
  end

  error.call(relative_path, "frontmatter must include description") if description.to_s.strip.empty?
end

markdown_link = /!?\[[^\]]*\]\(([^)]+)\)/
files.grep(/\.md\z/).each do |relative_path|
  repo_path.call(relative_path).each_line.with_index(1) do |line, line_number|
    line.scan(markdown_link) do |match|
      raw_target = match.first.strip
      target =
        if raw_target.start_with?("<") && raw_target.include?(">")
          raw_target[1...raw_target.index(">")]
        else
          raw_target.split(/\s+/, 2).first
        end

      next if target.nil? || target.empty?
      next if target.start_with?("#")
      next if target.match?(%r{\A[a-zA-Z][a-zA-Z0-9+.-]*:})

      target_path = target.split("#", 2).first
      next if target_path.empty?
      next if target_path.start_with?("/")
      next unless target_path.match?(%r{(^|/|^\./|^\.\./)references/}) || target_path.end_with?(".md", ".markdown")

      decoded_target =
        begin
          URI.decode_www_form_component(target_path)
        rescue ArgumentError
          target_path
        end

      destination =
        if Pathname.new(decoded_target).absolute?
          Pathname.new(decoded_target)
        else
          repo_path.call(File.dirname(relative_path)) + decoded_target
        end

      next if destination.exist?

      error.call("#{relative_path}:#{line_number}", "broken relative markdown link: #{target}")
    end
  end
end

claude_marketplace_path = ".claude-plugin/marketplace.json"
codex_marketplace_path = ".agents/plugins/marketplace.json"

unless json_cache[claude_marketplace_path].is_a?(Hash)
  error.call(claude_marketplace_path, "Claude marketplace is missing or invalid")
end

unless json_cache[codex_marketplace_path].is_a?(Hash)
  error.call(codex_marketplace_path, "Codex marketplace is missing or invalid")
end

validate_unique_names = lambda do |entries, path|
  names = Set.new
  entries.each do |entry|
    name = entry["name"]
    if name.to_s.strip.empty?
      error.call(path, "marketplace entry is missing name")
    elsif names.include?(name)
      error.call(path, "duplicate marketplace entry: #{name}")
    else
      names.add(name)
    end
  end
end

if (marketplace = json_cache[claude_marketplace_path])
  entries = marketplace["plugins"]
  if entries.is_a?(Array)
    validate_unique_names.call(entries, claude_marketplace_path)

    entries.each do |entry|
      name = entry["name"]
      source = entry["source"]

      unless source.is_a?(String) && source.start_with?("./")
        error.call(claude_marketplace_path, "#{name || "<unnamed>"} source must start with ./")
        next
      end

      plugin_dir = source.delete_prefix("./")
      unless repo_path.call(plugin_dir).directory?
        error.call(claude_marketplace_path, "#{name} source directory does not exist: #{source}")
        next
      end

      manifest_path = "#{plugin_dir}/.claude-plugin/plugin.json"
      unless repo_path.call(manifest_path).file?
        error.call(claude_marketplace_path, "#{name} is missing #{manifest_path}")
        next
      end

      manifest = json_cache[manifest_path] || read_json.call(manifest_path)
      manifest_name = manifest&.fetch("name", nil)
      error.call(manifest_path, "manifest name must match marketplace name '#{name}'") if manifest_name && manifest_name != name
    end
  else
    error.call(claude_marketplace_path, "plugins must be an array")
  end
end

codex_listed_plugin_dirs = Set.new
if (marketplace = json_cache[codex_marketplace_path])
  entries = marketplace["plugins"]
  if entries.is_a?(Array)
    validate_unique_names.call(entries, codex_marketplace_path)

    entries.each do |entry|
      name = entry["name"]
      source = entry["source"]
      source_path = source.is_a?(Hash) ? source["path"] : nil

      unless source.is_a?(Hash) && source["source"] == "local"
        error.call(codex_marketplace_path, "#{name || "<unnamed>"} source must be local")
        next
      end

      unless source_path.is_a?(String) && source_path.start_with?("./")
        error.call(codex_marketplace_path, "#{name || "<unnamed>"} source.path must start with ./")
        next
      end

      plugin_dir = source_path.delete_prefix("./")
      codex_listed_plugin_dirs.add(plugin_dir)

      unless repo_path.call(plugin_dir).directory?
        error.call(codex_marketplace_path, "#{name} source directory does not exist: #{source_path}")
        next
      end

      manifest_path = "#{plugin_dir}/.codex-plugin/plugin.json"
      unless repo_path.call(manifest_path).file?
        error.call(codex_marketplace_path, "#{name} is missing #{manifest_path}")
        next
      end

      manifest = json_cache[manifest_path] || read_json.call(manifest_path)
      next unless manifest

      manifest_name = manifest["name"]
      error.call(manifest_path, "manifest name must match marketplace name '#{name}'") if manifest_name != name

      if repo_path.call("#{plugin_dir}/skills").directory? && manifest["skills"].to_s.strip.empty?
        error.call(manifest_path, "Codex manifest must expose skills when plugin has a skills directory")
      end

      manifest_text = JSON.generate(manifest)
      if manifest_text.match?(/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/)
        error.call(manifest_path, "Codex manifest must not contain personal email addresses")
      end
    end
  else
    error.call(codex_marketplace_path, "plugins must be an array")
  end
end

codex_manifests = files.select { |path| path.match?(%r{\A[^/]+/\.codex-plugin/plugin\.json\z}) }
codex_manifests.each do |manifest_path|
  plugin_dir = manifest_path.split("/", 2).first
  next if codex_listed_plugin_dirs.include?(plugin_dir)

  error.call(manifest_path, "Codex manifest exists but plugin is not listed in #{codex_marketplace_path}")
end

mcp_files = files.select { |path| path.end_with?("/.mcp.json") }
mcp_files.each do |relative_path|
  config = json_cache[relative_path]
  servers = config&.fetch("mcpServers", nil)
  unless servers.is_a?(Hash) && !servers.empty?
    error.call(relative_path, "mcpServers must be a non-empty object")
    next
  end

  servers.each do |server_name, server_config|
    unless server_config.is_a?(Hash)
      error.call(relative_path, "#{server_name} config must be an object")
      next
    end

    has_command = server_config["command"].is_a?(String)
    has_http = server_config["type"].is_a?(String) && server_config["url"].is_a?(String)

    unless has_command || has_http
      error.call(relative_path, "#{server_name} must declare either command or type/url")
    end

    args = server_config["args"]
    error.call(relative_path, "#{server_name} args must be an array when present") if args && !args.is_a?(Array)

    env = server_config["env"]
    error.call(relative_path, "#{server_name} env must be an object when present") if env && !env.is_a?(Hash)
  end
end

email_pattern = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/
files.grep(/\.(md|json)\z/).each do |relative_path|
  next if relative_path.end_with?("plugin.json")
  next if relative_path.end_with?("marketplace.json")
  next if ["AGENTS.md", "CLAUDE.md"].include?(relative_path)

  repo_path.call(relative_path).each_line.with_index(1) do |line, line_number|
    line.scan(email_pattern).each do |email|
      next if email.include?("@example")

      error.call("#{relative_path}:#{line_number}", "possible real email address: #{email}")
    end
  end
end

files.grep(/\.md\z/).each do |relative_path|
  repo_path.call(relative_path).each_line.with_index(1) do |line, line_number|
    line.scan(/00D[A-Za-z0-9]{15}/).each do |org_id|
      next if org_id.start_with?("00D000000000000")
      next if line.include?("data:image")

      error.call("#{relative_path}:#{line_number}", "possible Salesforce org ID: #{org_id}")
    end

    line.scan(%r{/Users/[a-z][A-Za-z0-9_-]*}).each do |user_path|
      error.call("#{relative_path}:#{line_number}", "hardcoded user path: #{user_path}")
    end
  end
end

if errors.empty?
  puts "OK: validated #{files.length} files, #{skill_files.length} skills, #{mcp_files.length} MCP configs"
else
  puts "Errors:"
  errors.each { |path, message| puts "  #{path}: #{message}" }
  exit 1
end
