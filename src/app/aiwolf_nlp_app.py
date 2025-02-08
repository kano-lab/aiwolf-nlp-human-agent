from __future__ import annotations

import threading
from configparser import ConfigParser
from pathlib import Path

from aiwolf_nlp_common.action import Action
from aiwolf_nlp_common.client.websocket import WebSocketClient
from PIL import Image
from rich_pixels import Pixels
from textual import work
from textual.app import App, ComposeResult
from textual.containers import Container, HorizontalGroup, VerticalGroup
from textual.widgets import Button, Input, Label, Digits
from textual.worker import get_current_worker

from app.widgets import AIWolfNLPInputGroup, AIwolfNLPLog, MapLabel, AIWolfNLPTimer
from player.agent import Agent
from utils.agent_log import AgentLog
from utils.log_info import LogInfo

from .debug_setting import DebugSetting
from .screen.title import TitleScreen, TitleScreenResult
from .screen.vote import VoteScreen


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
        self.prev_divine_result: str | None = None
        self.button_pressed_event = threading.Event()

        self.debug_setting: DebugSetting = DebugSetting(auto_talk=False, auto_vote=False)

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
                HorizontalGroup(
                    Label("[bold]・会話履歴", id="history_log_label"),
                    AIWolfNLPTimer(id="timer"),
                    id="label_timer",
                ),
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
        yield AIWolfNLPInputGroup(id="input_container", disabled=True)

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
        # user_name = "kanolab5"
        self.query_one("#image", Label).update(self.image)

        try:
            client, agent = self.call_from_thread(
                callback=lambda: self._game_initialize(user_name=user_name),
            )
            self.call_from_thread(callback=lambda: self._connect(client=client, log=log))
        except Exception as e:
            self._app_exit(log=log, error_message=str(e))
            return

        while agent.running:
            if len(agent.received) == 0:
                receive = client.receive()
                if isinstance(receive, (str, list)):
                    agent.append_recv(recv=receive)
            agent.set_packet()
            if agent.packet is None:
                continue

            req = self.agent_action(agent=agent, log=log)

            if Action.is_initialize(request=agent.packet.request):
                self.call_from_thread(
                    callback=lambda: self.query_one("#agent_name_info", MapLabel).update_value(
                        value=agent.info.agent,
                    ),
                )
                self.call_from_thread(
                    callback=lambda: self.query_one("#agent_role_info", MapLabel).update_value(
                        value=agent.role.ja,
                    ),
                )

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
                log.add_system_message(
                    message="ゲームサーバに接続しました!",
                    success=True,
                )
        except ConnectionRefusedError:
            raise ConnectionRefusedError("ゲームサーバへの接続に失敗しました。")

    def agent_action(self, agent: Agent, log: AIwolfNLPLog) -> str:
        message: str = ""

        if Action.is_talk(request=agent.packet.request):
            if (
                not agent.packet.info.divine_result.is_empty()
                and self.prev_divine_result != agent.packet.info.divine_result.result
            ):
                self.call_from_thread(
                    callback=lambda: log.add_system_message(
                        message=f"占いの結果、{agent.packet.info.divine_result.target}は{agent.packet.info.divine_result.result}でした。"
                    )
                )
                self.prev_divine_result = agent.packet.info.divine_result.result

            self.call_from_thread(
                callback=lambda: self.query_one("#timer", AIWolfNLPTimer).start_timer()
            )
            self.call_from_thread(
                callback=lambda: log.update_talk_history(talk_history=agent.packet.talk_history),
            )
            self.call_from_thread(
                callback=lambda: self.query_one("#input_container", AIWolfNLPInputGroup).enable()
            )

            if not self.debug_setting.automatic_talk:
                message = self._wait_input()

            self.call_from_thread(
                callback=lambda: self.query_one("#timer", AIWolfNLPTimer).start_spinner()
            )
        elif Action.is_vote(request=agent.packet.request) and not self.debug_setting.automatic_vote:
            vote_target = self.call_from_thread(
                callback=lambda: self.push_screen_wait(VoteScreen(agent=agent, vote=True)),
            )
            self.call_from_thread(
                callback=lambda: log.add_system_message(
                    message=f"{vote_target}に投票しました",
                    success=True,
                ),
            )
            message = vote_target
        elif (
            Action.is_divine(request=agent.packet.request)
            and not self.debug_setting.automatic_divine
        ):
            divine_target = self.call_from_thread(
                callback=lambda: self.push_screen_wait(
                    VoteScreen(
                        agent=agent,
                        divine=True,
                    ),
                ),
            )
            self.call_from_thread(
                callback=lambda: log.add_system_message(
                    message=f"{divine_target}を占いました",
                    success=True,
                ),
            )
            message = divine_target
        elif (
            Action.is_attack(request=agent.packet.request)
            and not self.debug_setting.automatic_attack
        ):
            attack_target = self.call_from_thread(
                callback=lambda: self.push_screen_wait(
                    VoteScreen(
                        agent=agent,
                        attack=True,
                    ),
                ),
            )
            self.call_from_thread(
                callback=lambda: log.add_system_message(
                    message=f"{attack_target}を襲撃します",
                    success=True,
                ),
            )
            message = attack_target
        elif Action.is_initialize(request=agent.packet.request):
            self.call_from_thread(
                callback=lambda: self.query_one("#timer", AIWolfNLPTimer).set_action_timeout(
                    action_timeout=agent.packet.setting.action_timeout
                )
            )
        elif Action.is_daily_initialize(request=agent.packet.request):
            self.call_from_thread(callback=lambda: log.daily_initialize())

            if agent.info.executed_agent is not None:
                self.call_from_thread(
                    callback=lambda: log.add_system_message(
                        message=f"{agent.info.executed_agent}が投票により処刑されました。",
                        error=True,
                    )
                )

            if agent.info.attacked_agent is not None:
                self.call_from_thread(
                    callback=lambda: log.add_system_message(
                        message=f"{agent.info.attacked_agent}が人狼に襲われました。", error=True
                    )
                )

        elif Action.is_daily_finish(request=agent.packet.request):
            self.call_from_thread(
                callback=lambda: log.add_system_message(
                    message="夜になりました！:zzz:", night=True
                ),
            )

        if not message:
            self.call_from_thread(
                callback=lambda: self.query_one("#input_container", AIWolfNLPInputGroup).disable(),
            )
            message = agent.action()

        return message

    def _wait_input(self) -> str:
        while True:
            self.button_pressed_event.wait()
            self.button_pressed_event.clear()

            if self.query_one("#comment_field", Input).value:
                break

            self.query_one("#input_container", AIWolfNLPInputGroup).set_empty_class()

        input_content: str = self.query_one("#comment_field", Input).value
        self.query_one("#comment_field", Input).clear()
        self.query_one("#input_container", AIWolfNLPInputGroup).set_normal_class()

        return input_content

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "send_button":
            self.button_pressed_event.set()
