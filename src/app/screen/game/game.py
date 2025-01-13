from __future__ import annotations

from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, HorizontalGroup, VerticalGroup
from textual.widgets import Input, Button, Label, RichLog
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
    CSS_PATH = "game.tcss"

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
            Label("会話履歴", id="history_log_label"),
            RichLog(markup=True, id="history_log"),
            id="history_container"
        )
        yield Container(
            Input(id="text_input"),
            id="text_container"
        )
    
    def _on_mount(self, event):
        rich_log = self.query_one(RichLog)

        text = """
            [bold green u]ゲームサーバに接続しました![/bold green u]

            Agent[01]: こんにちは！
            Agent[02]: こんにちは！

            [bold blue u]夜になりました！:zzz:[/bold blue u]:zzz:

            [bold red u]接続が途切れました。[/bold red u]
        """

        rich_log.write(text)

