"""
Player module.

Handles player position, view, movement, and physics.
"""

from typing import TYPE_CHECKING
from .config import X_BLOCKS, Y_BLOCKS, Z_BLOCKS, EYE_HEIGHT, MOVE_SPEED, TILT_SPEED
from .vector import Vector, Vector2, angles_to_vect

if TYPE_CHECKING:
    from .world import World
    from .input_handler import InputHandler


class Player:
    """
    Player class with position, view, and movement logic.
    """

    def __init__(self, x: float = 5.0, y: float = 5.0, z: float = None):
        """
        Initialize player.

        Args:
            x: Initial x position
            y: Initial y position
            z: Initial z position (defaults to ground level + eye height)
        """
        self.pos = Vector(x=x, y=y, z=z if z is not None else (4 + EYE_HEIGHT))
        self.view = Vector2(psi=0.0, phi=0.0)

    def update(self, world: "World", input_handler: "InputHandler"):
        """
        Update player position and view based on input and physics.

        Args:
            world: World instance for collision detection
            input_handler: Input handler for reading controls
        """
        self._apply_gravity(world)
        self._apply_collision(world)
        self._process_movement(input_handler)
        self._process_view(input_handler)

    def _apply_gravity(self, world: "World"):
        """Apply simple gravity - fall if no block below feet."""
        x, y = int(self.pos.x), int(self.pos.y)
        z_below = int(self.pos.z - EYE_HEIGHT - 0.01)

        if 0 <= z_below < Z_BLOCKS and world.is_empty(x, y, z_below):
            self.pos.z -= 1

    def _apply_collision(self, world: "World"):
        """Handle collision - push up if inside a block."""
        x, y = int(self.pos.x), int(self.pos.y)
        z_at = int(self.pos.z - EYE_HEIGHT + 0.01)

        if 0 <= z_at < Z_BLOCKS and not world.is_empty(x, y, z_at):
            self.pos.z += 1

    def _process_movement(self, input_handler: "InputHandler"):
        """Process movement input."""
        direction = angles_to_vect(self.view)

        if input_handler.is_key_pressed("i"):
            # Move forward
            self.pos.x += MOVE_SPEED * direction.x
            self.pos.y += MOVE_SPEED * direction.y

        if input_handler.is_key_pressed("k"):
            # Move backward
            self.pos.x -= MOVE_SPEED * direction.x
            self.pos.y -= MOVE_SPEED * direction.y

        if input_handler.is_key_pressed("j"):
            # Strafe left
            self.pos.x += MOVE_SPEED * direction.y
            self.pos.y -= MOVE_SPEED * direction.x

        if input_handler.is_key_pressed("l"):
            # Strafe right
            self.pos.x -= MOVE_SPEED * direction.y
            self.pos.y += MOVE_SPEED * direction.x

        # Clamp position to world bounds
        self.pos.x = max(0.1, min(X_BLOCKS - 0.1, self.pos.x))
        self.pos.y = max(0.1, min(Y_BLOCKS - 0.1, self.pos.y))
        self.pos.z = max(EYE_HEIGHT, min(Z_BLOCKS - 0.1, self.pos.z))

    def _process_view(self, input_handler: "InputHandler"):
        """Process view rotation input."""
        if input_handler.is_key_pressed("w"):
            # Look up
            self.view.psi += TILT_SPEED

        if input_handler.is_key_pressed("s"):
            # Look down
            self.view.psi -= TILT_SPEED

        if input_handler.is_key_pressed("d"):
            # Look right
            self.view.phi += TILT_SPEED

        if input_handler.is_key_pressed("a"):
            # Look left
            self.view.phi -= TILT_SPEED

        # Clamp vertical view angle
        self.view.psi = max(-1.5, min(1.5, self.view.psi))

    def get_direction(self) -> Vector:
        """Get current view direction as vector."""
        return angles_to_vect(self.view)

    def get_pos(self) -> Vector:
        """Get current position."""
        return self.pos.copy()

    def get_view(self) -> Vector2:
        """Get current view angles."""
        return self.view.copy()


def init_player() -> Player:
    """
    Create and initialize a player at default position.

    Returns:
        Initialized Player instance
    """
    return Player(x=5.0, y=5.0)
