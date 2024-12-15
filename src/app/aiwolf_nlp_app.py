from textual.app import App, ComposeResult
from textual.widgets import Button

class AIWolfNLPApp(App):

    def compose(self) -> ComposeResult:
        yield Button("Start", id="start")
        yield Button.error("Exit", id="exit")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "exit":
            self.app.exit()