from textual.app import App
from .screen.title import TitleScreen, TitleScreenResult
from .screen.game.game import GameScreen

from textual.app import ComposeResult
from textual.widgets import Static

class PrintStatic(Static):
    text = "Hello, world!"

    def render(self) -> str:
        return f"{self.text}"


class AIWolfNLPApp(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    SCREENS = {"start": TitleScreen}

    def compose(self) -> ComposeResult:
        yield PrintStatic()

    def on_mount(self) -> None:
        def check_select(result:TitleScreenResult) -> None:
            if result.is_start:
                game_screen = GameScreen(user_name=result.user_name)
                self.push_screen(game_screen)
            elif result.is_exit:
                self.app.exit()

        self.push_screen("start", check_select)

    def action_toggle_dark(self) -> None:
        self.theme = "textual-dark" if self.theme == "textual-light" else "textual-light"
