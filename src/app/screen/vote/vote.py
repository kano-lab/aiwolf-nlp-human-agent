from aiwolf_nlp_common.protocol.info.map import AgentStatus, StatusMap
from aiwolf_nlp_common.status import Status
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button


class VoteScreen(ModalScreen[str]):
    def __init__(self, status_map: StatusMap, name=None, id=None, classes=None):
        self.status_map: StatusMap = status_map
        super().__init__(name, id, classes)

    def compose(self) -> ComposeResult:
        agent_list = sorted(self.status_map, key=lambda x: x.agent)

        agent_status: AgentStatus
        for agent_status in agent_list:
            if Status.is_alive(status=agent_status.status):
                yield Button(label=agent_status.agent)
            else:
                yield Button(label=agent_status.agent, disabled=True)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(str(event.button.label))
