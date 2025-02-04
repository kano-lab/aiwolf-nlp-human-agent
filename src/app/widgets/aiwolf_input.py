from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.widgets import Button, Input, LoadingIndicator


class AIWolfNLPInputGroup(HorizontalGroup):
    def __init__(self, *children, name=None, id=None, classes=None, disabled=False):
        self.content_disabled = disabled
        self.loading_indicator = LoadingIndicator(id="loading")

        super().__init__(*children, name=name, id=id, classes=classes, disabled=False)

    def compose(self) -> ComposeResult:
        self.input = Input(id="comment_field")
        self.button = Button(":play_button:", id="send_button")

        yield self.input
        yield self.button

    def _on_mount(self, event):
        if self.content_disabled:
            self.disable()

        return super()._on_mount(event)

    async def enable(self) -> None:
        self.input.disabled = False
        self.button.disabled = False

        if self.input.children:
            await self.input.remove_children()

    async def disable(self) -> None:
        self.input.disabled = True
        self.button.disabled = True

        if not self.input.children:
            await self.input.mount(self.loading_indicator)

    def toggle_availability(self) -> None:
        if self.content_disabled:
            self.enable()
        else:
            self.disable()
