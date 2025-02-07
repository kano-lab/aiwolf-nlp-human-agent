from aiwolf_nlp_common.protocol.info.map import AgentStatus, StatusMap
from aiwolf_nlp_common.status import Status
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.screen import ModalScreen
from textual.widgets import Button, Label

from player.agent import Agent


class VoteScreen(ModalScreen[str]):
    CSS_PATH = "vote.tcss"

    __max_row_button_num: int = 3

    __error_description: str = "[b]説明が追加されていません。"
    __vote_description: str = "[b]投票を行うエージェントを選択してください。"
    __divine_description: str = "[b]占いを行うエージェントを選択してください。"
    __attack_description: str = "[b]襲撃を行うエージェントを選択してください。"

    def __init__(
        self,
        agent: Agent,
        name: str = None,
        id: str = None,
        classes: str = None,
        *,
        vote: bool = False,
        divine: bool = False,
        attack: bool = False,
    ) -> None:
        self.agent_name: str = agent.info.agent
        self.status_map: StatusMap = agent.info.status_map
        self.vote = vote
        self.divine = divine
        self.attack = attack

        super().__init__(name, id, classes)

    def _set_button(self, frame: VerticalGroup) -> None:
        agent_list = sorted(self.status_map, key=lambda x: x.agent)
        agent_status: AgentStatus

        button_row = HorizontalGroup(classes="button_row")
        row_num: int = 0
        button_num: int = 0

        for agent_status in agent_list:
            if Status.is_alive(status=agent_status.status):
                button_row.compose_add_child(
                    Button(
                        label=agent_status.agent,
                        classes="alive",
                        disabled=agent_status.agent == self.agent_name,
                    ),
                )
            else:
                button_row.compose_add_child(
                    Button(label=agent_status.agent, classes="dead", disabled=True),
                )

            button_num += 1

            if button_num % self.__max_row_button_num == 0:
                button_row.id = f"row_{row_num + 1}"
                frame.compose_add_child(button_row)
                button_row = HorizontalGroup(classes="button_row")
                row_num += 1
                button_num = 0

        if button_num % self.__max_row_button_num != 0:
            button_row.id = f"row_{row_num + 1}"
            frame.compose_add_child(button_row)

    def _get_description(self) -> str:
        if self.vote:
            return self.__vote_description

        if self.divine:
            return self.__divine_description

        if self.attack:
            return self.__attack_description

        return self.__error_description

    def compose(self) -> ComposeResult:
        frame = VerticalGroup(id="vote_frame")

        frame.compose_add_child(Label(self._get_description(), id="vote_description"))
        self._set_button(frame=frame)

        yield frame

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(str(event.button.label))
