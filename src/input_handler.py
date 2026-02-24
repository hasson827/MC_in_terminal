"""
输入处理模块。

处理游戏控制的键盘输入。
"""

import curses
from typing import Set


class InputHandler:
    """
    键盘输入处理器。
    """

    def __init__(self, stdscr: curses.window):
        """
        初始化输入处理器。

        参数：
            stdscr: curses 窗口，用于读取输入
        """
        self.stdscr = stdscr
        self.keystate: Set[int] = set()
        self._should_quit = False

    def process_input(self):
        """
        处理所有待处理的键盘输入。

        清除之前的状态并读取当前所有按键。
        """
        # 清除之前的按键状态
        self.keystate.clear()

        # 读取所有待处理输入
        while True:
            try:
                key = self.stdscr.getch()
                if key == -1:
                    break  # 无更多输入

                # 处理 q 键退出
                if key == ord("q") or key == ord("Q"):
                    self._should_quit = True

                self.keystate.add(key)

            except curses.error:
                break

    def is_key_pressed(self, key: str) -> bool:
        """
        检查按键是否被按下。

        参数：
            key: 单字符按键

        返回：
            如果按键被按下返回 True
        """
        return ord(key) in self.keystate

    def is_keycode_pressed(self, keycode: int) -> bool:
        """
        检查键码是否被按下。

        参数：
            keycode: 键码

        返回：
            如果键码被按下返回 True
        """
        return keycode in self.keystate

    def should_quit(self) -> bool:
        """检查是否请求退出。"""
        return self._should_quit

    def reset_quit(self):
        """重置退出标志。"""
        self._should_quit = False


# 按键常量
KEY_QUIT = ord("q")
KEY_LOOK_UP = ord("w")
KEY_LOOK_DOWN = ord("s")
KEY_LOOK_LEFT = ord("a")
KEY_LOOK_RIGHT = ord("d")
KEY_MOVE_FORWARD = ord("i")
KEY_MOVE_BACKWARD = ord("k")
KEY_STRAFE_LEFT = ord("j")
KEY_STRAFE_RIGHT = ord("l")
KEY_REMOVE_BLOCK = ord("x")
KEY_PLACE_BLOCK = ord(" ")  # 空格键
