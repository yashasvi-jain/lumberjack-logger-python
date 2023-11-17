from typing import Optional


def getCode(filepath: str) -> Optional[str]:
    """
    Reads the code from the provided filepath.

    Args:
        filepath (str): The path of the file to read.

    Returns:
        str: The code from the file.
    """

    if not filepath:
        return None

    try:
        with open(filepath, 'r') as f:
            code: str = f.read()
            return code
    except:
        return None
