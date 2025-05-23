import json
import random
import numpy as np
import os
from PIL import Image, ImageDraw
import time
import copy

idx = 1

# 颜色定义
color_table = {
    "0": (0, 0, 0),        # 黑色（背景）
    "1": (0, 116, 217),    # 蓝色
    "2": (255, 65, 54),    # 红色
    "3": (46, 204, 64),    # 绿色
    "4": (255, 220, 0),    # 黄色（用于圈）
    "5": (170, 170, 170),  # 灰色
    "6": (240, 18, 190),   # 紫红色
    "7": (255, 133, 27),   # 橙色
    "8": (127, 219, 255),  # 青色
    "9": (135, 12, 37)     # 棕色
}

# 可用于随机色块的颜色（不包括黑色和黄色）
block_colors = [1, 2, 3, 5, 6, 7, 8, 9]
WHITE = (255, 255, 255)

def convert_int(grid):
    """将网格转换为整数类型"""
    return [[int(item) for item in sublist] for sublist in grid]

def create_hollow_circle(matrix, size, start_row, start_col):
    """在矩阵中创建一个空心黄圈，并返回四个顶点坐标"""
    # 确保圈至少是3x3大小
    size = max(size, 3)
    
    # 检查是否超出边界
    if start_row + size > len(matrix) or start_col + size > len(matrix[0]):
        return None
    
    # 检查放置位置是否已有颜色块
    for i in range(start_row, start_row + size):
        for j in range(start_col, start_col + size):
            if matrix[i][j] != 0:
                return None
                
    # 放置空心黄圈
    for i in range(start_row, start_row + size):
        for j in range(start_col, start_col + size):
            # 只在边缘填充黄色
            if (i == start_row or i == start_row + size - 1 or 
                j == start_col or j == start_col + size - 1):
                matrix[i][j] = 4  # 黄色
    
    # 返回四个顶点坐标：左上, 右上, 左下, 右下
    return (start_row, start_col, start_row + size - 1, start_col + size - 1)

def draw_circle(matrix, top, left, bottom, right):
    """根据四个顶点坐标绘制空心黄圈"""
    for i in range(top, bottom + 1):
        for j in range(left, right + 1):
            if (i == top or i == bottom or j == left or j == right):
                matrix[i][j] = 4  # 黄色

def clear_old_circle(matrix, top, left, bottom, right):
    """清除旧的黄圈，将其重置为黑色"""
    for i in range(top, bottom + 1):
        for j in range(left, right + 1):
            if (i == top or i == bottom or j == left or j == right) and matrix[i][j] == 4:
                matrix[i][j] = 0  # 黑色

def predict_expansion_boundary(matrix, top, left, bottom, right, flag):
    """预测一个圈可能扩散到的最远边界"""
    rows, cols = len(matrix), len(matrix[0])
    
    # 向上扩散，直到碰到障碍物或边界
    top_bound = top
    while top_bound > 0:
        blocked = False
        for j in range(left, right + 1):
            if matrix[top_bound - 1][j] != 0:
                if matrix[top_bound - 1][j] == 4:
                    flag[0] = True
                blocked = True
                break
        if blocked:
            break
        top_bound -= 1
    
    # 向右扩散
    right_bound = right
    while right_bound < cols - 1:
        blocked = False
        for i in range(top, bottom + 1):
            if matrix[i][right_bound + 1] != 0:
                if matrix[i][right_bound + 1] == 4:
                    flag[0] = True
                blocked = True
                break
        if blocked:
            break
        right_bound += 1
    
    # 向下扩散
    bottom_bound = bottom
    while bottom_bound < rows - 1:
        blocked = False
        for j in range(left, right + 1):
            if matrix[bottom_bound + 1][j] != 0:
                if matrix[bottom_bound + 1][j] == 4:
                    flag[0] = True
                blocked = True
                break
        if blocked:
            break
        bottom_bound += 1
    
    # 向左扩散
    left_bound = left
    while left_bound > 0:
        blocked = False
        for i in range(top, bottom + 1):
            if matrix[i][left_bound - 1] != 0:
                if matrix[i][left_bound - 1] == 4:
                    flag[0] = True
                blocked = True
                break
        if blocked:
            break
        left_bound -= 1
    
    return (top_bound, left_bound, bottom_bound, right_bound)

