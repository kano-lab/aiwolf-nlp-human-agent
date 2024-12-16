from textual.app import App
from .screen.start import Start


class AIWolfNLPApp(App):
    CSS_PATH = "aiwolf_nlp_app.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    SCREENS = {"start": Start}

    def on_mount(self) -> None:
        def check_select(button_id: str | None) -> None:
            if button_id == "start":
                pass
            elif button_id == "exit":
                self.app.exit()

        self.push_screen("start", check_select)

    def action_toggle_dark(self) -> None:
        self.theme = "textual-dark" if self.theme == "textual-light" else "textual-light"
