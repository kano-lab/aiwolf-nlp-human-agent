from textual.app import App
from .screen.start import Start

from textual.app import ComposeResult
from textual.widgets import Static

class PrintStatic(Static):
    text = "Hello, world!"

    def render(self) -> str:
        return f"{self.text}"


class AIWolfNLPApp(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    SCREENS = {"start": Start}

    def compose(self) -> ComposeResult:
        yield PrintStatic()

    def on_mount(self) -> None:
        def check_select(args:tuple[str, str] | None) -> None:
            button_id, player_name = args
            if button_id == "start":
                self.query_one(PrintStatic).text = args
            elif button_id == "exit":
                self.app.exit()

        self.push_screen("start", check_select)

    def action_toggle_dark(self) -> None:
        self.theme = "textual-dark" if self.theme == "textual-light" else "textual-light"
