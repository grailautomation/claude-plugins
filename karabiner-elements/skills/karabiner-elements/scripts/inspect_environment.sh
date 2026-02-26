#!/usr/bin/env bash
# Karabiner-Elements Environment Inspector
# Gathers information about the current Karabiner configuration
set -uo pipefail

CLI_PATH="/Library/Application Support/org.pqrs/Karabiner-Elements/bin/karabiner_cli"
CONFIG_PATH="$HOME/.config/karabiner/karabiner.json"
DEVICES_PATH="$HOME/.local/share/karabiner/karabiner_grabber_devices.json"

echo "=== Karabiner-Elements Environment Report ==="
echo ""

# Check installation
echo "## Installation Status"
if [ -d "/Applications/Karabiner-Elements.app" ]; then
    echo "✓ Karabiner-Elements.app is installed"
else
    echo "✗ Karabiner-Elements.app NOT found"
fi

if [ -f "$CLI_PATH" ]; then
    VERSION=$("$CLI_PATH" --version 2>/dev/null)
    echo "✓ CLI available - Version: $VERSION"
else
    echo "✗ CLI not available"
fi
echo ""

# Current profile
echo "## Active Profile"
if [ -f "$CLI_PATH" ]; then
    PROFILE=$("$CLI_PATH" --show-current-profile-name 2>/dev/null)
    echo "Current profile: $PROFILE"
fi
echo ""

# List all profiles
echo "## All Profiles"
if [ -f "$CLI_PATH" ]; then
    "$CLI_PATH" --list-profile-names 2>/dev/null
fi
echo ""

# Configuration summary
echo "## Configuration Summary"
if [ -f "$CONFIG_PATH" ]; then
    echo "Config file exists at: $CONFIG_PATH"
    echo "File size: $(ls -lh "$CONFIG_PATH" | awk '{print $5}')"
    echo "Last modified: $(stat -f '%Sm' "$CONFIG_PATH")"

    # Count rules in selected profile
    RULES_COUNT=$(python3 -c "
import json
with open('$CONFIG_PATH') as f:
    config = json.load(f)
profile = next((p for p in config['profiles'] if p.get('selected')), None)
if profile:
    rules = profile.get('complex_modifications', {}).get('rules', [])
    print(len(rules))
" 2>/dev/null)
    echo "Complex modification rules: ${RULES_COUNT:-0}"
else
    echo "✗ Config file not found"
fi
echo ""

# Connected devices
echo "## Connected Devices"
if [ -f "$DEVICES_PATH" ]; then
    python3 -c "
import json
with open('$DEVICES_PATH') as f:
    data = json.load(f)
for d in data.get('devices', []):
    name = d.get('product', 'Unknown Device')
    vid = d.get('vendor_id', 'N/A')
    pid = d.get('product_id', 'N/A')
    is_kb = '✓' if d.get('is_keyboard') else '✗'
    is_mouse = '✓' if d.get('is_pointing_device') else '✗'
    is_builtin = '✓' if d.get('is_built_in_keyboard') else '✗'
    print(f'  {name}')
    print(f'    Vendor ID: {vid}, Product ID: {pid}')
    print(f'    Keyboard: {is_kb}, Mouse: {is_mouse}, Built-in: {is_builtin}')
" 2>/dev/null
else
    echo "Devices file not found"
fi
echo ""

# Simple modifications in current profile
echo "## Simple Modifications (Current Profile)"
if [ -f "$CONFIG_PATH" ]; then
    python3 -c "
import json
with open('$CONFIG_PATH') as f:
    config = json.load(f)
profile = next((p for p in config['profiles'] if p.get('selected')), None)
if profile:
    mods = profile.get('simple_modifications', [])
    if mods:
        for m in mods:
            fr = m.get('from', {}).get('key_code', 'unknown')
            to = m.get('to', [{}])[0].get('key_code', 'unknown')
            print(f'  {fr} → {to}')
    else:
        print('  (none)')
" 2>/dev/null
fi
echo ""

# Complex modification rules
echo "## Complex Modification Rules (Current Profile)"
if [ -f "$CONFIG_PATH" ]; then
    python3 -c "
import json
with open('$CONFIG_PATH') as f:
    config = json.load(f)
profile = next((p for p in config['profiles'] if p.get('selected')), None)
if profile:
    rules = profile.get('complex_modifications', {}).get('rules', [])
    for i, r in enumerate(rules, 1):
        desc = r.get('description', 'No description')
        manip_count = len(r.get('manipulators', []))
        print(f'  {i}. {desc} ({manip_count} manipulator(s))')
" 2>/dev/null
fi
echo ""

echo "=== End of Report ==="
