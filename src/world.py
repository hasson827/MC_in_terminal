"""
世界数据模块。

管理3D方块网格和世界生成。
"""

from typing import List
from .config import X_BLOCKS, Y_BLOCKS, Z_BLOCKS, EMPTY_BLOCK, GROUND_BLOCK
from .vector import Vector


class World:
    """
    3D方块世界。

    坐标系：
    - x: 左右 (0 到 X_BLOCKS-1)
    - y: 前后 (0 到 Y_BLOCKS-1)
    - z: 上下 (0 到 Z_BLOCKS-1)
    """

    def __init__(self):
        """初始化空世界。"""
        # 3D数组：blocks[z][y][x]
        self.blocks: List[List[List[str]]] = [
            [[EMPTY_BLOCK for _ in range(X_BLOCKS)] for _ in range(Y_BLOCKS)]
            for _ in range(Z_BLOCKS)
        ]

    def generate_ground(self, ground_height: int = 4):
        """
        生成地面层。

        参数：
            ground_height: 底部填充的层数
        """
        for x in range(X_BLOCKS):
            for y in range(Y_BLOCKS):
                for z in range(min(ground_height, Z_BLOCKS)):
                    self.blocks[z][y][x] = GROUND_BLOCK

    def get_block(self, x: int, y: int, z: int) -> str:
        """
        获取指定位置的方块。

        参数：
            x, y, z: 方块坐标

        返回：
            方块字符，越界返回 EMPTY_BLOCK
        """
        if not self.is_valid_position(x, y, z):
            return EMPTY_BLOCK
        return self.blocks[z][y][x]

    def set_block(self, x: int, y: int, z: int, block: str):
        """
        设置指定位置的方块。

        参数：
            x, y, z: 方块坐标
            block: 方块字符
        """
        if self.is_valid_position(x, y, z):
            self.blocks[z][y][x] = block

    def is_valid_position(self, x: int, y: int, z: int) -> bool:
        """
        检查位置是否在世界边界内。

        参数：
            x, y, z: 坐标

        返回：
            位置有效返回 True
        """
        return 0 <= x < X_BLOCKS and 0 <= y < Y_BLOCKS and 0 <= z < Z_BLOCKS

    def is_empty(self, x: int, y: int, z: int) -> bool:
        """
        检查位置是否为空。

        参数：
            x, y, z: 方块坐标

        返回：
            方块为空或越界返回 True
        """
        return self.get_block(x, y, z) == EMPTY_BLOCK

    def place_block(self, pos: Vector, block: str) -> bool:
        """
        在给定位置相邻处放置方块。

        找到最近的面并在其旁边放置方块。

        参数：
            pos: 射线击中点位置
            block: 方块字符

        返回：
            放置成功返回 True
        """
        x, y, z = int(pos.x), int(pos.y), int(pos.z)

        # 6个面的偏移方向：+x, -x, +y, -y, +z, -z
        offsets = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

        # 6个面到击中点的距离
        dists = [
            abs(x + 1 - pos.x),  # +x 面
            abs(pos.x - x),  # -x 面
            abs(y + 1 - pos.y),  # +y 面
            abs(pos.y - y),  # -y 面
            abs(z + 1 - pos.z),  # +z 面
            abs(pos.z - z),  # -z 面
        ]

        # 找最近的面
        min_idx = min(range(6), key=lambda i: dists[i])
        dx, dy, dz = offsets[min_idx]
        new_x, new_y, new_z = x + dx, y + dy, z + dz

        if self.is_valid_position(new_x, new_y, new_z):
            self.blocks[new_z][new_y][new_x] = block
            return True
        return False

    def remove_block(self, x: int, y: int, z: int) -> bool:
        """
        移除指定位置的方块。

        参数：
            x, y, z: 方块坐标

        返回：
            移除成功返回 True
        """
        if self.is_valid_position(x, y, z) and not self.is_empty(x, y, z):
            self.blocks[z][y][x] = EMPTY_BLOCK
            return True
        return False
