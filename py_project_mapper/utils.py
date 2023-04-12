import ast
import os
from typing import List

from models import FileData, MethodData, ClassData


def walk_python_files(path: str) -> List[str]:
    return [os.path.join(root, file) for root, dirs, files in os.walk(path) for file in files if file.endswith(".py")]


def parse_python_file(file_path: str) -> FileData:
    with open(file_path, 'r') as file:
        content = file.read()
        tree = ast.parse(content)
        data = FileData(path=file_path)
        data.variables = [target.id for node in tree.body if isinstance(node, ast.Assign)
                          for target in node.targets if isinstance(target, ast.Name)]
        data.functions = [MethodData.from_node(node) for node in tree.body if
                          isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
        data.classes = [ClassData.from_node(node) for node in tree.body if isinstance(node, ast.ClassDef)]
    return data


def print_python_structure(file_data: FileData) -> None:
    print(f"File: {file_data.path}")
    print(" Variables:")
    for variable in file_data.variables:
        print(f" - {variable}")
    print(" Functions:")
    for function in file_data.functions:
        print(function.formatted(indent=8))
    print(" Classes:")
    for cls in file_data.classes:
        print(cls.formatted(indent=8))
