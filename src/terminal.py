"""
终端控制模块。

使用 curses 处理终端初始化和恢复。
"""

import curses
from typing import Optional


class Terminal:
    """
    终端控制器，使用 curses 实现非阻塞输入。
    """

    def __init__(self):
        """初始化终端控制器。"""
        self.stdscr: Optional[curses.window] = None
        self.initialized = False

    def init_terminal(self) -> curses.window:
        """
        初始化终端为非阻塞输入模式。

        返回：
            curses 窗口对象
        """
        self.stdscr = curses.initscr()

        # 禁用行缓冲
        curses.noecho()
        curses.cbreak()

        # 不需要按回车键
        self.stdscr.nodelay(True)

        # 隐藏光标
        curses.curs_set(0)

        # 启用键盘特殊键
        self.stdscr.keypad(True)

        self.initialized = True

        return self.stdscr

    def restore_terminal(self):
        """恢复终端到原始状态。"""
        if self.initialized and self.stdscr:
            # 显示光标
            curses.curs_set(1)

            # 恢复终端设置
            curses.nocbreak()
            self.stdscr.keypad(False)
            curses.echo()
            curses.endwin()

            self.initialized = False
            print("终端已恢复")

    def get_stdscr(self) -> Optional[curses.window]:
        """获取 curses 窗口。"""
        return self.stdscr

    def clear_screen(self):
        """清空终端屏幕。"""
        if self.stdscr:
            self.stdscr.clear()

    def refresh(self):
        """刷新终端显示。"""
        if self.stdscr:
            self.stdscr.refresh()


# 全局终端实例
_terminal_instance: Optional[Terminal] = None


def get_terminal() -> Terminal:
    """获取或创建全局终端实例。"""
    global _terminal_instance
    if _terminal_instance is None:
        _terminal_instance = Terminal()
    return _terminal_instance


def init_terminal() -> curses.window:
    """初始化终端并返回 curses 窗口。"""
    term = get_terminal()
    return term.init_terminal()


def restore_terminal():
    """恢复终端到原始状态。"""
    term = get_terminal()
    term.restore_terminal()
