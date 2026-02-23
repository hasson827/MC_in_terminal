#!/usr/bin/env python3
"""
MC_in_terminal - Terminal-based 3D Minecraft

A Python rewrite of the classic terminal Minecraft game.
"""

import sys
import time
import atexit

# Add src directory to path
sys.path.insert(0, ".")

from src.config import (
    FRAME_DELAY_MS,
    GROUND_BLOCK,
    HIGHLIGHT_BLOCK,
)
from src.terminal import Terminal
from src.world import World
from src.player import Player
from src.input_handler import InputHandler
from src.renderer import Renderer


class Game:
    """
    Main game class that orchestrates all components.
    """

    def __init__(self):
        """Initialize game components."""
        self.terminal = Terminal()
        self.world = None
        self.player = None
        self.renderer = None
        self.input_handler = None
        self.raycaster = None
        self.running = False

        # State for block interaction
        self.current_block = None
        self.current_block_char = None

    def init(self):
        """Initialize all game systems."""
        # Initialize terminal
        stdscr = self.terminal.init_terminal()

        # Register cleanup
        atexit.register(self.cleanup)

        # Initialize world
        self.world = World()
        self.world.generate_ground(4)

        # Initialize player
        self.player = Player(x=5.0, y=5.0)

        # Initialize renderer
        self.renderer = Renderer(stdscr)
        self.raycaster = self.renderer.get_raycaster()

        # Initialize input handler
        self.input_handler = InputHandler(stdscr)

        self.running = True
        print("Game initialized. Press 'q' to quit.", file=sys.stderr)

    def cleanup(self):
        """Clean up resources."""
        self.terminal.restore_terminal()

    def process_input(self):
        """Process all input."""
        self.input_handler.process_input()

        if self.input_handler.should_quit():
            self.running = False

    def update(self):
        """Update game state."""
        # Update player (movement, physics)
        self.player.update(self.world, self.input_handler)

        # Get block player is looking at
        pos = self.player.get_pos()
        direction = self.player.get_direction()
        blocks = self.world.get_blocks_ref()

        block_pos = self.raycaster.get_current_block_pos(pos, direction, blocks)

        if block_pos is not None:
            x, y, z = int(block_pos.x), int(block_pos.y), int(block_pos.z)
            self.current_block = (x, y, z)
            self.current_block_char = self.world.get_block(x, y, z)

            # Handle block removal
            if self.input_handler.is_key_pressed("x"):
                self.world.remove_block(x, y, z)
                self.current_block_char = None  # Block was removed
                self.current_block = None

            # Handle block placement
            elif self.input_handler.is_key_pressed(" "):
                self.world.place_block(block_pos, GROUND_BLOCK)
        else:
            self.current_block = None
            self.current_block_char = None

    def render(self):
        """Render the current frame."""
        pos = self.player.get_pos()
        view = self.player.get_view()
        blocks = self.world.get_blocks_ref()

        # Highlight current block if looking at one
        if self.current_block is not None and self.current_block_char is not None:
            x, y, z = self.current_block
            blocks[z][y][x] = HIGHLIGHT_BLOCK

        # Generate and draw picture
        self.renderer.get_picture(pos, view, blocks)
        self.renderer.draw_ascii()

        # Restore original block character
        if self.current_block is not None and self.current_block_char is not None:
            x, y, z = self.current_block
            blocks[z][y][x] = self.current_block_char

    def run(self):
        """Main game loop."""
        self.init()

        frame_time = FRAME_DELAY_MS / 1000.0  # Convert to seconds

        while self.running:
            frame_start = time.time()

            self.process_input()

            if not self.running:
                break

            self.update()
            self.render()

            # Maintain frame rate
            elapsed = time.time() - frame_start
            sleep_time = frame_time - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

        self.cleanup()
        print("Thanks for playing!")


def main():
    """Entry point."""
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted.")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
