import os

def load_instruction_from_file(file_path: str) -> str:
    """
    Loads instructions for an agent from a text file.
    
    Args:
        file_path: The full path to the text file containing the instructions.

    Returns:
        A string containing the entire content of the file, stripped of 
        leading/trailing whitespace.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        IOError: If an error occurs during file reading.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: Instruction file not found at '{file_path}'")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            instructions = f.read()
        return instructions.strip()

    except IOError as e:
        raise IOError(f"Error reading instruction file '{file_path}': {e}")