import os


def extract_base_name(filename: str) -> str:
    """
    Extract the base name from a filename, removing extension and path.
    
    Args:
        filename: The input filename (may include path and extension)
        
    Returns:
        The base name without extension or path
        
    Example:
        "Beyonce.wav" -> "Beyonce"
    """
    basename = os.path.basename(filename)
    parts = basename.split('.')
    if len(parts) == 1:
        return parts[0]
    return '.'.join(parts[:-1])