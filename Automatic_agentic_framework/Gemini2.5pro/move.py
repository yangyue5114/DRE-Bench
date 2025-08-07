import numpy as np
import random

def move_pattern(canvas, pattern, current_pos, direction, n):
    """
    在画布上移动一个3x3的图案。

    此函数首先会将图案在旧位置的痕迹清除（恢复为背景色0），
    然后计算新位置，并在边界检查通过后，将图案绘制到新位置。
    参数:
    - canvas (np.ndarray): 10x20的背景画布。
    - pattern (np.ndarray): 要移动的3x3图案。
    - current_pos (dict): 包含图案当前左上角 'y' 和 'x' 坐标的字典。
    - direction (str): 移动方向，可选值为 'up', 'down', 'left', 'right'。
    - n (int): 向指定方向移动的步数。

    返回:
    - tuple: (canvas, current_pos)
        - 如果移动成功，返回更新后的画布和位置。
        - 如果移动无效（如超出边界），则返回原始的画布和位置。
    """
    # 获取画布和图案的尺寸
    canvas_height, canvas_width = canvas.shape
    pattern_height, pattern_width = pattern.shape
    
    # 获取图案当前的左上角坐标
    y, x = current_pos['y'], current_pos['x']

    # 根据方向和步数计算新位置的理论坐标
    new_y, new_x = y, x
    if direction == 'up':
        new_y -= n
    elif direction == 'down':
        new_y += n
    elif direction == 'left':
        new_x -= n
    elif direction == 'right':
        new_x += n
    else:
        print(f"错误：无效的方向 '{direction}'。请输入 'up', 'down', 'left', 或 'right'。")
        return canvas, current_pos

    # --- 关键：边界检查 ---
    # 检查新位置是否会导致图案的任何部分超出画布边界
    if not (0 <= new_y <= canvas_height - pattern_height and 0 <= new_x <= canvas_width - pattern_width):
        print(f"移动无效：尝试从 ({y}, {x}) 向 {direction} 移动 {n} 格会导致图案超出边界。")
        return canvas, current_pos

    # 如果移动有效，则执行以下操作：
    # 1. 将旧位置的图案擦除 (恢复为背景色0)
    canvas[y:y + pattern_height, x:x + pattern_width] = 0

    # 2. 在新位置绘制图案
    canvas[new_y:new_y + pattern_height, new_x:new_x + pattern_width] = pattern

    # 3. 更新图案的位置记录
    new_pos = {'y': new_y, 'x': new_x}
    
    print(f"成功：图案已从 ({y}, {x}) 移动到 ({new_y}, {new_x})。")
    return canvas, new_pos

# --- 主程序：演示代码 ---
if __name__ == "__main__":
    
    # --- 1. 初始化 ---
    print("--- 1. 初始化环境 ---")
    
    # 创建一个10x20的背景画布，数据类型为整数，填充为0
    canvas_main = np.zeros((10, 20), dtype=int)

    # 创建一个3x3的随机颜色图案 (颜色范围 1-9)
    pattern_main = np.random.randint(1, 10, size=(3, 3))
    print("生成的 3x3 图案为:")
    print(pattern_main)

    # 在一个随机位置绘制图案
    # 为了确保整个3x3图案能完整显示，起始点需要留下足够空间
    # y轴最大起始位置: 10 (画布高) - 3 (图案高) = 7
    # x轴最大起始位置: 20 (画布宽) - 3 (图案宽) = 17
    initial_y = random.randint(0, 7)
    initial_x = random.randint(0, 17)
    
    # 使用字典来存储和追踪图案的位置
    current_position = {'y': initial_y, 'x': initial_x}

    # 将图案的初始状态放置到画布上
    canvas_main[initial_y:initial_y+3, initial_x:initial_x+3] = pattern_main
    
    print("\n--- 2. 初始状态 ---")
    print("初始画布:")
    print(canvas_main)
    print(f"图案的初始位置 (左上角 y, x): ({current_position['y']}, {current_position['x']})")

    # --- 3. 执行一系列移动操作 ---
    print("\n--- 3. 开始移动图案 ---")

    # 示例1: 向右移动5个位置
    print("\n>>> 操作1: 向右移动 5 格")
    canvas_main, current_position = move_pattern(canvas_main, pattern_main, current_position, 'right', 5)
    print(canvas_main)

    # 示例2: 向下移动3个位置
    print("\n>>> 操作2: 向下移动 3 格")
    canvas_main, current_position = move_pattern(canvas_main, pattern_main, current_position, 'down', 3)
    print(canvas_main)
    
    # 示例3: 向左移动10个位置
    print("\n>>> 操作3: 向左移动 10 格")
    canvas_main, current_position = move_pattern(canvas_main, pattern_main, current_position, 'left', 10)
    print(canvas_main)

    # 示例4: 尝试一次无效的移动 (向上移动10格会导致出界)
    print("\n>>> 操作4: 尝试向上移动 10 格 (预期失败)")
    canvas_main, current_position = move_pattern(canvas_main, pattern_main, current_position, 'up', 10)
    print("由于移动无效，画布和位置保持不变:")
    print(canvas_main)
    print(f"图案当前位置仍然是 (y, x): ({current_position['y']}, {current_position['x']})")
    
    # 示例5: 向上移动2个位置 (有效移动)
    print("\n>>> 操作5: 向上移动 2 格 (预期成功)")
    canvas_main, current_position = move_pattern(canvas_main, pattern_main, current_position, 'up', 2)
    print(canvas_main)
    print(f"图案最终位置 (y, x): ({current_position['y']}, {current_position['x']})")