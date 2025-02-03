from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path

from aiwolf_nlp_common.action import Action
from aiwolf_nlp_common.client.websocket import WebSocketClient
from PIL import Image
from rich_pixels import Pixels
from textual import work
from textual.app import App, ComposeResult
from textual.containers import Container, HorizontalGroup, VerticalGroup
from textual.widgets import Label
from textual.worker import get_current_worker

from app.widgets import AIWolfNLPInput, AIwolfNLPLog, MapLabel
from player.agent import Agent
from utils.agent_log import AgentLog
from utils.log_info import LogInfo

from .screen.title import TitleScreen, TitleScreenResult


def create_detail_label(key: str, value: str, id: str | None = None) -> MapLabel:
    return MapLabel(
        key=key,
        value=value,
        id=id,
        classes="detail_info_label",
        bold=True,
        underline=True,
    )


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
                self._run_agent(user_name=result.user_name)
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
                    create_detail_label(
                        key="プレイヤー名",
                        value="???",
                        id="player_name_info",
                    ),
                    create_detail_label(key="Agent名", value="???", id="agent_name_info"),
                    create_detail_label(key="役職", value="???", id="agent_role_info"),
                    id="detail_info_container",
                ),
                id="player_info_container",
            ),
            id="info_container",
        )
        yield Container(AIWolfNLPInput(disabled=True, id="text_input"), id="text_container")

    def _app_exit(self, log: AIwolfNLPLog, error_message: str = "") -> None:
        worker = get_current_worker()

        if error_message and not worker.is_cancelled:
            self.call_from_thread(lambda: log.add_system_message(message=error_message, error=True))

        if not worker.is_cancelled:
            self.call_from_thread(
                lambda: log.add_system_message(
                    message=f"{5}秒後にアプリを終了します。",
                    error=True,
                ),
            )
            self.call_from_thread(
                lambda: self.set_timer(delay=5, callback=lambda: self.app.exit(return_code=-1)),
            )

    @work(exclusive=True, thread=True)
    def _run_agent(self, user_name: str):
        log: AIwolfNLPLog = self.query_one("#history_log", AIwolfNLPLog)
        user_name = "kanolab5"
        self.query_one("#image", Label).update(self.image)

        try:
            client, agent = self._game_initialize(user_name=user_name)
            self._connect(client=client, log=log)
        except Exception as e:
            self._app_exit(log=log, error_message=str(e))
            return

        while agent.running:
            if len(agent.received) == 0:
                receive = client.receive()
                if isinstance(receive, (str, list)):
                    agent.append_recv(recv=receive)
            agent.set_packet()
            req = agent.action()
            if agent.packet is None:
                continue

            if Action.is_initialize(request=agent.packet.request):
                self.query_one("#agent_name_info", MapLabel).update_value(value=agent.info.agent)
                self.query_one("#agent_role_info", MapLabel).update_value(value=agent.role.ja)
            elif Action.is_talk(request=agent.packet.request):
                self.query_one("#text_input", AIWolfNLPInput).enable()

            if req != "":
                client.send(req=req)

        self._app_exit(log=log, error_message="正常に終わっちゃった！！！！！！！！！！！！")

    def _game_initialize(self, user_name: str) -> tuple[WebSocketClient, Agent]:
        config_path = "./src/res/config.ini"

        if Path(config_path).exists():
            config = ConfigParser()
            config.read(config_path)
        else:
            raise FileNotFoundError(f'"{config_path}"に設定ファイルが見つかりません')

        log_info = LogInfo()

        client: WebSocketClient = WebSocketClient(
            url=config.get("websocket", "url"),
        )

        agent = Agent(
            name=user_name,
            agent_log=AgentLog(config=config, agent_name=user_name, log_info=log_info),
        )

        self.query_one("#player_name_info", MapLabel).update_value(value=agent.name)

        return client, agent

    def _connect(self, client: WebSocketClient, log: AIwolfNLPLog) -> None:
        worker = get_current_worker()

        try:
            client.connect()
            if not worker.is_cancelled:
                self.call_from_thread(
                    lambda: log.add_system_message(
                        message="ゲームサーバに接続しました!",
                        success=True,
                    ),
                )
        except ConnectionRefusedError:
            raise ConnectionRefusedError("ゲームサーバへの接続に失敗しました。")

    def execute(self) -> None:
        text = """
            Agent[01]: こんにちは！
            Agent[02]: こんにちは！

            [bold blue u]夜になりました！:zzz:[/bold blue u]:zzz:

            [bold red u]接続が途切れました。[/bold red u]
        """
