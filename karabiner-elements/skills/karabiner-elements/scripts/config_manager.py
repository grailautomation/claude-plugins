#!/usr/bin/env python3
"""
Karabiner-Elements Configuration Manager
Safe utilities for reading and modifying Karabiner configurations.
"""

import json
import sys
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List

CONFIG_PATH = Path.home() / '.config/karabiner/karabiner.json'
COMPLEX_MODS_DIR = Path.home() / '.config/karabiner/assets/complex_modifications'
BACKUP_DIR = Path.home() / '.config/karabiner/backups'

def backup_config() -> Path:
    """Create a timestamped backup of the current config."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = BACKUP_DIR / f'karabiner_{timestamp}.json'
    shutil.copy(CONFIG_PATH, backup_path)
    return backup_path

def load_config() -> Dict[str, Any]:
    """Load the current Karabiner configuration."""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config not found: {CONFIG_PATH}")
    return json.loads(CONFIG_PATH.read_text())

def save_config(config: Dict[str, Any], backup: bool = True) -> None:
    """Save configuration with optional backup."""
    if backup:
        backup_config()
    CONFIG_PATH.write_text(json.dumps(config, indent=4))

def get_selected_profile(config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Get the currently selected profile."""
    for profile in config.get('profiles', []):
        if profile.get('selected'):
            return profile
    return None

def list_profiles(config: Dict[str, Any]) -> List[str]:
    """List all profile names."""
    return [p.get('name', 'Unnamed') for p in config.get('profiles', [])]

def get_profile_by_name(config: Dict[str, Any], name: str) -> Optional[Dict[str, Any]]:
    """Get a profile by name."""
    for profile in config.get('profiles', []):
        if profile.get('name') == name:
            return profile
    return None


def add_complex_rule(profile: Dict[str, Any], rule: Dict[str, Any]) -> None:
    """Add a complex modification rule to a profile."""
    if 'complex_modifications' not in profile:
        profile['complex_modifications'] = {'parameters': {}, 'rules': []}
    if 'rules' not in profile['complex_modifications']:
        profile['complex_modifications']['rules'] = []
    profile['complex_modifications']['rules'].append(rule)

def remove_complex_rule(profile: Dict[str, Any], description: str) -> bool:
    """Remove a complex modification rule by description. Returns True if found."""
    rules = profile.get('complex_modifications', {}).get('rules', [])
    for i, rule in enumerate(rules):
        if rule.get('description') == description:
            rules.pop(i)
            return True
    return False

def add_simple_modification(profile: Dict[str, Any], from_key: str, to_key: str) -> None:
    """Add a simple key-to-key modification."""
    if 'simple_modifications' not in profile:
        profile['simple_modifications'] = []
    
    # Check if modification already exists
    for mod in profile['simple_modifications']:
        if mod.get('from', {}).get('key_code') == from_key:
            mod['to'] = [{'key_code': to_key}]
            return
    
    # Add new modification
    profile['simple_modifications'].append({
        'from': {'key_code': from_key},
        'to': [{'key_code': to_key}]
    })

def create_rule(description: str, manipulators: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a complex modification rule structure."""
    return {
        'description': description,
        'manipulators': manipulators
    }

def create_basic_manipulator(
    from_key: str,
    to_key: str,
    from_modifiers: Optional[Dict[str, Any]] = None,
    to_modifiers: Optional[List[str]] = None,
    conditions: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Create a basic manipulator structure."""
    manipulator = {
        'type': 'basic',
        'from': {'key_code': from_key},
        'to': [{'key_code': to_key}]
    }
    
    if from_modifiers:
        manipulator['from']['modifiers'] = from_modifiers
    
    if to_modifiers:
        manipulator['to'][0]['modifiers'] = to_modifiers
    
    if conditions:
        manipulator['conditions'] = conditions
    
    return manipulator


def save_complex_mod_file(filename: str, title: str, rules: List[Dict[str, Any]]) -> Path:
    """Save rules to a separate complex modifications file."""
    COMPLEX_MODS_DIR.mkdir(parents=True, exist_ok=True)
    filepath = COMPLEX_MODS_DIR / f'{filename}.json'
    content = {
        'title': title,
        'rules': rules
    }
    filepath.write_text(json.dumps(content, indent=4))
    return filepath

# CLI Interface
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Karabiner Configuration Manager')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # List profiles
    subparsers.add_parser('list-profiles', help='List all profiles')
    
    # Show current profile
    subparsers.add_parser('current-profile', help='Show current profile name')
    
    # List rules
    subparsers.add_parser('list-rules', help='List complex modification rules')
    
    # Backup
    subparsers.add_parser('backup', help='Create a backup of current config')
    
    # Add simple modification
    simple_parser = subparsers.add_parser('add-simple', help='Add simple modification')
    simple_parser.add_argument('from_key', help='Source key code')
    simple_parser.add_argument('to_key', help='Target key code')
    
    args = parser.parse_args()
    
    try:
        config = load_config()
        
        if args.command == 'list-profiles':
            for name in list_profiles(config):
                print(name)
        
        elif args.command == 'current-profile':
            profile = get_selected_profile(config)
            print(profile.get('name', 'Unknown') if profile else 'No profile selected')
        
        elif args.command == 'list-rules':
            profile = get_selected_profile(config)
            if profile:
                rules = profile.get('complex_modifications', {}).get('rules', [])
                for i, rule in enumerate(rules, 1):
                    print(f"{i}. {rule.get('description', 'No description')}")
        
        elif args.command == 'backup':
            backup_path = backup_config()
            print(f"Backup created: {backup_path}")
        
        elif args.command == 'add-simple':
            profile = get_selected_profile(config)
            if profile:
                add_simple_modification(profile, args.from_key, args.to_key)
                save_config(config)
                print(f"Added: {args.from_key} → {args.to_key}")
        
        else:
            parser.print_help()
            
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)
