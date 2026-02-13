"""
Raycasting module.

Handles ray-world intersection for rendering.
"""

import math
from typing import List, Optional, Tuple
from .config import (
    X_BLOCKS,
    Y_BLOCKS,
    Z_BLOCKS,
    BLOCK_BORDER_SIZE,
    RAY_EPSILON,
    EMPTY_BLOCK,
    BORDER_CHAR,
)
from .vector import Vector, Vector2, angles_to_vect


class Raycaster:
    """
    Raycasting engine for 3D rendering.
    """

    def __init__(self):
        """Initialize raycaster."""
        self.directions: Optional[List[List[Vector]]] = None

    def init_directions(self, view: Vector2) -> List[List[Vector]]:
        """
        Calculate direction vectors for all screen pixels.

        Args:
            view: Current view angles

        Returns:
            2D array of normalized direction vectors
        """
        from .config import X_PIXELS, Y_PIXELS, VIEW_HEIGHT, VIEW_WIDTH

        # Calculate screen corners
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

        # Calculate screen center and offsets
        screen_mid_vert = (screen_up + screen_down) * 0.5
        screen_mid_hor = (screen_left + screen_right) * 0.5
        mid_to_left = screen_left - screen_mid_hor
        mid_to_up = screen_up - screen_mid_vert

        # Calculate direction for each pixel
        directions = []
        for y_pix in range(Y_PIXELS):
            row = []
            for x_pix in range(X_PIXELS):
                # Start from center, offset to pixel position
                tmp = screen_mid_hor + mid_to_left + mid_to_up
                tmp = tmp - mid_to_left * (x_pix / (X_PIXELS - 1)) * 2
                tmp = tmp - mid_to_up * (y_pix / (Y_PIXELS - 1)) * 2
                row.append(tmp.normalize())
            directions.append(row)

        self.directions = directions
        return directions

    def ray_outside(self, pos: Vector) -> bool:
        """
        Check if position is outside world bounds.

        Args:
            pos: Position to check

        Returns:
            True if outside bounds
        """
        return (
            pos.x >= X_BLOCKS
            or pos.y >= Y_BLOCKS
            or pos.z >= Z_BLOCKS
            or pos.x < 0
            or pos.y < 0
            or pos.z < 0
        )

    def on_block_border(self, pos: Vector) -> bool:
        """
        Check if position is on a block edge/corner.

        Args:
            pos: Position to check

        Returns:
            True if on border (for rendering edge lines)
        """
        cnt = 0
        if abs(pos.x - round(pos.x)) < BLOCK_BORDER_SIZE:
            cnt += 1
        if abs(pos.y - round(pos.y)) < BLOCK_BORDER_SIZE:
            cnt += 1
        if abs(pos.z - round(pos.z)) < BLOCK_BORDER_SIZE:
            cnt += 1
        return cnt >= 2

    def raytrace(
        self, pos: Vector, direction: Vector, blocks: List[List[List[str]]]
    ) -> str:
        """
        Trace ray from position in direction through world.

        Args:
            pos: Starting position
            direction: Ray direction (normalized)
            blocks: 3D block array

        Returns:
            Character to render (' ' for empty, block char, or '-' for edge)
        """
        pos = pos.copy()  # Don't modify original
        eps = RAY_EPSILON

        while not self.ray_outside(pos):
            x, y, z = int(pos.x), int(pos.y), int(pos.z)
            c = blocks[z][y][x]

            if c != EMPTY_BLOCK:
                if self.on_block_border(pos):
                    return BORDER_CHAR
                else:
                    return c

            # Calculate distance to next block boundary
            dist = 2.0

            if direction.x > eps:
                dist = min(dist, (int(pos.x + 1) - pos.x) / direction.x)
            elif direction.x < -eps:
                dist = min(dist, (int(pos.x) - pos.x) / direction.x)

            if direction.y > eps:
                dist = min(dist, (int(pos.y + 1) - pos.y) / direction.y)
            elif direction.y < -eps:
                dist = min(dist, (int(pos.y) - pos.y) / direction.y)

            if direction.z > eps:
                dist = min(dist, (int(pos.z + 1) - pos.z) / direction.z)
            elif direction.z < -eps:
                dist = min(dist, (int(pos.z) - pos.z) / direction.z)

            # Step forward
            pos = pos + direction * (dist + eps)

        return EMPTY_BLOCK

    def get_current_block(
        self, pos: Vector, direction: Vector, blocks: List[List[List[str]]]
    ) -> Optional[Tuple[int, int, int]]:
        """
        Find block that player is looking at.

        Args:
            pos: Player position
            direction: View direction
            blocks: 3D block array

        Returns:
            Tuple of (x, y, z) coordinates of targeted block, or None
        """
        pos = pos.copy()
        eps = RAY_EPSILON

        while not self.ray_outside(pos):
            x, y, z = int(pos.x), int(pos.y), int(pos.z)
            c = blocks[z][y][x]

            if c != EMPTY_BLOCK:
                return (x, y, z)

            # Calculate distance to next block boundary
            dist = 2.0

            if direction.x > eps:
                dist = min(dist, (int(pos.x + 1) - pos.x) / direction.x)
            elif direction.x < -eps:
                dist = min(dist, (int(pos.x) - pos.x) / direction.x)

            if direction.y > eps:
                dist = min(dist, (int(pos.y + 1) - pos.y) / direction.y)
            elif direction.y < -eps:
                dist = min(dist, (int(pos.y) - pos.y) / direction.y)

            if direction.z > eps:
                dist = min(dist, (int(pos.z + 1) - pos.z) / direction.z)
            elif direction.z < -eps:
                dist = min(dist, (int(pos.z) - pos.z) / direction.z)

            # Step forward
            pos = pos + direction * (dist + eps)

        return None

    def get_current_block_pos(
        self, pos: Vector, direction: Vector, blocks: List[List[List[str]]]
    ) -> Optional[Vector]:
        """
        Find exact position of block player is looking at.

        Args:
            pos: Player position
            direction: View direction
            blocks: 3D block array

        Returns:
            Vector of targeted block position, or None
        """
        pos = pos.copy()
        eps = RAY_EPSILON

        while not self.ray_outside(pos):
            x, y, z = int(pos.x), int(pos.y), int(pos.z)
            c = blocks[z][y][x]

            if c != EMPTY_BLOCK:
                return pos

            # Calculate distance to next block boundary
            dist = 2.0

            if direction.x > eps:
                dist = min(dist, (int(pos.x + 1) - pos.x) / direction.x)
            elif direction.x < -eps:
                dist = min(dist, (int(pos.x) - pos.x) / direction.x)

            if direction.y > eps:
                dist = min(dist, (int(pos.y + 1) - pos.y) / direction.y)
            elif direction.y < -eps:
                dist = min(dist, (int(pos.y) - pos.y) / direction.y)

            if direction.z > eps:
                dist = min(dist, (int(pos.z + 1) - pos.z) / direction.z)
            elif direction.z < -eps:
                dist = min(dist, (int(pos.z) - pos.z) / direction.z)

            # Step forward
            pos = pos + direction * (dist + eps)

        return None
