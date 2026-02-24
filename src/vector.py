"""
3D向量数学模块。

提供 Vector 和 Vector2 类用于3D计算。
"""

import math
from dataclasses import dataclass


@dataclass
class Vector:
    """3D向量，包含 x, y, z 分量。"""

    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __add__(self, other: "Vector") -> "Vector":
        """向量加法。"""
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector") -> "Vector":
        """向量减法。"""
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> "Vector":
        """向量乘以标量。"""
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar: float) -> "Vector":
        """标量乘以向量（右乘）。"""
        return self.__mul__(scalar)

    def iadd_scaled(self, other: "Vector", scalar: float) -> None:
        """
        原位操作：self += other * scalar
        避免创建临时Vector对象，用于性能优化。
        """
        self.x += other.x * scalar
        self.y += other.y * scalar
        self.z += other.z * scalar

    def length(self) -> float:
        """计算向量长度。"""
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self) -> "Vector":
        """返回归一化向量（单位长度）。"""
        length = self.length()
        if length < 1e-10:
            return Vector(0, 0, 0)
        return Vector(self.x / length, self.y / length, self.z / length)

    def copy(self) -> "Vector":
        """创建此向量的副本。"""
        return Vector(self.x, self.y, self.z)


@dataclass
class Vector2:
    """2D向量，用于视角（psi=俯仰角, phi=偏航角）。"""

    psi: float = 0.0  # 垂直角度（俯仰）
    phi: float = 0.0  # 水平角度（偏航）

    def copy(self) -> "Vector2":
        """创建此向量的副本。"""
        return Vector2(self.psi, self.phi)


def angles_to_vect(angles: Vector2) -> Vector:
    """
    将视角角度转换为方向向量。

    参数：
        angles: 包含 psi（俯仰角）和 phi（偏航角）的 Vector2

    返回：
        指向该角度方向的 Vector
    """
    cos_psi = math.cos(angles.psi)
    return Vector(
        x=cos_psi * math.cos(angles.phi),
        y=cos_psi * math.sin(angles.phi),
        z=math.sin(angles.psi),
    )
