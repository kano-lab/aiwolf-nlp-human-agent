from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path
from typing import TYPE_CHECKING

from PIL import Image
from textual.app import ComposeResult
from textual.containers import Container, HorizontalGroup, VerticalGroup
from textual.screen import Screen
from textual.widgets import Input, Label, RichLog, Static, LoadingIndicator
from rich_pixels import Pixels

from player.agent import Agent
from utils.agent_log import AgentLog
from utils.log_info import LogInfo

if TYPE_CHECKING:
    from aiwolf_nlp_common.client import Client

from aiwolf_nlp_common.client.websocket import WebSocketClient

class GameScreen(Screen):
    CSS_PATH = "game.tcss"
    IMAGE_PATH = "./src/res/images/seer.png"

    def __init__(self, user_name: str):
        self._agent_initialize(user_name=user_name)

        self.image = Image.open(self.IMAGE_PATH)
        self.image = Pixels.from_image(self.image)

        super().__init__()

    def _agent_initialize(self, user_name: str) -> None:
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
    
    def _create_detail_label(self, key:str, value:str) -> Label:
        return Label(f"[u][b]{key}: [/b]{value}", classes="detail_info_label")

    def compose(self) -> ComposeResult:
        yield HorizontalGroup(
            VerticalGroup(
                Label("[bold]・会話履歴", id="history_log_label"),
                RichLog(markup=True, id="history_log"),
                id="history_container",
            ),
            Container(
                Label(id="image"),
                Container(
                    self._create_detail_label(key="プレイヤー名", value=self.agent.name),
                    self._create_detail_label(key="Agent名", value=self.agent.index),
                    self._create_detail_label(key="役職", value="占い師"),
                    id="detail_info_container"
                ),
                id="player_info_container"
            ),
            id="info_container",
        )
        yield Container(Input(id="text_input"), id="text_container")

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

        self.query_one("#image",Static).update(self.image)
