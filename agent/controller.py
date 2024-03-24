"""Agent controller"""

from typing import Callable
from agent.config import get_agents


class Agent:
    """The agent class"""

    def __init__(
        self,
        validator_list: str,
        current_term_id: str,
        aggregate: Callable[[str, str], str],
    ):
        """Initialize the agent"""
        self.user_proxy, self.aggregator = get_agents(
            validator_list, current_term_id, aggregate
        )

    def respond(self, query: str) -> str:
        """Respond to a query"""
        result = self.user_proxy.initiate_chat(
            self.aggregator, message=query, summary_method="last_msg"
        )
        return result.summary
