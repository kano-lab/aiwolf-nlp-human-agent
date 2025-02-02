from __future__ import annotations

from textual.widgets import Label


class MapLabel(Label):
    def __init__(
        self,
        key: str,
        value: str,
        id: str | None = None,
        classes: str | None = None,
        *,
        bold: bool = False,
        underline: bool = False,
    ) -> None:
        self.key: str = key
        self.value: str = value
        self.bold: bool = bold
        self.underline: bool = underline

        super().__init__(str(self), id=id, classes=classes)

    def __str__(self) -> str:
        text = "・"
        key_text = f"{self.key}: "
        value_text = self.value

        if self.bold:
            key_text = f"[b]{key_text}[/b]"

        if self.underline:
            text = text + "[u] "

        return text + key_text + value_text

    def update_key(self, key: str) -> None:
        self.key = key
        self.update(str(self))

    def update_value(self, value: str) -> None:
        self.value = value
        self.update(str(self))
