from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Input, Button


class Start(Screen):
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
            classes="box",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start":
            pass

        if event.button.id == "exit":
            self.app.exit()
