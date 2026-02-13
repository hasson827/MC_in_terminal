"""
Input handling module.

Processes keyboard input for game controls.
"""

import curses
from typing import Set


class InputHandler:
    """
    Handles keyboard input processing.
    """

    def __init__(self, stdscr: curses.window):
        """
        Initialize input handler.

        Args:
            stdscr: curses window for input
        """
        self.stdscr = stdscr
        self.keystate: Set[int] = set()
        self._should_quit = False

    def process_input(self):
        """
        Process all pending keyboard input.

        Clears previous state and reads all current keypresses.
        """
        # Clear previous key state
        self.keystate.clear()

        # Read all pending input
        while True:
            try:
                key = self.stdscr.getch()
                if key == -1:
                    break  # No more input

                # Handle q key for quit
                if key == ord("q") or key == ord("Q"):
                    self._should_quit = True

                self.keystate.add(key)

            except curses.error:
                break

    def is_key_pressed(self, key: str) -> bool:
        """
        Check if a key is currently pressed.

        Args:
            key: Single character key to check

        Returns:
            True if key is pressed, False otherwise
        """
        return ord(key) in self.keystate

    def is_keycode_pressed(self, keycode: int) -> bool:
        """
        Check if a keycode is currently pressed.

        Args:
            keycode: Key code to check

        Returns:
            True if keycode is pressed, False otherwise
        """
        return keycode in self.keystate

    def should_quit(self) -> bool:
        """Check if quit was requested."""
        return self._should_quit

    def reset_quit(self):
        """Reset quit flag."""
        self._should_quit = False


# Key constants for convenience
KEY_QUIT = ord("q")
KEY_LOOK_UP = ord("w")
KEY_LOOK_DOWN = ord("s")
KEY_LOOK_LEFT = ord("a")
KEY_LOOK_RIGHT = ord("d")
KEY_MOVE_FORWARD = ord("i")
KEY_MOVE_BACKWARD = ord("k")
KEY_STRAFE_LEFT = ord("j")
KEY_STRAFE_RIGHT = ord("l")
KEY_REMOVE_BLOCK = ord("x")
KEY_PLACE_BLOCK = ord(" ")  # Space bar
