"""
Minecraft 终端版 - 主程序入口。

基于 ASCII 光线追踪的终端 3D Minecraft 游戏。
"""

import time
import sys
from src.config import FRAME_DELAY_MS
from src.world import World
from src.player import Player
from src.raycast import Raycaster
from src.renderer import Renderer
from src.input_handler import InputHandler
from src.terminal import init_terminal, restore_terminal


class Game:
    """
    游戏主类，协调所有子系统。
    """

    def __init__(self):
        """初始化游戏组件。"""
        self.world = World()
        self.player = Player(x=10.0, y=10.0)
        self.raycaster = Raycaster()
        self.renderer = Renderer(self.raycaster, self.world)
        self.input_handler = None
        self.stdscr = None
        self.running = True

    def setup(self):
        """设置游戏环境。终端初始化和世界生成。"""
        # 初始化终端
        self.stdscr = init_terminal()
        self.input_handler = InputHandler(self.stdscr)

        # 生成地面
        self.world.generate_ground(ground_height=4)

        print("游戏初始化完成！按 q 退出")

    def cleanup(self):
        """清理游戏资源，恢复终端。"""
        restore_terminal()

    def run(self):
        """主游戏循环。"""
        self.setup()

        try:
            while self.running:
                frame_start = time.time()

                # 处理输入
                self.input_handler.process_input()

                # 检查退出
                if self.input_handler.should_quit():
                    self.running = False
                    break

                # 更新游戏状态
                self.player.update(self.world, self.input_handler)

                # 处理方块交互
                player_pos = self.player.get_pos()
                player_dir = self.player.get_direction()
                blocks = self.world.blocks

                target = self.raycaster.get_current_block_pos(
                    player_pos, player_dir, blocks
                )

                if target:
                    bx, by, bz = int(target.x), int(target.y), int(target.z)
                    if self.input_handler.is_key_pressed("x"):
                        self.world.remove_block(bx, by, bz)
                    if self.input_handler.is_key_pressed(" "):
                        self.world.place_block(target, "@")

                # 渲染
                picture = self.renderer.get_picture(
                    player_pos, self.player.get_view(), player_dir
                )
                self.renderer.draw_ascii(picture, self.stdscr)

                # 帧率控制
                frame_time = (time.time() - frame_start) * 1000
                delay = max(0, FRAME_DELAY_MS - frame_time) / 1000
                time.sleep(delay)

        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()

    def print_controls(self):
        """打印控制说明。"""
        print("\n=== Minecraft 终端版 ===")
        print("控制:")
        print("  w/s/a/d - 视角旋转")
        print("  i/k/j/l - 移动 (前/后/左/右)")
        print("  x       - 移除方块")
        print("  空格    - 放置方块")
        print("  q       - 退出")
        print("========================\n")


def main():
    """程序入口。"""
    game = Game()
    game.print_controls()

    try:
        game.run()
    except Exception as e:
        print(f"\n游戏错误: {e}")
        restore_terminal()
        sys.exit(1)


if __name__ == "__main__":
    main()
