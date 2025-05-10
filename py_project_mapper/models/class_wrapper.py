import ast
import textwrap
from typing import List, Optional

from .function_wrapper import FunctionWrapper


class ClassWrapper:
    def __init__(self, node: ast.ClassDef):
        self.node = node

    @property
    def name(self) -> str:
        return self.node.name

    @property
    def docstring(self) -> Optional[str]:
        return ast.get_docstring(self.node)

    @property
    def bases(self) -> List[str]:
        return [base.id for base in self.node.bases if isinstance(base, ast.Name)]

    @property
    def methods(self) -> List[FunctionWrapper]:
        return [FunctionWrapper(child_node) for child_node in self.node.body
                if isinstance(child_node, (ast.FunctionDef, ast.AsyncFunctionDef))]

    def formatted(self, indent: int = 0) -> str:
        base_str = f"({', '.join(self.bases)})" if self.bases else ""
        result = f"class {self.name}{base_str}:\n"

        if self.docstring:
            docstring_lines = self.docstring.strip().splitlines()
            formatted_docstring = '"""\n' + "\n".join(docstring_lines) + '\n"""\n'
            result += textwrap.indent(formatted_docstring, " " * 2)

        if self.methods:
            # Add a newline between class docstring and first method if both exist
            if self.docstring:
                result += "\n"
            formatted_methods = [method.formatted(indent=2) for method in self.methods]  # Methods indented relative to class
            result += "\n".join(formatted_methods)
        elif not self.docstring:  # If no methods and no docstring, add a pass
            result += textwrap.indent("pass\n", " " * 2)

        return textwrap.indent(result, " " * indent)
