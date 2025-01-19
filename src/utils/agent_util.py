import re

def agent_name_to_idx(name: str) -> int:
    match = re.search(r"\d+", name)
    if match is None:
        raise ValueError(name, "No number found in agent name")
    return int(match.group())


def agent_idx_to_agent(idx: int) -> str:
    return f"Agent[{idx:0>2d}]"
