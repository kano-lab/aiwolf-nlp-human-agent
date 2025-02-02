from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path

import asyncio
from aiwolf_nlp_common.client.websocket import WebSocketClient
from PIL import Image
from rich_pixels import Pixels
from textual import work
from textual.app import ComposeResult
from textual.containers import Container, HorizontalGroup, VerticalGroup
from textual.screen import Screen
from textual.widgets import Input, Label

from app.widgets import AIwolfNLPLog
from player.agent import Agent
from utils.agent_log import AgentLog
from utils.log_info import LogInfo

import time
from time import sleep as time_sleep
from asyncio import get_running_loop


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

        self.client: WebSocketClient = WebSocketClient(
            url=config.get("websocket", "url"),
        )

        self.agent = Agent(
            name=user_name,
            agent_log=AgentLog(config=config, agent_name=user_name, log_info=log_info),
        )

    @work(exclusive=True, thread=True)
    def _agent_listen():
        pass

    def _create_detail_label(self, key: str, value: str) -> Label:
        return Label(f"・[u][b]{key}: [/b]{value}", classes="detail_info_label")

    def compose(self) -> ComposeResult:
        yield HorizontalGroup(
            VerticalGroup(
                Label("[bold]・会話履歴", id="history_log_label"),
                AIwolfNLPLog(markup=True, id="history_log"),
                id="history_container",
            ),
            Container(
                Label(id="image"),
                Container(
                    self._create_detail_label(key="プレイヤー名", value=self.agent.name),
                    self._create_detail_label(key="Agent名", value=self.agent.index),
                    self._create_detail_label(key="役職", value="占い師"),
                    id="detail_info_container",
                ),
                id="player_info_container",
            ),
            id="info_container",
        )
        yield Container(Input(id="text_input"), id="text_container")

    def agent_connect(self, log: AIwolfNLPLog) -> bool:
        is_success:bool = True

        try:
            self.client.connect()
            log.add_system_message(message="ゲームサーバに接続しました!", success=True)
        except:
            log.add_system_message(message="ゲームサーバへの接続に失敗しました。", error=True)
            is_success = False
        finally:
            log.update()
        
        return is_success
    
    def app_exit(self, log: AIwolfNLPLog) -> None:
        log.add_system_message(message=f"{1}秒後にアプリを終了します。", error=True)
        self.set_timer(delay=3, callback=self.app.exit)

    def _on_mount(self, event):
        log: AIwolfNLPLog = self.query_one("#history_log", AIwolfNLPLog)

        if not self.agent_connect(log=log):
            self.app_exit(log=log)
            return

        text = """
            Agent[01]: こんにちは！
            Agent[02]: こんにちは！

            [bold blue u]夜になりました！:zzz:[/bold blue u]:zzz:

            [bold red u]接続が途切れました。[/bold red u]
        """

        log.add_message(text)

        for i in range(10):
            log.add_system_message(message="ゲームサーバに接続しました!", success=True)

        log.add_system_message(message="ゲームサーバに接続しました!", night=True)

        log.update()

        self.query_one("#image", Label).update(self.image)
