# 🎮 MC_in_terminal

<div align="center">

**终端版 3D Minecraft 游戏**

使用 ASCII 字符渲染的经典 Minecraft 体验

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## 📖 简介

MC_in_terminal 是一款在终端中运行的 3D Minecraft 游戏，使用纯 Python 实现。通过先进的光线追踪渲染引擎，将 3D 方块世界转换为 ASCII 字符艺术，让你在命令行中体验 Minecraft 的乐趣！

这是对原始 C 语言版本 [minecraft.c](https://github.com/tarantino07/minecraft.c) 的 Python 重写版本。

## 功能特点

| 特性 | 描述 |
|------|------|
| **ASCII 渲染** | 使用字符绘制 3D 世界，独特的视觉风格 |
| **光线追踪引擎** | 真实的 3D 光线追踪渲染技术 |
| **方块交互** | 支持放置和删除方块 |
| **重力系统** | 简单的重力模拟，真实的游戏体验 |
| **方块选择** | 准星指向方块高亮显示 |
| **ANSI 颜色** | 支持 ANSI 颜色输出的终端 |
| **零依赖** | 仅使用 Python 标准库 |

## 安装

### 系统要求

- Python 3.6 或更高版本
- 支持 ANSI 颜色的终端

### 克隆仓库

```bash
git clone https://github.com/hasson827/MC_in_terminal.git
cd MC_in_terminal
```

### 安装依赖

**Linux / macOS:**

无需额外安装依赖，项目仅使用 Python 标准库。

```bash
# 可选：确认 Python 版本
python3 --version
```

**Windows:**

Windows 用户需要安装 `windows-curses` 以支持终端控制：

```bash
pip install windows-curses
```

## 运行游戏

```bash
python main.py
```

或使用 Python 3：

```bash
python3 main.py
```

## 操作说明

### 视角控制

| 按键 | 功能 |
|:----:|:-----|
| `w` | 视角向上 |
| `s` | 视角向下 |
| `a` | 视角向左 |
| `d` | 视角向右 |

### 移动控制

| 按键 | 功能 |
|:----:|:-----|
| `i` | 向前移动 |
| `k` | 向后移动 |
| `j` | 向左平移 |
| `l` | 向右平移 |

### 方块操作

| 按键 | 功能 |
|:----:|:-----|
| `空格` | 放置方块 |
| `x` | 删除选中方块 |
| `q` | 退出游戏 |

> 💡 **提示**: 当你瞄准一个方块时，它会高亮显示为 `o` 字符，此时可以执行放置或删除操作。

## 🔧 技术实现

### 光线追踪渲染引擎

本项目的核心是一个 **3D 光线追踪渲染引擎**，工作原理如下：

```
───────────────────────────────────────
             光线追踪流程         
───────────────────────────────────────
  1. 从玩家眼睛位置，向屏幕每个像素发射光线   
  2. 光线沿方向步进，检测是否碰到方块        
  3. 碰到方块时，根据位置判断是否在边缘      
  4. 返回对应字符（方块字符或边缘线）        
───────────────────────────────────────
```

**关键技术点：**

- **DDA 算法优化**: 计算光线到下一个方块边界的精确距离，高效步进
- **边缘检测**: 判断光线是否击中方块边缘，绘制轮廓线
- **视锥计算**: 根据视角参数计算屏幕每个像素的方向向量

### 性能参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 渲染分辨率 | 900 × 180 | 字符级别的渲染分辨率 |
| 世界大小 | 20 × 20 × 10 | 方块数量 (X × Y × Z) |
| 帧率 | 50 FPS | 目标帧率 |
| 视野角度 | 1.0 × 0.7 弧度 | 水平 × 垂直视野 |

## 项目结构

```
MC_in_terminal/
├── README.md              # 项目说明文档
├── requirements.txt       # 依赖列表（Windows 用户）
├── main.py               # 游戏入口
└── src/
    ├── __init__.py       # 包初始化
    ├── config.py         # 游戏配置常量
    ├── vector.py         # 3D 向量数学库
    ├── world.py          # 世界数据和方块管理
    ├── player.py         # 玩家类（移动、物理）
    ├── raycast.py        # 光线追踪渲染引擎
    ├── input_handler.py  # 键盘输入处理
    ├── renderer.py       # ASCII 渲染器
    └── terminal.py       # 终端控制（curses 封装）
```

### 核心模块说明

| 模块 | 功能 |
|------|------|
| `config.py` | 所有可调参数集中管理，便于优化调整 |
| `vector.py` | 3D 向量运算，支持角度转换 |
| `raycast.py` | 光线追踪核心算法，实现 3D 渲染 |
| `renderer.py` | 将光线追踪结果转换为 ASCII 字符 |
| `world.py` | 管理方块数据，支持放置/删除操作 |
| `player.py` | 玩家状态、移动逻辑和重力系统 |

## 配置调优

你可以在 `src/config.py` 中调整游戏参数：

```python
# 屏幕渲染尺寸
Y_PIXELS = 180  # 渲染高度
X_PIXELS = 900  # 渲染宽度

# 移动设置
MOVE_SPEED = 0.30  # 移动速度
TILT_SPEED = 0.1   # 视角旋转速度

# 帧率控制
FRAME_DELAY_MS = 20  # 帧延迟（毫秒）
```

> **注意**: 增大渲染分辨率会显著降低性能，请根据终端大小和机器性能调整。

## 致谢

本项目是对以下项目的 Python 重写：

- **原 C 语言版本**: 感谢原作者创造了这个有趣的终端 Minecraft 概念
- **灵感来源**: 所有热爱在终端中创造艺术的开发者们

---

<div align="center">

**享受在终端中探索 Minecraft 世界！** 

如果你喜欢这个项目，欢迎 ⭐ Star 支持！

</div>
