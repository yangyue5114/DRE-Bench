import numpy as np
import math

# --- 1. 全局定义与设置 ---

# 画布尺寸和中心点
SIZE = 13
CENTER = SIZE // 2  # 对于尺寸13，中心索引是 6

# 定义直线的颜色 (确保它们不同)
# 颜色定义：1-9代表九种不同颜色，0代表背景
COLOR_TOP_ENDPOINT = 7
COLOR_LINE_BODY = 4
COLOR_BOTTOM_ENDPOINT = 9

# 定义直线的长度（从中心点向上延伸的格数，不含中心点本身）
LINE_LENGTH_FROM_CENTER = 5


def rotate_point(y, x, angle_deg, center_y, center_x):
    """
    围绕一个中心点旋转一个坐标点。

    参数:
    - y, x (int): 要旋转的点的原始坐标。
    - angle_deg (float): 旋转角度 (单位：度)。
    - center_y, center_x (int): 旋转中心的坐标。

    返回:
    - tuple: (new_y, new_x) 旋转后的整数坐标。
    """
    # 将角度转换为弧度
    angle_rad = math.radians(angle_deg)

    # 步骤1: 将坐标平移，使旋转中心成为原点 (0,0)
    translated_x = x - center_x
    translated_y = y - center_y

    # 步骤2: 应用标准2D旋转公式
    # x' = x*cos(θ) - y*sin(θ)
    # y' = x*sin(θ) + y*cos(θ)
    rotated_x = translated_x * math.cos(angle_rad) - translated_y * math.sin(angle_rad)
    rotated_y = translated_x * math.sin(angle_rad) + translated_y * math.cos(angle_rad)

    # 步骤3: 将坐标平移回原来的坐标系
    # 并使用 round() 四舍五入到最近的整数格点
    new_x = int(round(rotated_x + center_x))
    new_y = int(round(rotated_y + center_y))

    return new_y, new_x

def main():
    """
    主函数，执行所有操作。
    """
    # --- 2. 创建初始直线的定义 ---
    # 我们不直接在矩阵上画线，而是创建一个点的列表。
    # 每个元素包含其原始坐标和颜色。
    original_line_points = []

    # 添加底部端点 (位于中心)
    original_line_points.append({'y': CENTER, 'x': CENTER, 'color': COLOR_BOTTOM_ENDPOINT})

    # 添加直线主体 (从中心点上方一格开始)
    for i in range(1, LINE_LENGTH_FROM_CENTER):
        original_line_points.append({'y': CENTER - i, 'x': CENTER, 'color': COLOR_LINE_BODY})

    # 添加顶部端点
    original_line_points.append({'y': CENTER - LINE_LENGTH_FROM_CENTER, 'x': CENTER, 'color': COLOR_TOP_ENDPOINT})

    # 定义要处理的旋转角度
    angles_to_process = [0, 45, 90, 135, 180, 225, 270, 315]

    # --- 3. 循环处理每个角度并输出结果 ---
    print("本任务将一条中心垂直线围绕画布中心进行旋转。")

    # 首先显示初始状态 (0度)
    print("\n--- 初始状态 (旋转 0 度) ---")
    canvas_0_deg = np.zeros((SIZE, SIZE), dtype=int)
    for point in original_line_points:
        canvas_0_deg[point['y'], point['x']] = point['color']
    print(canvas_0_deg)

    # 循环处理其他角度
    for angle in angles_to_process[1:]: # 从45度开始
        print(f"\n--- 旋转 {angle} 度 ---")
        
        # 为每个角度创建一个全新的空白画布
        new_canvas = np.zeros((SIZE, SIZE), dtype=int)
        
        # 遍历原始直线的每一个点
        for point in original_line_points:
            # 计算该点旋转后的新位置
            ny, nx = rotate_point(point['y'], point['x'], angle, CENTER, CENTER)
            
            # 边界检查，确保新坐标在画布内
            if 0 <= ny < SIZE and 0 <= nx < SIZE:
                new_canvas[ny, nx] = point['color']
        
        print(new_canvas)
        
    # 根据要求，单独输出360度的结果，它与0度相同
    print("\n--- 旋转 360 度 ---")
    print(canvas_0_deg)


# --- 程序入口 ---
if __name__ == "__main__":
    main()