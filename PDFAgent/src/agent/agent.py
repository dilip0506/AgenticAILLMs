from dataclasses import dataclass
import re

from .memory import ConversationMemory
from .tools import ToolRegistry, registry


@dataclass
class Action:
    kind: str
    value: str
    argument: str = ""


class Agent:
    """A deterministic starter agent with replaceable decision logic."""

    def __init__(self, tools: ToolRegistry = registry) -> None:
        self.tools = tools
        self.memory = ConversationMemory()

    def respond(self, prompt: str) -> str:
        self.memory.add("user", prompt)
        action = self._decide(prompt)
        if action.kind == "tool":
            answer = self.tools.call(action.value, action.argument)
        else:
            answer = action.value
        self.memory.add("assistant", answer)
        return answer

    def _decide(self, prompt: str) -> Action:
        normalized = prompt.strip()
        lowered = normalized.lower()
        if re.search(r"\b(what time|current time|date and time)\b", lowered):
            return Action("tool", "time")
        if lowered.startswith(("calculate ", "compute ")):
            expression = normalized.split(" ", 1)[1]
            return Action("tool", "calculate", expression)
        if lowered in {"help", "tools"}:
            available = ", ".join(self.tools.names())
            return Action("text", f"Available tools: {available}")
        return Action("text", f"I received: {normalized}\nTry 'help', 'What time is it?', or 'calculate 2 + 2'.")
