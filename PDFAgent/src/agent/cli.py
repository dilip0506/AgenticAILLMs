from .agent import Agent


def main() -> None:
    agent = Agent()
    print("Python Agent — type 'help' for examples, or 'quit' to exit.")
    while True:
        try:
            prompt = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if prompt.lower() in {"quit", "exit"}:
            break
        if not prompt:
            continue
        print(f"Agent: {agent.respond(prompt)}")


if __name__ == "__main__":
    main()
