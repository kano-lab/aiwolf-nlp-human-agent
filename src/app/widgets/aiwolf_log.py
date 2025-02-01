from textual.widgets import RichLog


class AIwolfNLPLog(RichLog):
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
        self.messages: list = []
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

    def _assignment_decoration(
        self,
        message: str,
        *,
        red: bool = False,
        green: bool = False,
        blue: bool = False,
        under_line: bool = False,
    ) -> str:
        options: list = []

        if (red and green) or (red and blue) or (green and blue):
            raise ValueError("Only one of red, green, or blue can be True at a time.")

        if red:
            options.append("red")

        if blue:
            options.append("blue")

        if green:
            options.append("green")

        if under_line:
            options.append("u")

        bbcode_start: str = f"[{" ".join(options)}]"
        bbcode_end: str = f"[/{" ".join(options)}]"

        return bbcode_start + message + bbcode_end

    def add_message(self, message: str) -> None:
        self.messages.append(message)

    def add_system_message(
        self,
        message: str,
        *,
        success: bool = False,
        error: bool = False,
        night: bool = False,
    ) -> None:
        system_message: str = f"\n{self._assignment_decoration(message=message, red=error, green=success, blue=night, under_line=True)}\n"

        self.add_message(message=system_message)

    def write(self) -> None:
        self.write("\n".join(self.messages))