def would_circles_overlap(matrix, circles, new_circle):
    """检查新圈在扩散后是否会与已有圈重叠"""
    # 创建一个临时矩阵用于模拟扩散
    temp_matrix = copy.deepcopy(matrix)

    # 设置一个标记，若遇到黄色，则表示会相遇
    flag = [False]
    
    # 在临时矩阵中标记所有已有圈的当前位置
    for circle in circles:
        top, left, bottom, right = circle
        draw_circle(temp_matrix, top, left, bottom, right)
    
    # 预测新圈扩散后的边界
    new_top, new_left, new_bottom, new_right = predict_expansion_boundary(temp_matrix, *new_circle, flag)
    
    # 创建一个新矩阵，标记新圈扩散后的区域
    expansion_matrix = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    for i in range(new_top, new_bottom + 1):
        for j in range(new_left, new_right + 1):
            if i == new_top or i == new_bottom or j == new_left or j == new_right:
                expansion_matrix[i][j] = 1
    
    # 预测所有已有圈扩散后的区域
    for circle in circles:
        circle_top, circle_left, circle_bottom, circle_right = circle
        expanded_top, expanded_left, expanded_bottom, expanded_right = predict_expansion_boundary(temp_matrix, *circle, flag)
        
        # 在扩散矩阵中标记已有圈扩散后的区域
        for i in range(expanded_top, expanded_bottom + 1):
            for j in range(expanded_left, expanded_right + 1):
                if i == expanded_top or i == expanded_bottom or j == expanded_left or j == expanded_right:
                    # 检查新圈扩散区域是否与已有圈扩散区域重叠
                    if expansion_matrix[i][j] == 1 or flag[0] == True:
                        return True  # 发现重叠
    
    return False  # 没有重叠

def expand_circle(matrix, circles):
    """根据提供的圈坐标，实现每个圈的四个边向外扩散"""
    rows, cols = len(matrix), len(matrix[0])
    output_matrix = copy.deepcopy(matrix)
    
    # 记录每个圈是否还可以继续扩散
    can_expand = [True] * len(circles)
    
    # 最大迭代次数，防止无限循环
    max_iterations = max(rows, cols)
    
    for iteration in range(max_iterations):
        any_expanded = False  # 标记本轮是否有任何圈扩散
        
        for circle_idx, circle in enumerate(circles):
            if not can_expand[circle_idx]:
                continue  # 跳过不能扩散的圈
            
            top, left, bottom, right = circle
            
            # 检查四条边是否可以扩散
            can_expand_top = True
            can_expand_right = True
            can_expand_bottom = True
            can_expand_left = True
            
            # 1. 检查上边是否可以上扩散
            if top > 0:  # 确保不超出顶部边界
                for j in range(left, right + 1):
                    if output_matrix[top - 1][j] != 0:  # 如果上方有非空单元格
                        can_expand_top = False
                        break
            else:
                can_expand_top = False  # 已经到达顶部边界
            
            # 2. 检查右边是否可以右扩散
            if right < cols - 1:  # 确保不超出右侧边界
                for i in range(top, bottom + 1):
                    if output_matrix[i][right + 1] != 0:  # 如果右侧有非空单元格
                        can_expand_right = False
                        break
            else:
                can_expand_right = False  # 已经到达右侧边界
            
            # 3. 检查下边是否可以下扩散
            if bottom < rows - 1:  # 确保不超出底部边界
                for j in range(left, right + 1):
                    if output_matrix[bottom + 1][j] != 0:  # 如果下方有非空单元格
                        can_expand_bottom = False
                        break
            else:
                can_expand_bottom = False  # 已经到达底部边界
            
            # 4. 检查左边是否可以左扩散
            if left > 0:  # 确保不超出左侧边界
                for i in range(top, bottom + 1):
                    if output_matrix[i][left - 1] != 0:  # 如果左侧有非空单元格
                        can_expand_left = False
                        break
            else:
                can_expand_left = False  # 已经到达左侧边界
            
            # 更新圈的坐标
            new_top = top - 1 if can_expand_top else top
            new_right = right + 1 if can_expand_right else right
            new_bottom = bottom + 1 if can_expand_bottom else bottom
            new_left = left - 1 if can_expand_left else left
            
            # 检查是否有任何一条边扩散
            if (new_top != top or new_right != right or new_bottom != bottom or new_left != left):
                # 清除旧的圈
                clear_old_circle(output_matrix, top, left, bottom, right)
                # 绘制新的圈
                draw_circle(output_matrix, new_top, new_left, new_bottom, new_right)
                any_expanded = True
                # 更新圈的坐标
                circles[circle_idx] = (new_top, new_left, new_bottom, new_right)
            else:
                # 该圈不能再扩散
                can_expand[circle_idx] = False
            
        # 如果没有圈能够继续扩散，则退出循环
        if not any_expanded:
            break
    
    return output_matrix

def generate_random_blocks(matrix, num_blocks):
    """在矩阵中随机放置统一大小和颜色的色块"""
    rows, cols = len(matrix), len(matrix[0])
    blocks_placed = 0
    
    # 设置统一的块大小
    block_height = 3  # 统一高度
    block_width = 2   # 统一宽度
    
    # 设置统一的颜色为蓝色
    color = 1  # 1对应蓝色 (0, 116, 217)
    
    while blocks_placed < num_blocks:
        # 随机选择位置
        start_row = random.randint(0, rows - block_height)
        start_col = random.randint(0, cols - block_width)
        
        # 检查是否可以放置
        can_place = True
        for i in range(start_row, min(start_row + block_height, rows)):
            for j in range(start_col, min(start_col + block_width, cols)):
                if matrix[i][j] != 0:
                    can_place = False
                    break
            if not can_place:
                break
        
        # 放置色块
        if can_place:
            for i in range(start_row, min(start_row + block_height, rows)):
                for j in range(start_col, min(start_col + block_width, cols)):
                    matrix[i][j] = color
            blocks_placed += 1

