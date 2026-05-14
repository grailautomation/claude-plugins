---
name: workato-connector-sdk-cli
description: >-
  Workato Connector SDK CLI reference (Ruby gem workato-connector-sdk). Use when the user
  asks about "workato gem", "workato-connector-sdk", "run connector locally", "rspec test",
  "write connector tests", "vcr cassettes", "connector_spec", "workato exec",
  "workato push", "workato new connector", "workato generate schema",
  or needs to develop, test, or debug Workato custom connectors locally with the Ruby CLI.
  NOT the Platform CLI (Python) for workspace management — use workato-platform-cli for that.
version: 0.1.0
---

# Workato SDK CLI - Local Development & Testing

Guide for using the Workato Connector SDK CLI gem to develop, test, and deploy custom connectors locally.

## Overview

> **Note:** This skill covers the Connector SDK CLI (Ruby gem `workato-connector-sdk`).
> For the Platform CLI (Python package `workato-platform-cli` for managing workspace
> recipes, connections, and projects), see the `workato-platform-cli` plugin.

The Workato SDK CLI (`workato-connector-sdk` gem) enables local connector development with:
- Local execution and testing of connector code
- RSpec integration for automated testing
- VCR cassette recording for API mocking
- Push commands for Workato platform sync

## Installation

```bash
gem install workato-connector-sdk
```

Workato's current SDK CLI getting-started docs list Ruby 2.7.x, 3.0.x, and 3.1.x as supported. Local installs may run on newer Ruby versions, but verify with the installed gem before assuming compatibility.

The Connector SDK gem and the Workato Platform CLI can both expose a `workato` command. Before running SDK CLI commands, check:

```bash
type -a workato
workato version
```

The Connector SDK gem uses `workato version`, not `workato --version`. If `workato --version` succeeds but `workato version` fails, you are probably invoking the Platform CLI, not the Ruby Connector SDK CLI.

## Project Structure

A standard connector project:

```
my-connector/
├── connector.rb          # Main connector code
├── settings.yaml         # Connection credentials (gitignored)
├── settings.yaml.enc     # Encrypted credentials
├── master.key            # Encryption key (gitignored)
├── Gemfile
└── spec/
    ├── connector_spec.rb
    └── cassettes/        # VCR recordings
```

## Essential Commands

### Generate New Connector

```bash
workato new my_connector
```

Creates project scaffold with connector.rb, Gemfile, and spec structure.

### Execute Actions/Triggers

```bash
# Execute an action
workato exec actions.search_records --input='{"query": "test"}'

# Execute a trigger
workato exec triggers.new_record --input='{"since": "2024-01-01"}'

# With settings file
workato exec actions.create_record --settings=settings.yaml --input='{"name": "Test"}'
```

### Test Connection

```bash
workato exec connection.authorization --settings=settings.yaml
```

### Push to Workato

```bash
WORKATO_API_TOKEN="<API_TOKEN>" workato push --title="My Connector"
```

`workato push` reads `WORKATO_API_TOKEN` and `WORKATO_BASE_URL` from the environment unless `--api-token` or `--environment` is provided explicitly. The Connector SDK gem does not provide a `workato pull` command; use Workato's UI or API workflows when you need to retrieve existing connector source.

## RSpec Testing

### Basic Test Structure

```ruby
RSpec.describe 'connector', :vcr do
  let(:connector) { Workato::Connector::Sdk::Connector.from_file('connector.rb') }
  let(:settings) { Workato::Connector::Sdk::Settings.from_file('settings.yaml') }

  describe 'connection' do
    it 'tests successfully' do
      result = connector.connection.authorization(settings)
      expect(result).to be_truthy
    end
  end

  describe 'actions' do
    describe 'search_records' do
      it 'returns results' do
        input = { query: 'test' }
        result = connector.actions.search_records.execute(settings, input)
        expect(result[:records]).to be_an(Array)
      end
    end
  end
end
```

### Running Tests

```bash
# Run all tests
bundle exec rspec

# Run specific test
bundle exec rspec spec/connector_spec.rb:25

# Run with VCR recording
VCR_RECORD=all bundle exec rspec
```

## VCR Cassette Recording

VCR records HTTP interactions for deterministic testing:

