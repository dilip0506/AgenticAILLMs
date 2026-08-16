# Python Agent

A minimal Python agent scaffold with a tool registry, conversation memory, and a simple command-line interface. It uses only the Python standard library, so you can run it immediately and plug in an LLM later.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
agent
```

Then try:

```text
You: What time is it?
You: Calculate 12 * (3 + 4)
You: quit
```

## Project layout

```text
src/agent/
  agent.py       # Agent loop and decision logic
  cli.py         # Interactive terminal interface
  memory.py      # Conversation history
  tools.py       # Built-in tools and tool registry
tests/           # Small unit test suite
```

## Extending it

Add a function decorated with `@registry.register` in `src/agent/tools.py`, then teach `Agent._decide` how to select it. For an LLM-backed agent, replace `_decide` with a model client that returns the same `Action` structure.

Run tests with:

```bash
python -m unittest discover -s tests
```
