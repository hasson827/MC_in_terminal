"""
World data module.

Manages the 3D block grid and world generation.
"""

from typing import List, Optional
from .config import X_BLOCKS, Y_BLOCKS, Z_BLOCKS, EMPTY_BLOCK, GROUND_BLOCK
from .vector import Vector


class World:
    """
    3D block world containing all blocks.

    Coordinate system:
    - x: left/right (0 to X_BLOCKS-1)
    - y: forward/backward (0 to Y_BLOCKS-1)
    - z: up/down (0 to Z_BLOCKS-1)
    """

    def __init__(self):
        """Initialize empty world."""
        # Create 3D array: blocks[z][y][x]
        self.blocks: List[List[List[str]]] = [
            [[EMPTY_BLOCK for _ in range(X_BLOCKS)] for _ in range(Y_BLOCKS)]
            for _ in range(Z_BLOCKS)
        ]

    def generate_ground(self, ground_height: int = 4):
        """
        Generate ground layer.

        Args:
            ground_height: Number of bottom layers to fill with ground blocks
        """
        for x in range(X_BLOCKS):
            for y in range(Y_BLOCKS):
                for z in range(min(ground_height, Z_BLOCKS)):
                    self.blocks[z][y][x] = GROUND_BLOCK

    def get_block(self, x: int, y: int, z: int) -> str:
        """
        Get block at position.

        Args:
            x, y, z: Block coordinates

        Returns:
            Block character, or EMPTY_BLOCK if out of bounds
        """
        if not self.is_valid_position(x, y, z):
            return EMPTY_BLOCK
        return self.blocks[z][y][x]

    def set_block(self, x: int, y: int, z: int, block: str):
        """
        Set block at position.

        Args:
            x, y, z: Block coordinates
            block: Block character to place
        """
        if self.is_valid_position(x, y, z):
            self.blocks[z][y][x] = block

    def is_valid_position(self, x: int, y: int, z: int) -> bool:
        """
        Check if position is within world bounds.

        Args:
            x, y, z: Coordinates to check

        Returns:
            True if position is valid
        """
        return 0 <= x < X_BLOCKS and 0 <= y < Y_BLOCKS and 0 <= z < Z_BLOCKS

    def is_empty(self, x: int, y: int, z: int) -> bool:
        """
        Check if block position is empty.

        Args:
            x, y, z: Block coordinates

        Returns:
            True if block is empty or out of bounds
        """
        return self.get_block(x, y, z) == EMPTY_BLOCK

    def place_block(self, pos: Vector, block: str) -> bool:
        """
        Place a block adjacent to the given position.

        Finds the closest face and places block adjacent to it.

        Args:
            pos: Position (ray hit point)
            block: Block character to place

        Returns:
            True if block was placed successfully
        """
        x, y, z = int(pos.x), int(pos.y), int(pos.z)

        # Calculate distances to each face
        dists = [
            abs(x + 1 - pos.x),  # Right face (+x)
            abs(pos.x - x),  # Left face (-x)
            abs(y + 1 - pos.y),  # Back face (+y)
            abs(pos.y - y),  # Front face (-y)
            abs(z + 1 - pos.z),  # Top face (+z)
            abs(pos.z - z),  # Bottom face (-z)
        ]

        # Find closest face
        min_idx = 0
        min_dist = dists[0]
        for i in range(1, 6):
            if dists[i] < min_dist:
                min_dist = dists[i]
                min_idx = i

        # Place block on appropriate side
        dx = [1, -1, 0, 0, 0, 0]
        dy = [0, 0, 1, -1, 0, 0]
        dz = [0, 0, 0, 0, 1, -1]

        new_x = x + dx[min_idx]
        new_y = y + dy[min_idx]
        new_z = z + dz[min_idx]

        if self.is_valid_position(new_x, new_y, new_z):
            self.blocks[new_z][new_y][new_x] = block
            return True
        return False

    def remove_block(self, x: int, y: int, z: int) -> bool:
        """
        Remove block at position.

        Args:
            x, y, z: Block coordinates

        Returns:
            True if block was removed
        """
        if self.is_valid_position(x, y, z) and not self.is_empty(x, y, z):
            self.blocks[z][y][x] = EMPTY_BLOCK
            return True
        return False

    def get_blocks_ref(self) -> List[List[List[str]]]:
        """Get reference to the blocks array."""
        return self.blocks


def init_blocks() -> World:
    """
    Initialize world with ground.

    Returns:
        Initialized World instance
    """
    world = World()
    world.generate_ground(4)  # Fill bottom 4 layers
    return world
