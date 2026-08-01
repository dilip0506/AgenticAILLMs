import unittest

from agent import Agent


class AgentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = Agent()

    def test_calculation(self) -> None:
        self.assertEqual(self.agent.respond("calculate 12 * (3 + 4)"), "84")

    def test_time_tool(self) -> None:
        result = self.agent.respond("What time is it?")
        self.assertNotIn("Unknown tool", result)

    def test_memory(self) -> None:
        self.agent.respond("hello")
        self.assertEqual(len(self.agent.memory.messages), 2)


if __name__ == "__main__":
    unittest.main()
