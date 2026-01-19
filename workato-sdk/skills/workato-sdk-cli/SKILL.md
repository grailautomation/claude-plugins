---
name: Workato SDK CLI
description: This skill should be used when the user asks about "workato cli", "workato gem", "run connector locally", "rspec test", "write connector tests", "vcr cassettes", "connector_spec", "workato exec", "workato push", "workato generate", or needs to test and develop Workato connectors locally.
version: 0.1.0
---

# Workato SDK CLI - Local Development & Testing

Guide for using the Workato Connector SDK CLI gem to develop, test, and deploy custom connectors locally.

## Overview

The Workato SDK CLI (`workato-connector-sdk` gem) enables local connector development with:
- Local execution and testing of connector code
- RSpec integration for automated testing
- VCR cassette recording for API mocking
- Push/pull commands for Workato platform sync

## Installation

```bash
gem install workato-connector-sdk
```

Requirements: Ruby 2.7+, Bundler

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
workato push --title="My Connector" --api-token=YOUR_TOKEN
```

### Pull from Workato

```bash
workato pull --connector-id=12345 --api-token=YOUR_TOKEN
```

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
# Generate master key and encrypt settings
workato generate_key
workato encrypt settings.yaml
```

Creates `settings.yaml.enc` (safe to commit) and `master.key` (gitignore).

### Settings File Format

```yaml
# settings.yaml
api_key: your-api-key
subdomain: your-subdomain
environment: sandbox
```

### Environment Variables

```bash
export WORKATO_API_KEY=your-key
workato exec actions.test --settings-from-env
```

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
