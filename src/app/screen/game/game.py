from __future__ import annotations

from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, HorizontalGroup, VerticalGroup
from textual.widgets import Input, Button, Label, Log
from pathlib import Path
from utils.log_info import LogInfo
from utils.agent_log import AgentLog
from player.agent import Agent

from configparser import ConfigParser
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiwolf_nlp_common.client import Client

from aiwolf_nlp_common.client.websocket import WebSocketClient


class GameScreen(Screen):
    def __init__(self, user_name: str):
        self.agent_initialize(user_name=user_name)
        super().__init__()

    def agent_initialize(self, user_name: str) -> None:
        config_path = "./src/res/config.ini"

        if Path(config_path).exists():
            config = ConfigParser()
            config.read(config_path)
        else:
            self.app.exit(return_code=-1, message="設定ファイルが見つかりません")

        log_info = LogInfo()

        self.client: Client = WebSocketClient(
            url=config.get("websocket", "url"),
        )

        self.agent = Agent(
            name=user_name,
            agent_log=AgentLog(config=config, agent_name=user_name, log_info=log_info),
        )

    def compose(self) -> ComposeResult:
        yield HorizontalGroup(
            Label(f"プレイヤー名:{self.agent.name}"),
            Label(f"Agent名: {self.agent.index}"),
        )
        yield VerticalGroup(
            Label("会話履歴"),
            Log()
        )
    
    def _on_mount(self, event):
        log = self.query_one(Log)
        log.write_line("ゲームサーバに接続しました!")

