"""
Renderer module.

Handles ASCII rendering of the 3D world.
"""

import sys
from typing import List, Optional
from .config import X_PIXELS, Y_PIXELS, EMPTY_BLOCK, HIGHLIGHT_BLOCK
from .vector import Vector, Vector2
from .raycast import Raycaster

# Try to import curses, handle if not available
try:
    import curses

    HAS_CURSES = True
except ImportError:
    HAS_CURSES = False


class Renderer:
    """
    ASCII renderer for the 3D world.
    """

    def __init__(self, stdscr=None):
        """
        Initialize renderer.

        Args:
            stdscr: Optional curses window for output
        """
        self.raycaster = Raycaster()
        self.stdscr = stdscr
        self.picture: List[List[str]] = []
        self._init_picture()

    def _init_picture(self):
        """Initialize the picture buffer."""
        self.picture = [[EMPTY_BLOCK for _ in range(X_PIXELS)] for _ in range(Y_PIXELS)]

    def get_picture(
        self, pos: Vector, view: Vector2, blocks: List[List[List[str]]]
    ) -> List[List[str]]:
        """
        Generate rendered picture from player view.

        Args:
            pos: Player position
            view: Player view angles
            blocks: 3D block array

        Returns:
            2D array of characters representing the view
        """
        # Calculate all direction vectors
        directions = self.raycaster.init_directions(view)

        # Render each pixel
        for y in range(Y_PIXELS):
            for x in range(X_PIXELS):
                self.picture[y][x] = self.raycaster.raytrace(
                    pos, directions[y][x], blocks
                )

        return self.picture

    def draw_ascii(self, picture: Optional[List[List[str]]] = None):
        """
        Draw picture to terminal with ANSI colors.

        Args:
            picture: Picture to draw (uses internal buffer if None)
        """
        if picture is None:
            picture = self.picture

        if self.stdscr and HAS_CURSES:
            self._draw_curses(picture)
        else:
            self._draw_stdout(picture)

    def _draw_curses(self, picture: List[List[str]]):
        """Draw using curses."""
        try:
            self.stdscr.clear()

            # Define color pairs if colors are available
            if curses.has_colors():
                curses.start_color()
                curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

            for i, row in enumerate(picture):
                line = "".join(row)
                if curses.has_colors():
                    # Highlight 'o' characters in green
                    self.stdscr.addstr(i, 0, line, curses.color_pair(0))
                else:
                    self.stdscr.addstr(i, 0, line)

            self.stdscr.refresh()
        except curses.error:
            pass  # Ignore curses errors (e.g., window too small)

    def _draw_stdout(self, picture: List[List[str]]):
        """Draw using standard output with ANSI codes."""
        # Move cursor to top-left
        sys.stdout.write("\033[0;0H")
        sys.stdout.flush()

        for row in picture:
            current_color = False
            line = []
            for c in row:
                if c == HIGHLIGHT_BLOCK and not current_color:
                    line.append("\x1b[32m")  # Green
                    current_color = True
                elif c != HIGHLIGHT_BLOCK and current_color:
                    line.append("\x1b[0m")  # Reset
                    current_color = False
                line.append(c)

            if current_color:
                line.append("\x1b[0m")  # Reset at end of line

            line.append("\n")
            sys.stdout.write("".join(line))

        sys.stdout.flush()

    def get_raycaster(self) -> Raycaster:
        """Get the raycaster instance."""
        return self.raycaster
