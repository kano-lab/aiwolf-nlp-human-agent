import random

from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Container, HorizontalGroup
from textual.widgets import Input, Button, Label
from art import *

def make_label(text: str, id: str, border_title: str = "", border_subtitle: str = "") -> Label:
    fonts:list = ["dancingfont", "doom", "larry3d"]
    text = text2art(text, font=random.choice(fonts))
    lbl = Label(text, id=id)
    lbl.border_title = border_title
    lbl.border_subtitle = border_subtitle

    return lbl


def make_label_container(
    container_id: str, text: str, label_id: str, border_title: str = "", border_subtitle: str = ""
) -> Container:
    return Container(
        make_label(
            text=text, id=label_id, border_title=border_title, border_subtitle=border_subtitle
        ),
        id=container_id,
    )


class TitleScreen(Screen):
    CSS_PATH = "title.tcss"

    def compose(self) -> ComposeResult:
        yield make_label_container(
            container_id="title_container",
            text="AI Wolf NLP",
            label_id="title",
            border_subtitle="Human Agent",
        )
        yield HorizontalGroup(
            Label(
                renderable="Player Name:",
                id="player_name_label",
            ),
            Input(
                value="Human",
                placeholder="Please input player name",
                type="text",
                select_on_focus=False,
                id="player_name",
            ),
            id="name_container",
            classes="box",
        )
        yield Container(
            Button(label="Start", id="start"),
            Button(label="Exit", id="exit"),
            id="button_container",
            classes="box",
        )

    def on_button_pressed(self, button_event: Button.Pressed) -> None:
        if not self.query_one(Input).is_valid:
            pass
        else:
            self.dismiss((button_event.button.id, self.query_one(Input).value))
