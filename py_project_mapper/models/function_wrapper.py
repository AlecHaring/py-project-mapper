import ast
import textwrap
from functools import cached_property
from typing import Union, Optional


class FunctionWrapper:
    def __init__(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]):
        self.node = node

    @property
    def name(self) -> str:
        return self.node.name

    @property
    def is_async(self) -> bool:
        return isinstance(self.node, ast.AsyncFunctionDef)

    @property
    def docstring(self) -> Optional[str]:
        return ast.get_docstring(self.node)

    @cached_property
    def signature(self) -> str:
        formatted_args = []
        for arg in self.node.args.args:
            annotation = None
            if arg.annotation:
                unparsed_annotation = ast.unparse(arg.annotation)
                annotation = unparsed_annotation.replace("'", "").replace('"', "")
            if annotation:
                formatted_args.append(f"{arg.arg}: {annotation}")
            else:
                formatted_args.append(arg.arg)
        return_type = ast.unparse(self.node.returns) if self.node.returns else None

        signature = "("
        signature += ", ".join(formatted_args)
        signature += ")"

        if return_type:
            signature += f" -> {return_type}"
        return signature

    def formatted(self, indent: int = 0) -> str:
        func_type = "async def" if self.is_async else "def"
        docstring = self.docstring
        result = f"{func_type} {self.name}{self.signature}\n"

        if docstring:
            formatted_docstring = f'"""\n{docstring}\n"""\n'
            result += textwrap.indent(formatted_docstring, " " * 2)

        return textwrap.indent(result, " " * indent)
