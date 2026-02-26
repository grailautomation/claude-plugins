# Maintenance, Device Info & Troubleshooting

## Maintenance Operations

### Restart Karabiner-Elements Service
```bash
launchctl kickstart -k gui/$(id -u)/org.pqrs.service.agent.karabiner_console_user_server
```

### Uninstall Karabiner-Elements
```bash
# First deactivate the driver
bash '/Library/Application Support/org.pqrs/Karabiner-DriverKit-VirtualHIDDevice/scripts/uninstall/deactivate_driver.sh'

# Then run uninstall (requires sudo)
sudo '/Library/Application Support/org.pqrs/Karabiner-Elements/uninstall.sh'
```

### Unlock Application Files (if locked)
```bash
sudo chflags nouchg,noschg /Applications/Karabiner-Elements.app
sudo chflags nouchg,noschg /Applications/Karabiner-EventViewer.app
```

### Check Logs
```bash
# System logs for Karabiner
log show --predicate 'subsystem == "org.pqrs.karabiner"' --last 1h

# Check log directory
ls -la /var/log/karabiner/ 2>/dev/null || echo "Log directory not found"
```

## Device Information

### Finding Device Identifiers
Use EventViewer or parse the devices file:
```bash
cat ~/.local/share/karabiner/karabiner_grabber_devices.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for d in data.get('devices', []):
    print(f\"Device: {d.get('product', 'Unknown')}\")
    print(f\"  Vendor ID: {d.get('vendor_id')}\")
    print(f\"  Product ID: {d.get('product_id')}\")
    print(f\"  Is Keyboard: {d.get('is_keyboard')}\")
    print()
"
```

### Common Vendor IDs
- Apple: 1452, 76
- Logitech: 1133
- Microsoft: 1118
- Razer: 5426

## Environment Variables

Edit environment file (requires root):
```bash
# Location
/Library/Application Support/org.pqrs/config/karabiner_environment

# Example content
PATH=$HOME/opt/bin:$PATH
XDG_CONFIG_HOME=$HOME/Library/Application Support/org.pqrs/config
```

After editing, restart the service:
```bash
launchctl kickstart -k gui/$(id -u)/org.pqrs.service.agent.karabiner_console_user_server
```

## Troubleshooting

### Karabiner Not Working After macOS Update
1. Open System Settings > Privacy & Security > Input Monitoring
2. Remove and re-add Karabiner-Elements components
3. Restart your Mac

### Keys Not Being Remapped
1. Check if correct profile is selected: `karabiner_cli --show-current-profile-name`
2. Verify the device is being grabbed (check EventViewer > Devices)
3. Lint your complex modifications: `karabiner_cli --lint-complex-modifications ...`

### Configuration Reset
If config is corrupted, reset to defaults:
```bash
mv ~/.config/karabiner/karabiner.json ~/.config/karabiner/karabiner.json.broken
# Karabiner will create a fresh config on next launch
```
