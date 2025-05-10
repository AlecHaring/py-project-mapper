import os
from typing import List


def walk_python_files(path: str) -> List[str]:
    """
    Walks through the given path and returns a list of all python file paths.
    """
    return [os.path.join(root, file) for root, dirs, files in os.walk(path) for file in files if file.endswith(".py")]
