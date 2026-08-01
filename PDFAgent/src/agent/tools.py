from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
import ast
import operator


@dataclass
class Tool:
    name: str
    description: str
    function: Callable[[str], str]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, name: str, description: str) -> Callable:
        def decorator(function: Callable[[str], str]) -> Callable[[str], str]:
            self._tools[name] = Tool(name, description, function)
            return function

        return decorator

    def call(self, name: str, argument: str) -> str:
        if name not in self._tools:
            return f"Unknown tool: {name}"
        try:
            return self._tools[name].function(argument)
        except Exception as exc:  # Keep one bad tool call from killing the session.
            return f"Tool error: {exc}"

    def names(self) -> list[str]:
        return sorted(self._tools)


registry = ToolRegistry()


@registry.register("time", "Get the current local date and time")
def current_time(_: str) -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")


_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def _evaluate(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_evaluate(node.left), _evaluate(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_evaluate(node.operand))
    raise ValueError("only numeric expressions are supported")


@registry.register("calculate", "Safely evaluate a numeric expression")
def calculate(expression: str) -> str:
    tree = ast.parse(expression, mode="eval")
    return str(_evaluate(tree.body))
