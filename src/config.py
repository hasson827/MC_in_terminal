"""
Configuration constants for the game.

All game parameters are defined here for easy tuning.
"""

# Screen rendering dimensions
Y_PIXELS = 180  # Render height (number of rows)
X_PIXELS = 900  # Render width (number of columns)

# World dimensions (in blocks)
Z_BLOCKS = 10  # World height (up/down)
Y_BLOCKS = 20  # World depth (forward/backward)
X_BLOCKS = 20  # World width (left/right)

# Player settings
EYE_HEIGHT = 1.5  # Eye height above feet
VIEW_HEIGHT = 0.7  # Vertical field of view
VIEW_WIDTH = 1.0  # Horizontal field of view

# Block rendering
BLOCK_BORDER_SIZE = 0.05  # Threshold for detecting block edges

# Movement settings
MOVE_SPEED = 0.30  # Movement speed
TILT_SPEED = 0.1  # View rotation speed

# Raycast settings
RAY_EPSILON = 0.01  # Small value for ray stepping

# Frame timing
FRAME_DELAY_MS = 20  # Milliseconds between frames (50 FPS)

# Block characters
EMPTY_BLOCK = " "
GROUND_BLOCK = "@"
HIGHLIGHT_BLOCK = "o"
BORDER_CHAR = "-"
