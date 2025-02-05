from aiwolf_nlp_common.protocol.list import TalkInfo, TalkList
from textual.widgets import RichLog


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

            self.add_message(message=f"{talk_elem.agent}:{talk_elem.text}")
            self.latest_history_index = talk_elem.idx

        self.update()

    def daily_initialize(self) -> None:
        self.add_system_message(message="朝が来ました:sunrise:", morning=True)
        self.latest_history_index = None
