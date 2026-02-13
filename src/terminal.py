"""
Terminal control module.

Handles terminal initialization and restoration using curses.
"""

import sys
import curses
from typing import Optional


class Terminal:
    """
    Terminal controller using curses for non-blocking input.
    """

    def __init__(self):
        """Initialize terminal controller."""
        self.stdscr: Optional[curses.window] = None
        self.initialized = False

    def init_terminal(self) -> curses.window:
        """
        Initialize terminal for non-blocking input.

        Returns:
            curses window object
        """
        self.stdscr = curses.initscr()

        # Disable line buffering
        curses.noecho()
        curses.cbreak()

        # Don't require Enter key
        self.stdscr.nodelay(True)

        # Hide cursor
        curses.curs_set(0)

        # Enable keypad for special keys
        self.stdscr.keypad(True)

        self.initialized = True

        return self.stdscr

    def restore_terminal(self):
        """Restore terminal to original state."""
        if self.initialized and self.stdscr:
            # Show cursor again
            curses.curs_set(1)

            # Restore terminal settings
            curses.nocbreak()
            self.stdscr.keypad(False)
            curses.echo()
            curses.endwin()

            self.initialized = False
            print("Terminal restored")

    def get_stdscr(self) -> Optional[curses.window]:
        """Get the curses window."""
        return self.stdscr

    def clear_screen(self):
        """Clear the terminal screen."""
        if self.stdscr:
            self.stdscr.clear()

    def refresh(self):
        """Refresh the terminal display."""
        if self.stdscr:
            self.stdscr.refresh()


# Global terminal instance for convenience
_terminal_instance: Optional[Terminal] = None


def get_terminal() -> Terminal:
    """Get or create the global terminal instance."""
    global _terminal_instance
    if _terminal_instance is None:
        _terminal_instance = Terminal()
    return _terminal_instance


def init_terminal() -> curses.window:
    """Initialize terminal and return curses window."""
    term = get_terminal()
    return term.init_terminal()


def restore_terminal():
    """Restore terminal to original state."""
    term = get_terminal()
    term.restore_terminal()
