"""
渲染器模块。

将光线追踪结果转换为ASCII画面。
"""

from typing import List, TYPE_CHECKING
import curses
from .config import Y_PIXELS, X_PIXELS, HIGHLIGHT_BLOCK, EMPTY_BLOCK

if TYPE_CHECKING:
    from .raycast import Raycaster
    from .world import World


class Renderer:
    """
    ASCII渲染器，将3D世界渲染到终端。
    """

    def __init__(self, raycaster: "Raycaster", world: "World"):
        """
        初始化渲染器。

        参数：
            raycaster: 光线追踪器
            world: 世界实例
        """
        self.raycaster = raycaster
        self.world = world
        self.picture: List[List[str]] = [
            [EMPTY_BLOCK for _ in range(X_PIXELS)] for _ in range(Y_PIXELS)
        ]
        self._has_colors = False

    def get_picture(self, player_pos, player_view, player_direction) -> List[List[str]]:
        """
        渲染一帧画面。

        参数：
            player_pos: 玩家位置 Vector
            player_view: 玩家视角 Vector2
            player_direction: 玩家方向 Vector

        返回：
            渲染后的字符2D数组
        """
        directions = self.raycaster.init_directions(player_view)
        blocks = self.world.blocks

        # 获取高亮方块位置
        target = self.raycaster.get_current_block(player_pos, player_direction, blocks)

        for y in range(Y_PIXELS):
            for x in range(X_PIXELS):
                char = self.raycaster.raytrace(player_pos, directions[y][x], blocks)
                # 高亮玩家注视的方块
                if target and char != EMPTY_BLOCK and char != "-":
                    bx, by, bz = (
                        int(player_pos.x + 0.5),
                        int(player_pos.y + 0.5),
                        int(player_pos.z),
                    )
                    tx, ty, tz = target
                    # 检查当前像素是否在目标方块附近
                    px, py, pz = int(player_pos.x), int(player_pos.y), int(player_pos.z)
                    # 简化：用高亮字符替换击中方块的字符
                    if char == "@":
                        char = HIGHLIGHT_BLOCK
                self.picture[y][x] = char

        return self.picture

    def draw_ascii(self, picture: List[List[str]], stdscr: curses.window):
        """
        将画面绘制到终端。

        参数：
            picture: 字符2D数组
            stdscr: curses 窗口
        """
        if stdscr is None:
            return

        # 初始化颜色（仅首次）
        if not self._has_colors:
            try:
                curses.start_color()
                curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
                curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
                self._has_colors = True
            except:
                pass

        stdscr.clear()

        # 使用 has_colors 的缓存值
        if self._has_colors:
            for y, row in enumerate(picture):
                line = "".join(row)
                try:
                    stdscr.addstr(y, 0, line, curses.color_pair(1))
                except curses.error:
                    break
        else:
            for y, row in enumerate(picture):
                line = "".join(row)
                try:
                    stdscr.addstr(y, 0, line)
                except curses.error:
                    break

        stdscr.refresh()
