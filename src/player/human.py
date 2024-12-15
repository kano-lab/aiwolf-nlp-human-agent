from __future__ import annotations

import curses
import re
import time
from typing import TYPE_CHECKING

from .agent import Agent

if TYPE_CHECKING:
    from aiwolf_nlp_common.role import Role


class Human(Agent):
    def __init__(self, name=None, agent_log=None) -> None:
        super().__init__(name, agent_log)

    def timeout_input(self, stdscr: curses.window) -> str:
        start_time = time.time()
        max_y, max_x = stdscr.getmaxyx()

        # 描画箇所
        y_pos = 0
        x_pos = 0

        # 前の表示を削除
        stdscr.clear()
        stdscr.refresh()

        stdscr.addstr(0, 0, "Remain Time:" + str(self.action_timeout))
        y_pos += 1
        y_pos += 1

        stdscr.addstr(y_pos, 0, "===== Game Info =====")
        y_pos += 1
        stdscr.addstr(y_pos, 0, "You are " + self.info.agent + ".")
        y_pos += 1

        stdscr.addstr(y_pos, 0, "Your role is " + self.role + ".")
        y_pos += 1

        stdscr.addstr(y_pos, 0, "Action: " + self.packet.request + ".")
        y_pos += 1

        if self.info is not None and not self.info.divine_result.is_empty():
            y_pos += 1

            stdscr.addstr(y_pos, 0, "===== Divine Result =====")
            y_pos += 1
            stdscr.addstr(
                y_pos,
                0,
                self.info.divine_result.target + " is " + self.info.divine_result.result,
            )
            y_pos += 1
            y_pos += 1

        y_pos = self.output_talk_history(stdscr=stdscr, y_pos=y_pos)
        is_back = is_input = False
        is_y_decrement = False

        # 見えやすくするために1行開ける
        y_pos += 1

        input_start_pos = y_pos
        input_prompt = "input message >>:"

        stdscr.addstr(input_start_pos, 0, input_prompt)
        x_pos = len(input_prompt)

        curses.curs_set(1)  # カーソルを表示
        stdscr.timeout(1000)  # getchの上限を設定

        input_text = []

        while True:
            current_time = time.time()
            elapsed_time = (int)(current_time - start_time)
            remain_time = self.action_timeout - elapsed_time

            stdscr.addstr(0, 0, "Remain Time:" + str(remain_time))
            stdscr.addstr(input_start_pos, 0, input_prompt)

            if is_y_decrement:
                stdscr.move(y_pos, max_x - 1)  # カーソルの位置を調整
            else:
                stdscr.move(y_pos, x_pos)  # カーソルの位置を調整

            is_back = is_input = False
            is_y_decrement = False

            key = stdscr.getch()  # 1文字ずつキーを取得

            if key == -1:
                continue

            if key == 10 and len(input_text) == 0:
                continue

            if key == 10:  # Enterキー (ASCIIコード10)
                break
            if key in (127, 8, curses.KEY_BACKSPACE):  # バックスペースキーの様々な可能性を考慮
                if input_text:
                    input_text.pop()
                    is_back = True
            else:
                input_text.append(chr(key))  # 入力されたキーを追加
                is_input = True

            write_start_pos = 0
            write_y_pos = input_start_pos
            one_line_chars = max_x - len(input_prompt)
            remain_text = len(input_text)
            write_text = []

            while remain_text > 0:
                write_end_pos = write_start_pos + one_line_chars
                write_text = input_text[write_start_pos:write_end_pos]
                stdscr.move(write_y_pos, 0)  # カーソルの位置を調整
                stdscr.clrtoeol()  # カーソルがある部分の入力部分をクリア
                stdscr.move(write_y_pos + 1, 0)  # カーソルの位置を調整
                stdscr.clrtoeol()  # カーソルがある部分の入力部分をクリア
                stdscr.addstr(write_y_pos, len(input_prompt), "".join(write_text))  # 入力を再描画

                remain_text -= len(write_text)
                write_start_pos = write_end_pos
                write_y_pos += 1

            if len(write_text) == one_line_chars - 1 and is_back:
                y_pos -= 1
                is_y_decrement = True
            elif len(write_text) == one_line_chars:
                x_pos = len(input_prompt)

                if is_input:
                    y_pos += 1
            else:
                x_pos = len(input_prompt) + len(write_text)

            if len(write_text) == 0:
                stdscr.move(input_start_pos, 0)  # カーソルの位置を調整
                stdscr.clrtoeol()  # カーソルがある部分の入力部分をクリア

            stdscr.refresh()

        return "".join(input_text)

    def timeout_numeric_input(self, stdscr: curses.window) -> int:
        start_time = time.time()
        max_y, max_x = stdscr.getmaxyx()

        # 描画箇所
        y_pos = 0
        x_pos = 0

        # 前の表示を削除
        stdscr.clear()
        stdscr.refresh()

        stdscr.addstr(0, 0, "Remain Time:" + str(self.action_timeout))
        y_pos += 1
        y_pos += 1

        stdscr.addstr(y_pos, 0, "===== Game Info =====")
        y_pos += 1
        stdscr.addstr(y_pos, 0, "You are " + self.info.agent + ".")
        y_pos += 1

        stdscr.addstr(y_pos, 0, "Your role is " + self.role + ".")
        y_pos += 1

        stdscr.addstr(y_pos, 0, "Action: " + self.packet.request + ".")
        y_pos += 1
        y_pos += 1

        stdscr.addstr(y_pos, 0, "===== Action Info =====")
        y_pos += 1

        stdscr.addstr(y_pos, 0, "Alive agent is " + ", ".join(self.alive_agents()) + ".")
        y_pos += 1

        stdscr.addstr(y_pos, 0, "Please enter only one number, such as “1” or “2”.")
        y_pos += 1

        # 見えやすくするために1行開ける
        y_pos += 1
        is_back = is_input = False
        is_y_decrement = False

        input_start_pos = y_pos
        input_prompt = "input message >>:"

        stdscr.addstr(input_start_pos, 0, input_prompt)
        x_pos = len(input_prompt)

        curses.curs_set(1)  # カーソルを表示
        stdscr.timeout(1000)  # getchの上限を設定

        input_text = []

        while True:
            current_time = time.time()
            elapsed_time = (int)(current_time - start_time)
            remain_time = self.action_timeout - elapsed_time

            stdscr.addstr(0, 0, "Remain Time:" + str(remain_time))
            stdscr.addstr(input_start_pos, 0, input_prompt)

            if is_y_decrement:
                stdscr.move(y_pos, max_x - 1)  # カーソルの位置を調整
            else:
                stdscr.move(y_pos, x_pos)  # カーソルの位置を調整

            is_back = is_input = False
            is_y_decrement = False

            key = stdscr.getch()  # 1文字ずつキーを取得

            if key == -1:
                continue

            if (
                key == 10
                and len(input_text) == 0
                and re.match(r".*[a-zA-Z\s\.\,]+", "".join(input_text))
            ):
                continue
            if key == 10 and len(input_text) != 0 and "".join(input_text).isdecimal():
                break
            if key in (127, 8, curses.KEY_BACKSPACE):  # バックスペースキーの様々な可能性を考慮
                if input_text:
                    input_text.pop()
                    is_back = True
            else:
                input_text.append(chr(key))  # 入力されたキーを追加
                is_input = True

            write_start_pos = 0
            write_y_pos = input_start_pos
            one_line_chars = max_x - len(input_prompt)
            remain_text = len(input_text)
            write_text = []

            while remain_text > 0:
                write_end_pos = write_start_pos + one_line_chars
                write_text = input_text[write_start_pos:write_end_pos]
                stdscr.move(write_y_pos, 0)  # カーソルの位置を調整
                stdscr.clrtoeol()  # カーソルがある部分の入力部分をクリア
                stdscr.move(write_y_pos + 1, 0)  # カーソルの位置を調整
                stdscr.clrtoeol()  # カーソルがある部分の入力部分をクリア
                stdscr.addstr(write_y_pos, len(input_prompt), "".join(write_text))  # 入力を再描画

                remain_text -= len(write_text)
                write_start_pos = write_end_pos
                write_y_pos += 1

            if len(write_text) == one_line_chars - 1 and is_back:
                y_pos -= 1
                is_y_decrement = True
            elif len(write_text) == one_line_chars:
                x_pos = len(input_prompt)

                if is_input:
                    y_pos += 1
            else:
                x_pos = len(input_prompt) + len(write_text)

            if len(write_text) == 0:
                stdscr.move(input_start_pos, 0)  # カーソルの位置を調整
                stdscr.clrtoeol()  # カーソルがある部分の入力部分をクリア

            stdscr.refresh()

        return int("".join(input_text))

    def output_talk_history(self, stdscr: curses.window, y_pos: int) -> int:
        max_y, max_x = stdscr.getmaxyx()

        # 見えやすくするための改行
        y_pos += 1

        stdscr.addstr(y_pos, 0, "====== Talk History =====")
        y_pos += 1

        if self.talk_history.is_empty():
            return y_pos

        for talk in self.talk_history:
            talk_display = talk.agent + " : " + talk.text

            stdscr.addstr(y_pos, 0, talk_display)

            y_pos += len(talk_display) // max_x + 1
            y_pos += 1

        return y_pos

    def append_recv(self, recv: str | list[str]) -> None:
        return super().append_recv(recv)

    def set_packet(self) -> None:
        return super().set_packet()

    def initialize(self) -> None:
        super().initialize()

        print("You are " + self.info.agent + ".")
        print("Your role is " + self.role + ".")

    def daily_initialize(self) -> None:
        return super().daily_initialize()

    def daily_finish(self) -> None:
        return super().daily_finish()

    def get_name(self) -> str:
        return super().get_name()

    def get_role(self) -> Role:
        return super().get_role()

    @Agent.timeout
    def talk(self) -> str:
        comment: str = curses.wrapper(self.timeout_input)

        if self.info is not None and not self.info.divine_result.is_empty():
            print("===== Divine Result =====")
            print(self.info.divine_result.target + " is " + self.info.divine_result.result)
            print()

            self.info.divine_result.reset()

        if self.talk_history.is_empty():
            return comment

        for talk in self.talk_history:
            talk_display = talk.agent + " : " + talk.text

            print(talk_display)

        return comment

    @Agent.timeout
    @Agent.send_agent_index
    def vote(self) -> int:
        vote_target: int = curses.wrapper(self.timeout_numeric_input)
        return vote_target

    @Agent.timeout
    @Agent.send_agent_index
    def divine(self) -> int:
        divine_target: int = curses.wrapper(self.timeout_numeric_input)
        return divine_target

    @Agent.timeout
    @Agent.send_agent_index
    def attack(self) -> int:
        attack_target: int = curses.wrapper(self.timeout_numeric_input)
        return attack_target

    @Agent.timeout
    def whisper(self) -> None:
        pass

    def finish(self) -> str:
        self.gameContinue = False

    def action(self) -> str:
        return super().action()

    def transfer_state(self, prev_agent: Agent) -> None:
        return super().transfer_state(prev_agent)

    def alive_agents(self) -> list[str]:
        return super().alive_agents()
