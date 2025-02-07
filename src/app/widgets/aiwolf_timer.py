from textual.widgets import Digits, Static
from textual.events import Timer
from rich.spinner import Spinner


class AIWolfNLPTimer(Digits):
    _spinner = Spinner("arc")
    spinner_update_manager: Timer | None = None
    action_timeout: int | None = None
    timer_update_manager: Timer | None = None
    display_time: int | None = None

    def __init__(
        self,
        value: str = "",
        *,
        name: str = None,
        id: str = None,
        classes: str = None,
        disabled: bool = False,
    ):
        super().__init__(value, name=name, id=id, classes=classes, disabled=disabled)

    def _on_mount(self, event):
        self.start_spinner()

    def set_action_timeout(self, action_timeout: int) -> None:
        self.action_timeout = action_timeout

    def start_timer(self) -> None:
        if self.action_timeout is None:
            raise ValueError("action_timeout is not set.")

        if self.spinner_update_manager is not None:
            self.spinner_update_manager.stop()
            self.remove_children()
            self.spinner_update_manager = None

        self.disabled = False
        self.display_time = self.action_timeout
        self.timer_update_manager = self.set_interval(
            interval=1, callback=self._update_timer, repeat=self.action_timeout
        )

    def start_spinner(self) -> None:
        if self.timer_update_manager is not None:
            self.timer_update_manager.stop()
            self.update("")
            self.timer_update_manager = None

        self.disabled = True
        self.mount(Static("", id="spinner"))
        self.spinner_update_manager = self.set_interval(
            interval=1 / 60, callback=self._update_spinner
        )

    def _update_timer(self) -> None:
        if self.display_time < 0:
            return

        self.display_time -= 1
        self.update(str(self.display_time))

    def _update_spinner(self) -> None:
        self.query_one(Static).update(self._spinner)
