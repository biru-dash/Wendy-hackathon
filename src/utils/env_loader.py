"""
Utility module to load environment variables from .env file.
This ensures all agents can access the same configuration.

Usage:
    from utils.env_loader import load_env
    load_env()  # Call this at the start of your agent or script
"""

import os
from pathlib import Path
from typing import Optional


def find_project_root() -> Path:
    """
    Find the project root directory by looking for .env file or .git directory.
    
    Returns:
        Path to project root directory
    """
    # Start from this file's directory and walk up
    current = Path(__file__).parent.parent.parent  # Go up from src/utils/env_loader.py to project root
    
    # Look for .env file or .git directory to confirm we're at root
    if (current / ".env").exists() or (current / ".git").exists():
        return current
    
    # Fallback: assume we're in the right place
    return current


def load_env(env_file: Optional[str] = None) -> None:
    """
    Load environment variables from .env file.
    
    This function tries to use python-dotenv if available, otherwise
    it manually parses the .env file and sets environment variables.
    
    Args:
        env_file: Optional path to .env file. If not provided, looks for .env in project root.
    """
    project_root = find_project_root()
    
    if env_file is None:
        env_file = project_root / ".env"
    else:
        env_file = Path(env_file)
    
    if not env_file.exists():
        # .env file doesn't exist, that's okay - use system environment variables
        return
    
    # Try to use python-dotenv if available
    try:
        from dotenv import load_dotenv
        load_dotenv(env_file, override=False)  # Don't override existing env vars
        return
    except ImportError:
        # python-dotenv not installed, manually parse .env file
        pass
    
    # Manual parsing of .env file (simple implementation)
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Parse KEY=VALUE format
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                
                # Only set if not already in environment (don't override)
                if key and key not in os.environ:
                    os.environ[key] = value


# Auto-load .env when this module is imported
# This ensures environment variables are available to all agents
load_env()

