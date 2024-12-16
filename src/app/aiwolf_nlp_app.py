from textual.app import App
from .screen.start import Start


class AIWolfNLPApp(App):
    CSS_PATH = "aiwolf_nlp_app.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    SCREENS = {"start": Start}

    def on_mount(self) -> None:
        self.push_screen("start")

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = "textual-dark" if self.theme == "textual-light" else "textual-light"