### Configuration

```ruby
# spec/spec_helper.rb
require 'vcr'

VCR.configure do |config|
  config.cassette_library_dir = 'spec/cassettes'
  config.hook_into :webmock
  config.filter_sensitive_data('<API_KEY>') { ENV['API_KEY'] }
end
```

### Recording Modes

| Mode | Behavior |
|------|----------|
| `none` | Only replay, fail if no cassette |
| `once` | Record once, then replay |
| `new_episodes` | Record new requests, replay existing |
| `all` | Always record fresh |

### Usage

```ruby
it 'fetches records', :vcr do
  # First run: records API call
  # Subsequent runs: replays from cassette
  result = connector.actions.get_records.execute(settings, {})
  expect(result).to include(:records)
end
```

## Settings Management

### Encrypted Settings

```bash
# Create or edit encrypted settings
workato edit settings.yaml.enc
```

Keep plaintext `settings.yaml`, `master.key`, and any files containing credentials gitignored. `WORKATO_CONNECTOR_MASTER_KEY` takes precedence over a key file when decrypting settings.

### Settings File Format

```yaml
# settings.yaml
api_key: your-api-key
subdomain: your-subdomain
environment: sandbox
```

### Environment Variables

Use environment variables for SDK CLI authentication to Workato itself, such as `WORKATO_API_TOKEN`, `WORKATO_BASE_URL`, and `WORKATO_CONNECTOR_MASTER_KEY`. Connector runtime credentials should still be passed through a plain or encrypted settings file with `--settings`.

## Debugging

### Verbose Output

```bash
workato exec actions.search --verbose
```

### Debug in Tests

```ruby
it 'debugs action' do
  result = connector.actions.my_action.execute(settings, input)
  pp result  # Pretty print result
  binding.pry  # Drop into debugger
end
```

### Common Issues

**Connection fails locally but works in Workato:**
- Check settings.yaml matches connection fields exactly
- Verify environment-specific URLs/credentials

**VCR cassette mismatch:**
- Delete cassette and re-record: `rm spec/cassettes/my_test.yml`
- Check for dynamic data in requests (timestamps, UUIDs)

**Action returns nil:**
- Ensure `execute` block returns a hash
- Check for missing `after_response` in HTTP calls

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Test Connector
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.1'
          bundler-cache: true
      - run: bundle exec rspec
```

### Secrets Management

Store `master.key` as GitHub secret, create during CI:

```yaml
- name: Setup credentials
  run: echo "${{ secrets.MASTER_KEY }}" > master.key
```

## Reference Files

For detailed documentation, consult the reference files:

### CLI Guides
- **`references/cli.md`** - CLI overview and installation
- **`references/cli__guides__getting-started.md`** - Getting started guide
- **`references/cli__guides__cli__actions.md`** - Testing actions locally
- **`references/cli__guides__cli__triggers.md`** - Testing triggers locally
- **`references/cli__guides__cli__methods.md`** - Testing methods
- **`references/cli__guides__cli__pick_lists.md`** - Testing pick lists
- **`references/cli__guides__cli__test.md`** - Test command reference
- **`references/cli__guides__cli__multistep-actions.md`** - Multistep action testing
- **`references/cli__guides__cli__download-streaming-actions.md`** - Download streaming
- **`references/cli__guides__cli__upload-streaming-actions.md`** - Upload streaming

### RSpec Testing
- **`references/cli__guides__rspec__writing_tests.md`** - Writing RSpec tests
- **`references/cli__guides__rspec__connector_spec.md`** - Connector spec patterns
- **`references/cli__guides__rspec__vcr.md`** - VCR cassette configuration
- **`references/cli__guides__rspec__file_streaming.md`** - File streaming tests
- **`references/cli__guides__rspec__enable-ci-cd-on-github.md`** - CI/CD setup

### Reference
- **`references/cli__reference__cli-commands.md`** - Complete CLI command reference
- **`references/cli__reference__cli-project-directory-reference.md`** - Project structure
- **`references/cli__reference__rspec-commands.md`** - RSpec command reference

### Other
- **`references/cli__guides__security-guidelines.md`** - Security best practices
- **`references/cli__guides__troubleshooting.md`** - Troubleshooting guide
