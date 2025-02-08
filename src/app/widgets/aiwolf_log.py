from aiwolf_nlp_common.protocol.list import TalkInfo, TalkList
from textual.widgets import RichLog

import random

from utils import agent_util


class AIwolfNLPLog(RichLog):
    __padding = "\t"

    def __init__(
        self,
        *,
        max_lines=None,
        min_width=78,
        wrap=False,
        highlight=False,
        markup=False,
        auto_scroll=True,
        name=None,
        id=None,
        classes=None,
        disabled=False,
    ):
        self.messages: list[str | TalkInfo] = []
        self.latest_history_index: int | None = None

        super().__init__(
            max_lines=max_lines,
            min_width=min_width,
            wrap=wrap,
            highlight=highlight,
            markup=markup,
            auto_scroll=auto_scroll,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )

        self.agent_color = self._set_agent_color()

    def _set_agent_color(self) -> dict:
        reddish_list: list = ["orchid2", "hot_pink2"]
        yellowish_list = ["light_goldenrod1", "yellow2"]
        cyanotype_list: list = ["light_cyan1", "light_steel_blue"]
        greenish_list: list = ["pale_green1", "sea_green1"]
        purple_list: list = ["dark_violet", "medium_orchid"]

        agent_list: list = []
        agent_color: dict = {}

        for i in range(5):
            agent_list.append(agent_util.agent_idx_to_agent(idx=i + 1))

        random.shuffle(agent_list)

        for index, agent in enumerate(agent_list):
            if index % 5 == 1:
                agent_color[agent] = random.choice(reddish_list)
            elif index % 5 == 2:
                agent_color[agent] = random.choice(yellowish_list)
            elif index % 5 == 3:
                agent_color[agent] = random.choice(cyanotype_list)
            elif index % 5 == 4:
                agent_color[agent] = random.choice(greenish_list)
            else:
                agent_color[agent] = random.choice(purple_list)

        return agent_color

    def _color_option(
        sel, red: bool = False, green: bool = False, blue: bool = False, orange: bool = False
    ) -> str:
        if red:
            return "red"

        if blue:
            return "blue"

        if green:
            return "green"

        if orange:
            return "orange1"

        return "bright_white"

    def _assignment_decoration(
        self,
        message: str,
        *,
        red: bool = False,
        green: bool = False,
        blue: bool = False,
        orange: bool = False,
        bold: bool = False,
        under_line: bool = False,
    ) -> str:
        options: list = []

        options.append(self._color_option(red=red, green=green, blue=blue, orange=orange))

        if bold:
            options.append("b")

        if under_line:
            options.append("u")

        bbcode_start: str = f"[{' '.join(options)}]"
        bbcode_end: str = f"[/{' '.join(options)}]"

        return bbcode_start + message + bbcode_end

    def add_message(self, message: str) -> None:
        self.messages.append(self.__padding + message)
        self.update()

    def add_system_message(
        self,
        message: str,
        *,
        success: bool = False,
        error: bool = False,
        morning: bool = False,
        night: bool = False,
    ) -> None:
        system_message: str = self._assignment_decoration(
            message=message,
            red=error,
            green=success,
            blue=night,
            orange=morning,
            bold=True,
            under_line=True,
        )

        if len(self.messages):
            system_message = "\n" + self.__padding + system_message

        self.add_message(message=system_message)

    def _allocate_agent_color(self, text: str) -> str:
        for agent, color in self.agent_color.items():
            text = text.replace(f">>{agent}", f"[{color}]>>{agent}[/{color}]").replace(
                f"{agent}", f"[{color}]{agent}[/{color}]"
            )

        return text

    def write(self, width=None, expand=False, shrink=True, scroll_end=None, animate=False):
        content = str("\n".join(self.messages))
        return super().write(content=content)

    def update(self) -> None:
        self.clear()
        self.write()

    def update_talk_history(self, talk_history: TalkList | None) -> None:
        if talk_history is None:
            return

        for talk_elem in talk_history:
            if self.latest_history_index is not None and talk_elem.idx <= self.latest_history_index:
                continue

            self.add_message(
                message=self._allocate_agent_color(text=f"{talk_elem.agent}:{talk_elem.text}")
            )
            self.latest_history_index = talk_elem.idx

        self.update()

    def daily_initialize(self) -> None:
        self.add_system_message(message="朝が来ました:sunrise:", morning=True)
        self.latest_history_index = None
