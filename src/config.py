"""
游戏配置常量。

所有游戏参数在此定义，便于调整。
"""

# 屏幕渲染尺寸
Y_PIXELS = 180  # 渲染高度（行数）
X_PIXELS = 900  # 渲染宽度（列数）

# 世界尺寸（方块数）
Z_BLOCKS = 10  # 世界高度（上下）
Y_BLOCKS = 20  # 世界深度（前后）
X_BLOCKS = 20  # 世界宽度（左右）

# 玩家设置
EYE_HEIGHT = 1.5  # 眼睛高度（相对脚底）
VIEW_HEIGHT = 0.7  # 垂直视野范围
VIEW_WIDTH = 1.0  # 水平视野范围

# 方块渲染
BLOCK_BORDER_SIZE = 0.05  # 检测方块边缘的阈值

# 移动设置
MOVE_SPEED = 0.30  # 移动速度
TILT_SPEED = 0.1  # 视角旋转速度

# 光线追踪设置
RAY_EPSILON = 0.01  # 光线步进的小值

# 帧计时
FRAME_DELAY_MS = 20  # 帧间隔毫秒（50 FPS）

# 方块字符
EMPTY_BLOCK = " "  # 空气
GROUND_BLOCK = "@"  # 地面方块
HIGHLIGHT_BLOCK = "o"  # 高亮方块（玩家注视的）
BORDER_CHAR = "-"  # 边缘字符
