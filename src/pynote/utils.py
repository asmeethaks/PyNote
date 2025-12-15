# src/pynote/utils.py
"""
Utility functions for PyNote editor.
"""

import os
import json
from pathlib import Path


def get_config_dir():
    """
    Get the configuration directory for PyNote.
    
    Returns:
        Path: Configuration directory path
    """
    if os.name == 'nt':  # Windows
        config_dir = Path(os.environ.get('APPDATA', '')) / 'PyNote'
    else:  # macOS/Linux
        config_dir = Path.home() / '.config' / 'pynote'
    
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def load_settings():
    """
    Load settings from JSON file.
    
    Returns:
        dict: Settings dictionary
    """
    config_file = get_config_dir() / 'settings.json'
    default_settings = {
        'theme': 'light',
        'window_geometry': '800x600'
        'autosave': False,
        'autosave_interval': 300,  # seconds
        'tab_size': 4,
        'font_family': 'Courier New',
        'font_size': 12,
        'recent_files': [],
    }
    
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            # Merge with defaults to handle missing keys
            default_settings.update(settings)
            return default_settings
        except Exception:
            return default_settings
    
    return default_settings


def save_settings(settings):
    """
    Save settings to JSON file.
    
    Args:
        settings: Settings dictionary
    """
    config_file = get_config_dir() / 'settings.json'
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2)
    except Exception as e:
        print(f"Failed to save settings: {e}")


def count_words(text):
    """
    Count words in text.
    
    Args:
        text: Text string
    
    Returns:
        int: Word count
    """
    return len(text.split())


def count_chars(text):
    """
    Count characters in text (excluding trailing newline).
    
    Args:
        text: Text string
    
    Returns:
        int: Character count
    """
    return len(text.rstrip('\n'))


def detect_encoding(filepath):
    """
    Detect file encoding (basic implementation).
    
    Args:
        filepath: Path to file
    
    Returns:
        str: Encoding name (defaults to 'utf-8')
    """
    try:
        # Try UTF-8 first
        with open(filepath, 'r', encoding='utf-8') as f:
            f.read()
        return 'utf-8'
    except UnicodeDecodeError:
        # Fallback to latin-1
        try:
            with open(filepath, 'r', encoding='latin-1') as f:
                f.read()
            return 'latin-1'
        except Exception:
            return 'utf-8'

