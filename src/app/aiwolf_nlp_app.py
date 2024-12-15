from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Input, Button, Footer


class AIWolfNLPApp(App):
    CSS_PATH = "aiwolf_nlp_app.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        yield Container(
            Input(
                value="Human",
                placeholder="Please input player name",
                type="text",
                select_on_focus=False,
                id="player_name",
            ),
            Button(label="Start", id="start"),
            Button(label="Exit", id="exit"),
            id="main_container",
            classes="box"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "exit":
            self.app.exit()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = "textual-dark" if self.theme == "textual-light" else "textual-light"
