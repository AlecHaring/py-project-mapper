import argparse
import os
import ast
from dataclasses import dataclass, field
from typing import List, Union


@dataclass
class MethodData:
    name: str
    signature: str
    is_async: bool

    @classmethod
    def from_node(cls, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> 'MethodData':
        signature = cls.get_function_signature(node)
        return cls(name=node.name, signature=signature, is_async=isinstance(node, ast.AsyncFunctionDef))

    @staticmethod
    def get_function_signature(node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> str:
        signature = "("
        for arg in node.args.args:
            arg_type = arg.annotation.id if arg.annotation and isinstance(arg.annotation, ast.Name) else "Any"
            signature += f"{arg.arg}: {arg_type}, "
        signature = signature.rstrip(", ")
        signature += f") -> {node.returns.id if node.returns and isinstance(node.returns, ast.Name) else 'None'}"
        return signature

    def formatted(self, indent: int = 0) -> str:
        prefix = " " * indent
        func_type = "async def" if self.is_async else "def"
        result = f"{prefix}{func_type} {self.name}{self.signature}\n"
        return result


@dataclass
class ClassData:
    name: str
    bases: List[str] = field(default_factory=list)
    methods: List[MethodData] = field(default_factory=list)

    @classmethod
    def from_node(cls, node: ast.ClassDef) -> 'ClassData':
        class_data = cls(name=node.name)
        class_data.methods = [MethodData.from_node(child_node) for child_node in node.body if
                              isinstance(child_node, (ast.FunctionDef, ast.AsyncFunctionDef))]
        class_data.bases = [base.id for base in node.bases if isinstance(base, ast.Name)]
        return class_data

    def formatted(self, indent: int = 0) -> str:
        prefix = " " * indent
        base_str = f"({', '.join(self.bases)})" if self.bases else ""
        result = f"{prefix}class {self.name}{base_str}\n"
        for method in self.methods:
            result += method.formatted(indent=indent + 4)
        return result


@dataclass
class FileData:
    path: str
    variables: List[str] = field(default_factory=list)
    functions: List[MethodData] = field(default_factory=list)
    classes: List[ClassData] = field(default_factory=list)


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


def main():
    parser = argparse.ArgumentParser(description="Analyze Python project structure.")
    parser.add_argument("-p", "--project_path", required=True, help="The path to the project directory.")
    args = parser.parse_args()

    project_path = args.project_path
    python_files = walk_python_files(project_path)
    for file_path in python_files:
        file_data = parse_python_file(file_path)
        print_python_structure(file_data)


if __name__ == "__main__":
    main()
