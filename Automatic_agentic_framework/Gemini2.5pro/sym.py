import numpy as np
import random

# --- 全局定义 ---
CANVAS_HEIGHT = 11
CANVAS_WIDTH = 20
# 定义对称轴所在的行索引 (第6行，索引为5)
AXIS_ROW_INDEX = 5
# 定义寻找可用位置时的最大尝试次数，防止无限循环
MAX_PLACEMENT_ATTEMPTS = 100

def create_canvas_with_axis(height, width, axis_index):
    """
    创建一个带有水平对称轴的画布。
    """
    canvas = np.zeros((height, width), dtype=int)
    canvas[axis_index, :] = 1
    return canvas

def generate_random_pattern():
    """
    生成一个随机尺寸 (不超过3x3) 和随机颜色的图案。
    """
    p_height = random.randint(1, 3)
    p_width = random.randint(1, 3)
    pattern = np.random.randint(2, 10, size=(p_height, p_width)) # 颜色从2开始，避免与对称轴的1混淆
    return pattern

def is_area_free(canvas, y, x, h, w):
    """
    检查画布上的一个矩形区域是否为空（即是否全为0）。
    """
    # 提取目标区域
    target_area = canvas[y : y + h, x : x + w]
    # 使用 np.all() 检查是否所有元素都为0
    return np.all(target_area == 0)

def place_and_reflect_pattern_safely(canvas, pattern, axis_y):
    """
    安全地放置图案及其反射，确保不覆盖任何现有图案。
    会尝试多次以寻找一个两个都可用的空闲位置。
    """
    p_height, p_width = pattern.shape
    canvas_height, canvas_width = canvas.shape
    reflected_pattern = np.flipud(pattern)

    for attempt in range(MAX_PLACEMENT_ATTEMPTS):
        # 1. 随机选择一个有效的原始位置
        side = random.choice(['above', 'below'])
        y_orig, x_orig = -1, -1

        if side == 'above' and axis_y - p_height >= 0:
            y_orig = random.randint(0, axis_y - p_height)
            x_orig = random.randint(0, canvas_width - p_width)
        elif side == 'below' and axis_y + 1 <= canvas_height - p_height:
            y_orig = random.randint(axis_y + 1, canvas_height - p_height)
            x_orig = random.randint(0, canvas_width - p_width)
        else: # 如果第一次选择的边放不下，尝试另一边
            side = 'below' if side == 'above' else 'above'
            if side == 'above' and axis_y - p_height >= 0:
                y_orig = random.randint(0, axis_y - p_height)
            elif side == 'below' and axis_y + 1 <= canvas_height - p_height:
                y_orig = random.randint(axis_y + 1, canvas_height - p_height)
            if y_orig == -1: # 如果两边都放不下
                if attempt == 0: print(f"信息: 图案 {p_height}x{p_width} 过大，无法放置。")
                return canvas # 直接返回，不进行放置
        
        x_orig = random.randint(0, canvas_width - p_width)
        
        # 2. 计算其反射位置
        y_refl = (2 * axis_y) - y_orig - p_height + 1
        x_refl = x_orig
        
        # 3. 检查原始位置和反射位置是否都为空闲
        if is_area_free(canvas, y_orig, x_orig, p_height, p_width) and \
           is_area_free(canvas, y_refl, x_refl, p_height, p_width):
            
            # 4. 如果都空闲，则放置图案并返回
            canvas[y_orig : y_orig + p_height, x_orig : x_orig + p_width] = pattern
            canvas[y_refl : y_refl + p_height, x_refl : x_refl + p_width] = reflected_pattern
            print(f"成功: 在第 {attempt + 1} 次尝试时找到对称位置。")
            print(f"  - 原始图案({p_height}x{p_width})已放置在({y_orig}, {x_orig}), 反射图案放置在({y_refl}, {x_refl})")
            return canvas

    # 5. 如果循环结束仍未找到位置，则放弃
    print(f"警告: 尝试 {MAX_PLACEMENT_ATTEMPTS} 次后，未能为尺寸为 {p_height}x{p_width} 的图案找到无冲突的对称位置。")
    return canvas

def place_noise_pattern_safely(canvas, pattern, axis_y):
    """安全地放置一个非对称的“噪音”图案。"""
    p_h, p_w = pattern.shape
    canvas_h, canvas_w = canvas.shape
    
    for _ in range(MAX_PLACEMENT_ATTEMPTS):
        y, x = -1, -1
        # 与上面类似的逻辑寻找一个单独的空位
        if random.choice(['above', 'below']) == 'above' and axis_y - p_h >= 0:
            y = random.randint(0, axis_y - p_h)
        elif axis_y + 1 <= canvas_h - p_h:
            y = random.randint(axis_y + 1, canvas_h - p_h)
        
        if y != -1:
            x = random.randint(0, canvas_w - p_w)
            if is_area_free(canvas, y, x, p_h, p_w):
                canvas[y:y+p_h, x:x+p_w] = pattern
                print(f"成功: 已添加一个非对称图案在 ({y},{x})")
                return canvas
                
    print("警告: 未能为非对称图案找到无冲突的位置。")
    return canvas

# --- 主程序 ---
if __name__ == "__main__":
    
    number_of_symmetric_pairs = 4 # 可适当增加数量来测试防冲突效果
    
    main_canvas = create_canvas_with_axis(CANVAS_HEIGHT, CANVAS_WIDTH, AXIS_ROW_INDEX)
    
    print("--- 初始画布 (仅包含对称轴) ---")
    print(main_canvas)
    
    print(f"\n--- 开始生成 {number_of_symmetric_pairs} 组对称图案 (不会相互覆盖) ---")
    for i in range(number_of_symmetric_pairs):
        print(f"\n--- 正在尝试放置第 {i + 1} 组 ---")
        random_p = generate_random_pattern()
        main_canvas = place_and_reflect_pattern_safely(main_canvas, random_p, AXIS_ROW_INDEX)

    # print("\n--- 尝试增加 2 个额外的非对称图案 ---")
    # for i in range(2):
    #     print(f"\n--- 正在尝试放置第 {i + 1} 个非对称图案 ---")
    #     noise_p = generate_random_pattern()
    #     main_canvas = place_noise_pattern_safely(main_canvas, noise_p, AXIS_ROW_INDEX)

    print("\n\n--- 最终完成的画布 ---")
    print(main_canvas)