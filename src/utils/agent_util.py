import re

from aiwolf_nlp_common.role import RoleInfo

import player
import player.human


def set_role(
    prev_agent: player.agent.Agent,
) -> player.agent.Agent:
    agent = player.human.Human()
    agent.transfer_state(prev_agent=prev_agent)
    return agent

def agent_name_to_idx(name: str) -> int:
    match = re.search(r"\d+", name)
    if match is None:
        raise ValueError(name, "No number found in agent name")
    return int(match.group())


def agent_idx_to_agent(idx: int) -> str:
    return f"Agent[{idx:0>2d}]"
