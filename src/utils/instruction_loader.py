import os
from pathlib import Path

# Get the src directory path (parent of utils)
SRC_DIR = Path(__file__).parent.parent

def load_instruction_from_file(file_path: str) -> str:
    """
    Loads instructions for an agent from a text file.
    
    Args:
        file_path: The path to the text file relative to the src directory.

    Returns:
        A string containing the entire content of the file, stripped of 
        leading/trailing whitespace.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        IOError: If an error occurs during file reading.
    """
    # Resolve path relative to src directory
    full_path = SRC_DIR / file_path
    
    if not full_path.exists():
        raise FileNotFoundError(f"Error: Instruction file not found at '{full_path}' (resolved from '{file_path}')")

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            instructions = f.read()
        return instructions.strip()

    except IOError as e:
        raise IOError(f"Error reading instruction file '{full_path}': {e}")