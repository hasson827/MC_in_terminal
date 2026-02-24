"""
光线追踪模块。

处理用于渲染的光线-世界相交检测。
"""

from typing import List, Optional, Tuple
from .config import (
    X_BLOCKS,
    Y_BLOCKS,
    Z_BLOCKS,
    X_PIXELS,
    Y_PIXELS,
    VIEW_HEIGHT,
    VIEW_WIDTH,
    BLOCK_BORDER_SIZE,
    RAY_EPSILON,
    EMPTY_BLOCK,
    BORDER_CHAR,
)
from .vector import Vector, Vector2, angles_to_vect


class Raycaster:
    """
    用于3D渲染的光线追踪引擎。
    """

    def __init__(self):
        """初始化光线追踪器。"""
        self.directions: Optional[List[List[Vector]]] = None
        self._cached_view: Optional[Vector2] = None  # 缓存视角用于方向复用

    def init_directions(self, view: Vector2) -> List[List[Vector]]:
        """
        计算所有屏幕像素的方向向量。

        参数：
            view: 当前视角角度

        返回：
            归一化方向向量的2D数组
        """
        # 视角未变时复用缓存
        if self._cached_view is not None and self.directions is not None:
            if (
                abs(self._cached_view.psi - view.psi) < 1e-6
                and abs(self._cached_view.phi - view.phi) < 1e-6
            ):
                return self.directions

        # 计算屏幕四角
        temp_view = view.copy()
        temp_view.psi -= VIEW_HEIGHT / 2.0
        screen_down = angles_to_vect(temp_view)

        temp_view.psi += VIEW_HEIGHT
        screen_up = angles_to_vect(temp_view)

        temp_view.psi -= VIEW_HEIGHT / 2.0
        temp_view.phi -= VIEW_WIDTH / 2.0
        screen_left = angles_to_vect(temp_view)

        temp_view.phi += VIEW_WIDTH
        screen_right = angles_to_vect(temp_view)

        # 计算屏幕中心和偏移
        screen_mid_vert = (screen_up + screen_down) * 0.5
        screen_mid_hor = (screen_left + screen_right) * 0.5
        mid_to_left = screen_left - screen_mid_hor
        mid_to_up = screen_up - screen_mid_vert

        # 计算每个像素的方向
        directions = []
        for y_pix in range(Y_PIXELS):
            row = []
            y_ratio = y_pix / (Y_PIXELS - 1) * 2
            for x_pix in range(X_PIXELS):
                x_ratio = x_pix / (X_PIXELS - 1) * 2
                # 从中心偏移到像素位置
                tmp = screen_mid_hor + mid_to_left + mid_to_up
                tmp = tmp - mid_to_left * x_ratio
                tmp = tmp - mid_to_up * y_ratio
                row.append(tmp.normalize())
            directions.append(row)

        self.directions = directions
        self._cached_view = view.copy()
        return directions

    def ray_outside(self, x: float, y: float, z: float) -> bool:
        """
        检查位置是否在世界边界外。

        参数：
            x, y, z: 位置坐标

        返回：
            边界外返回 True
        """
        return (
            x >= X_BLOCKS or y >= Y_BLOCKS or z >= Z_BLOCKS or x < 0 or y < 0 or z < 0
        )

    def on_block_border(self, x: float, y: float, z: float) -> bool:
        """
        检查位置是否在方块边缘/角落。

        参数：
            x, y, z: 位置坐标

        返回：
            在边缘返回 True（用于渲染边缘线）
        """
        cnt = 0
        rx, ry, rz = round(x), round(y), round(z)
        if abs(x - rx) < BLOCK_BORDER_SIZE:
            cnt += 1
        if abs(y - ry) < BLOCK_BORDER_SIZE:
            cnt += 1
        if abs(z - rz) < BLOCK_BORDER_SIZE:
            cnt += 1
        return cnt >= 2

    def _dda_step(
        self, x: float, y: float, z: float, dx: float, dy: float, dz: float, eps: float
    ) -> Tuple[float, float, float, float]:
        """
        DDA 算法：计算到下一个方块边界的距离。

        参数：
            x, y, z: 当前位置
            dx, dy, dz: 方向分量
            eps: 小值避免除零

        返回：
            (新x, 新y, 新z, 步进距离)
        """
        dist = 2.0  # 最大步进距离

        if dx > eps:
            dist = min(dist, (int(x + 1) - x) / dx)
        elif dx < -eps:
            dist = min(dist, (int(x) - x) / dx)

        if dy > eps:
            dist = min(dist, (int(y + 1) - y) / dy)
        elif dy < -eps:
            dist = min(dist, (int(y) - y) / dy)

        if dz > eps:
            dist = min(dist, (int(z + 1) - z) / dz)
        elif dz < -eps:
            dist = min(dist, (int(z) - z) / dz)

        step = dist + eps
        return x + dx * step, y + dy * step, z + dz * step, dist

    def raytrace(
        self, pos: Vector, direction: Vector, blocks: List[List[List[str]]]
    ) -> str:
        """
        从位置沿方向追踪光线穿过世界。

        参数：
            pos: 起始位置
            direction: 光线方向（已归一化）
            blocks: 3D方块数组

        返回：
            渲染字符（空为 ' '，方块字符，或边缘 '-'）
        """
        x, y, z = pos.x, pos.y, pos.z
        dx, dy, dz = direction.x, direction.y, direction.z
        eps = RAY_EPSILON

        while not self.ray_outside(x, y, z):
            bx, by, bz = int(x), int(y), int(z)
            c = blocks[bz][by][bx]

            if c != EMPTY_BLOCK:
                if self.on_block_border(x, y, z):
                    return BORDER_CHAR
                return c

            # DDA 步进
            x, y, z, _ = self._dda_step(x, y, z, dx, dy, dz, eps)

        return EMPTY_BLOCK

    def get_current_block(
        self, pos: Vector, direction: Vector, blocks: List[List[List[str]]]
    ) -> Optional[Tuple[int, int, int]]:
        """
        查找玩家注视的方块。

        参数：
            pos: 玩家位置
            direction: 视角方向
            blocks: 3D方块数组

        返回：
            目标方块坐标 (x, y, z)，或 None
        """
        x, y, z = pos.x, pos.y, pos.z
        dx, dy, dz = direction.x, direction.y, direction.z
        eps = RAY_EPSILON

        while not self.ray_outside(x, y, z):
            bx, by, bz = int(x), int(y), int(z)
            c = blocks[bz][by][bx]

            if c != EMPTY_BLOCK:
                return (bx, by, bz)

            x, y, z, _ = self._dda_step(x, y, z, dx, dy, dz, eps)

        return None

    def get_current_block_pos(
        self, pos: Vector, direction: Vector, blocks: List[List[List[str]]]
    ) -> Optional[Vector]:
        """
        查找玩家注视方块的精确位置。

        参数：
            pos: 玩家位置
            direction: 视角方向
            blocks: 3D方块数组

        返回：
            目标方块位置的 Vector，或 None
        """
        x, y, z = pos.x, pos.y, pos.z
        dx, dy, dz = direction.x, direction.y, direction.z
        eps = RAY_EPSILON

        while not self.ray_outside(x, y, z):
            bx, by, bz = int(x), int(y), int(z)
            c = blocks[bz][by][bx]

            if c != EMPTY_BLOCK:
                return Vector(x, y, z)

            x, y, z, _ = self._dda_step(x, y, z, dx, dy, dz, eps)

        return None
