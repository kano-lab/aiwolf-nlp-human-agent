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

    def on_button_pressed(self, button_event: Button.Pressed) -> None:
        self.dismiss((button_event.button.id, self.query_one(Input).value))
