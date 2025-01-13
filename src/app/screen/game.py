from __future__ import annotations

from textual.app import ComposeResult
from textual.screen import Screen
from pathlib import Path
from utils.log_info import LogInfo

from configparser import ConfigParser
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiwolf_nlp_common.client import Client

from aiwolf_nlp_common.client.websocket import WebSocketClient


class Game(Screen):
    def _on_mount(self, event) -> None:
        config_path = "./src/res/config.ini"

        if Path(config_path).exists():
            config = ConfigParser()
            config.read(config_path)
        else:
            self.app.exit(return_code=-1, message="設定ファイルが見つかりません")

        log_info = LogInfo()

        client: Client = WebSocketClient(
            url=config.get("websocket", "url"),
        )

        return super()._on_mount(event)