def generate_circle_pairs(rows, cols, num_blocks, num_circles):
    """生成包含随机色块和黄圈的初始矩阵，以及扩散后的目标矩阵"""
    # 创建原始矩阵
    input_matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    
    # 添加随机色块
    generate_random_blocks(input_matrix, num_blocks)
    
    # 添加空心黄圈并记录顶点坐标
    circles = []
    circles_placed = 0
    max_attempts = 10000  # 增加尝试次数
    attempts = 0
    
    while circles_placed < num_circles and attempts < max_attempts:
        # 随机选择圈的大小和位置
        circle_size = random.randint(3, 6)
        start_row = random.randint(0, rows - circle_size)
        start_col = random.randint(0, cols - circle_size)
        
        # 尝试放置圈
        temp_matrix = copy.deepcopy(input_matrix)
        vertices = create_hollow_circle(temp_matrix, circle_size, start_row, start_col)
        
        if vertices:
            # 检查这个新圈扩散后是否会与已有圈重叠
            if not circles or not would_circles_overlap(input_matrix, circles, vertices):
                # 在实际矩阵中放置圈
                create_hollow_circle(input_matrix, circle_size, start_row, start_col)
                circles.append(vertices)
                circles_placed += 1
        
        attempts += 1
    
    if attempts >= max_attempts:
        print(f"无法放置足够数量")
    
    # 如果无法放置所需数量的圈，至少确保有一个圈
    if circles_placed == 0 and num_circles > 0:
        # 尝试放置至少一个圈
        for _ in range(1000):  # 大量尝试以确保至少放置一个圈
            circle_size = random.randint(3, 5)
            start_row = random.randint(0, rows - circle_size)
            start_col = random.randint(0, cols - circle_size)
            
            vertices = create_hollow_circle(input_matrix, circle_size, start_row, start_col)
            if vertices:
                circles.append(vertices)
                circles_placed = 1
                break
    
    # 扩散黄圈生成目标矩阵
    output_matrix = expand_circle(input_matrix, circles)
    
    return input_matrix, output_matrix

def visualize_grid(grid, save_dir_pic, save_dir_dt, file_name, image_size=500):
    """将网格可视化为图像并保存"""
    rows, cols = len(grid), len(grid[0])
    cell_size = image_size // max(rows, cols)  
    img_width, img_height = cols * cell_size, rows * cell_size  
    image = Image.new('RGB', (img_width, img_height), WHITE)
    draw = ImageDraw.Draw(image)
    grid_line_color = (200, 200, 200)
    
    for i in range(rows):
        for j in range(cols):
            color_key = str(grid[i][j])
            color = color_table.get(color_key, WHITE)
            left = j * cell_size
            top = i * cell_size
            right = left + cell_size - 1
            bottom = top + cell_size - 1
            draw.rectangle([left, top, right, bottom], fill=color, outline=grid_line_color)
    
    os.makedirs(save_dir_pic, exist_ok=True)
    os.makedirs(save_dir_dt, exist_ok=True)
    timestamp = int(time.time())
    save_path = os.path.join(save_dir_pic, f"{file_name}_{idx}.png")
    save_path_2 = os.path.join(save_dir_dt, f"{file_name}_{idx}.json")
    image.save(save_path)
    print(f"保存图像: {save_path}")
    with open(save_path_2,"w") as f: 
        json.dump(convert_int(grid), f, indent=4)

# 主程序：生成数据集
rows, cols = 30, 30  # 矩阵大小为20x30

# 生成不同数量和圈的组合
num_blocks = 20
for num_circles in range(5, 6):  
    idx = 19
    for sample_idx in range(0, 7):  # 每种组合生成10个样本
        # time.sleep(1)  # 确保时间戳不同
        input_matrix, output_matrix = generate_circle_pairs(rows, cols, num_blocks, num_circles)
        
        file_name = f'circle_expand'
        save_dir_pic_input = f'pictures/circles={num_circles}'
        save_dir_data_input = f'data/circles={num_circles}'
        save_dir_pic_output = f'pictures_gt/circles={num_circles}'
        save_dir_data_output = f'data_gt/circles={num_circles}'
        
        visualize_grid(input_matrix, save_dir_pic_input, save_dir_data_input, file_name)
        visualize_grid(output_matrix, save_dir_pic_output, save_dir_data_output, file_name)
        idx += 1