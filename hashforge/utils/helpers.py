#!/usr/bin/env python3
"""
HashForge Utility Functions
"""

import sys
from pathlib import Path


def read_from_stdin() -> str:
    """Read data from stdin if available."""
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    return None


def read_file_safe(path: str) -> bytes:
    """Safely read file contents."""
    try:
        with open(path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    except PermissionError:
        raise PermissionError(f"Permission denied: {path}")


def format_output(data: str, format_type: str = 'text') -> str:
    """Format output based on type."""
    if format_type == 'json':
        import json
        return json.dumps({'result': data}, indent=2)
    return data


def truncate_string(s: str, max_len: int = 80) -> str:
    """Truncate string with ellipsis."""
    if len(s) <= max_len:
        return s
    return s[:max_len-3] + '...'


def validate_file_path(path: str) -> Path:
    """Validate and return Path object."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if not p.is_file():
        raise ValueError(f"Not a file: {path}")
    return p
