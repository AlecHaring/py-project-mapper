import ast
from dataclasses import dataclass
from typing import List

from .function_wrapper import FunctionWrapper
from .class_wrapper import ClassWrapper


@dataclass
class PythonFile:
    def __init__(self, file_path: str):
        self.path = file_path
        self.variables: List[str] = []
        self.functions: List[FunctionWrapper] = []
        self.classes: List[ClassWrapper] = []

        with open(file_path, 'r') as file:
            content = file.read()
            tree = ast.parse(content)
            for node in tree.body:
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            self.variables.append(target.id)

                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    self.functions.append(FunctionWrapper(node))

                if isinstance(node, ast.ClassDef):
                    self.classes.append(ClassWrapper(node))

    def formatted(self) -> str:
        output_parts = [
            f"--- File: {self.path} ---"
        ]

        if self.variables:
            output_parts.append("Variables:")
            for variable in self.variables:
                output_parts.append(f"  - {variable}")

        if self.functions:
            if self.variables:  # Add a newline if variables were printed
                output_parts.append("")
            output_parts.append("Functions:")
            for function_wrapper in self.functions:
                output_parts.append(function_wrapper.formatted(indent=1))

        if self.classes:
            if self.variables or self.functions:  # Add a newline if other sections exist
                output_parts.append("")
            output_parts.append("Classes:")
            for class_wrapper in self.classes:
                output_parts.append(class_wrapper.formatted(indent=1))

        return "\n".join(output_parts)
