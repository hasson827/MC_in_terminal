"""
玩家模块。

处理玩家位置、视角、移动和物理。
"""

from typing import TYPE_CHECKING
from .config import X_BLOCKS, Y_BLOCKS, Z_BLOCKS, EYE_HEIGHT, MOVE_SPEED, TILT_SPEED
from .vector import Vector, Vector2, angles_to_vect

if TYPE_CHECKING:
    from .world import World
    from .input_handler import InputHandler


class Player:
    """
    玩家类，包含位置、视角和移动逻辑。
    """

    def __init__(self, x: float = 5.0, y: float = 5.0, z: float = None):
        """
        初始化玩家。

        参数：
            x: 初始 x 坐标
            y: 初始 y 坐标
            z: 初始 z 坐标（默认为地面高度 + 眼睛高度）
        """
        self.pos = Vector(x=x, y=y, z=z if z is not None else (4 + EYE_HEIGHT))
        self.view = Vector2(psi=0.0, phi=0.0)
        self._direction = angles_to_vect(self.view)  # 缓存方向向量

    def update(self, world: "World", input_handler: "InputHandler"):
        """
        根据输入和物理更新玩家位置和视角。

        参数：
            world: 世界实例，用于碰撞检测
            input_handler: 输入处理器，用于读取控制
        """
        self._apply_gravity(world)
        self._apply_collision(world)
        self._process_movement(input_handler)
        self._process_view(input_handler)

    def _apply_gravity(self, world: "World"):
        """应用重力 - 脚下无方块时下落。"""
        x, y = int(self.pos.x), int(self.pos.y)
        z_below = int(self.pos.z - EYE_HEIGHT - 0.01)

        if 0 <= z_below < Z_BLOCKS and world.is_empty(x, y, z_below):
            self.pos.z -= 1

    def _apply_collision(self, world: "World"):
        """处理碰撞 - 在方块内时向上推。"""
        x, y = int(self.pos.x), int(self.pos.y)
        z_at = int(self.pos.z - EYE_HEIGHT + 0.01)

        if 0 <= z_at < Z_BLOCKS and not world.is_empty(x, y, z_at):
            self.pos.z += 1

    def _process_movement(self, input_handler: "InputHandler"):
        """处理移动输入。"""
        dx = self._direction.x
        dy = self._direction.y

        if input_handler.is_key_pressed("i"):
            # 前进
            self.pos.x += MOVE_SPEED * dx
            self.pos.y += MOVE_SPEED * dy

        if input_handler.is_key_pressed("k"):
            # 后退
            self.pos.x -= MOVE_SPEED * dx
            self.pos.y -= MOVE_SPEED * dy

        if input_handler.is_key_pressed("j"):
            # 左移
            self.pos.x += MOVE_SPEED * dy
            self.pos.y -= MOVE_SPEED * dx

        if input_handler.is_key_pressed("l"):
            # 右移
            self.pos.x -= MOVE_SPEED * dy
            self.pos.y += MOVE_SPEED * dx

        # 限制在世界边界内
        self.pos.x = max(0.1, min(X_BLOCKS - 0.1, self.pos.x))
        self.pos.y = max(0.1, min(Y_BLOCKS - 0.1, self.pos.y))
        self.pos.z = max(EYE_HEIGHT, min(Z_BLOCKS - 0.1, self.pos.z))

    def _process_view(self, input_handler: "InputHandler"):
        """处理视角旋转输入。"""
        view_changed = False

        if input_handler.is_key_pressed("w"):
            self.view.psi += TILT_SPEED
            view_changed = True

        if input_handler.is_key_pressed("s"):
            self.view.psi -= TILT_SPEED
            view_changed = True

        if input_handler.is_key_pressed("d"):
            self.view.phi += TILT_SPEED
            view_changed = True

        if input_handler.is_key_pressed("a"):
            self.view.phi -= TILT_SPEED
            view_changed = True

        # 限制垂直视角
        self.view.psi = max(-1.5, min(1.5, self.view.psi))

        # 只在视角改变时更新缓存的方向向量
        if view_changed:
            self._direction = angles_to_vect(self.view)

    def get_direction(self) -> Vector:
        """获取当前视角方向向量。"""
        return self._direction

    def get_pos(self) -> Vector:
        """获取当前位置。"""
        return self.pos.copy()

    def get_view(self) -> Vector2:
        """获取当前视角角度。"""
        return self.view.copy()
