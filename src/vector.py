"""
3D Vector mathematics module.

Provides Vector and Vector2 classes for 3D calculations.
"""

import math
from typing import Tuple
from dataclasses import dataclass


@dataclass
class Vector:
    """3D Vector with x, y, z components."""

    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __add__(self, other: "Vector") -> "Vector":
        """Add two vectors."""
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector") -> "Vector":
        """Subtract two vectors."""
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> "Vector":
        """Multiply vector by scalar."""
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar: float) -> "Vector":
        """Right multiply vector by scalar."""
        return self.__mul__(scalar)

    def __neg__(self) -> "Vector":
        """Negate vector."""
        return Vector(-self.x, -self.y, -self.z)

    def length(self) -> float:
        """Calculate vector length."""
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self) -> "Vector":
        """Return normalized vector (unit length)."""
        length = self.length()
        if length == 0:
            return Vector(0, 0, 0)
        return Vector(self.x / length, self.y / length, self.z / length)

    def copy(self) -> "Vector":
        """Create a copy of this vector."""
        return Vector(self.x, self.y, self.z)

    def to_tuple(self) -> Tuple[int, int, int]:
        """Convert to integer tuple (for indexing)."""
        return (int(self.x), int(self.y), int(self.z))


@dataclass
class Vector2:
    """2D Vector for view angles (psi = vertical, phi = horizontal)."""

    psi: float = 0.0  # Vertical angle (pitch)
    phi: float = 0.0  # Horizontal angle (yaw)

    def copy(self) -> "Vector2":
        """Create a copy of this vector."""
        return Vector2(self.psi, self.phi)


def angles_to_vect(angles: Vector2) -> Vector:
    """
    Convert view angles to a direction vector.

    Args:
        angles: Vector2 containing psi (pitch) and phi (yaw)

    Returns:
        Vector pointing in the direction of the angles
    """
    return Vector(
        x=math.cos(angles.psi) * math.cos(angles.phi),
        y=math.cos(angles.psi) * math.sin(angles.phi),
        z=math.sin(angles.psi),
    )


def vect_add(v1: Vector, v2: Vector) -> Vector:
    """Add two vectors."""
    return v1 + v2


def vect_sub(v1: Vector, v2: Vector) -> Vector:
    """Subtract v2 from v1."""
    return v1 - v2


def vect_scale(scalar: float, v: Vector) -> Vector:
    """Scale a vector by a scalar."""
    return v * scalar


def vect_normalize(v: Vector) -> Vector:
    """Normalize a vector to unit length."""
    return v.normalize()
