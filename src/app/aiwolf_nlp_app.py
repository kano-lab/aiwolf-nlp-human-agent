from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path

from aiwolf_nlp_common.client.websocket import WebSocketClient
from PIL import Image
from rich_pixels import Pixels
from textual import work
from textual.app import App, ComposeResult
from textual.containers import Container, HorizontalGroup, VerticalGroup
from textual.widgets import Input, Label

from app.widgets import AIwolfNLPLog, MapLabel
from player.agent import Agent
from utils.agent_log import AgentLog
from utils.log_info import LogInfo

from .screen.title import TitleScreen, TitleScreenResult

from textual.worker import Worker, get_current_worker


class AIWolfNLPApp(App):
    SCREENS = {"start": TitleScreen}
    CSS_PATH = "app.tcss"
    IMAGE_PATH = "./src/res/images/seer.png"

    def __init__(self):
        self.image = Image.open(self.IMAGE_PATH)
        self.image = Pixels.from_image(self.image)

        super().__init__()
    
    def _on_mount(self, event):
        def check_select(result: TitleScreenResult) -> None:
            if result.is_start:
                self.execute(user_name=result.user_name)
            elif result.is_exit:
                self.app.exit()

        self.push_screen("start", check_select)
    
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
                    self._create_detail_label(
                        key="プレイヤー名",
                        value="???",
                        id="player_name_info",
                    ),
                    self._create_detail_label(key="Agent名", value="???", id="agent_name_info"),
                    self._create_detail_label(key="役職", value="???"),
                    id="detail_info_container",
                ),
                id="player_info_container",
            ),
            id="info_container",
        )
        yield Container(Input(id="text_input"), id="text_container")

    def _app_exit(self, log: AIwolfNLPLog, error_message: str = "") -> None:
        worker = get_current_worker()

        if error_message:
            self.call_from_thread(lambda: log.add_system_message(message=error_message, error=True))
        
        self.call_from_thread(lambda: log.add_system_message(message=f"{5}秒後にアプリを終了します。", error=True))
        self.call_from_thread(log.update)
        self.call_from_thread(lambda: self.set_timer(delay=5, callback=lambda: self.app.exit(return_code=-1)))

    @work(exclusive=True, thread=True)
    def _run_agent(self, log: AIwolfNLPLog, user_name:str):

        try:
            self._game_initialize(user_name=user_name)
            self._connect(log=log)
        except Exception as e:
            self._app_exit(log=log, error_message=str(e))
            return

        while self.agent.running:
            pass

    def _create_detail_label(self, key: str, value: str, id: str | None = None) -> MapLabel:
        return MapLabel(
            key=key,
            value=value,
            id=id,
            classes="detail_info_label",
            bold=True,
            underline=True,
        )

    def _game_initialize(self, user_name:str) -> None:
        config_path = "./src/res/config.ini"

        if Path(config_path).exists():
            config = ConfigParser()
            config.read(config_path)
        else:
            raise FileNotFoundError(f'"{config_path}"に設定ファイルが見つかりません')

        log_info = LogInfo()

        self.client: WebSocketClient = WebSocketClient(
            url=config.get("websocket", "url"),
        )

        self.agent = Agent(
            name=user_name,
            agent_log=AgentLog(config=config, agent_name=user_name, log_info=log_info),
        )

        self.query_one("#player_name_info", MapLabel).update_value(value=self.agent.name)

    def _connect(self, log: AIwolfNLPLog) -> None:
        worker = get_current_worker()

        try:
            self.client.connect()
            if not worker.is_cancelled:
                self.call_from_thread(lambda: log.add_system_message(message="ゲームサーバに接続しました!", success=True))
                self.call_from_thread(log.update)
        except ConnectionRefusedError:
            raise ConnectionRefusedError("ゲームサーバへの接続に失敗しました。")
        
    def execute(self, user_name:str) -> None:
        log: AIwolfNLPLog = self.query_one("#history_log", AIwolfNLPLog)

        self._run_agent(log=log, user_name=user_name)

        text = """
            Agent[01]: こんにちは！
            Agent[02]: こんにちは！

            [bold blue u]夜になりました！:zzz:[/bold blue u]:zzz:

            [bold red u]接続が途切れました。[/bold red u]
        """

        # log.add_message(text)

        # log.update()

        self.query_one("#image", Label).update(self.image)