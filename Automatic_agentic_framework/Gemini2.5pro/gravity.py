import numpy as np
import random

# --- 1. 定义场景参数 ---
HEIGHT = 10
WIDTH = 20
GROUND_COLOR = 1

def create_initial_scene(num_objects):
    """
    创建带有地面和待下落色块的初始矩阵。

    参数:
    - num_objects (int): 要生成的3x1矩形元素的数量。

    返回:
    - tuple: (初始矩阵, 包含色块信息的列表, 包含地面高度信息的字典)
    """
    # 创建一个空白画布
    grid = np.zeros((HEIGHT, WIDTH), dtype=int)
    
    # --- 绘制起伏的地面 ---
    # ground_top_levels 用来记录每一列的地面最高点的y坐标
    ground_top_levels = {}
    for x in range(WIDTH):
        # 随机决定地面的高度（从底部算起，1到4行高）
        ground_height = random.randint(1, 4)
        # 计算地面最高点的y坐标
        top_y = HEIGHT - ground_height
        # 填充地面颜色
        grid[top_y:, x] = GROUND_COLOR
        ground_top_levels[x] = top_y

    # --- 在顶部绘制3x1的色块 ---
    # objects_to_fall 用来记录每个色块的颜色和初始x坐标
    objects_to_fall = []
    
    # 获取所有可以放置色块的列（为了避免重叠）
    available_columns = list(range(WIDTH))
    random.shuffle(available_columns)
    
    # 放置指定数量的色块
    count = 0
    while count < num_objects and available_columns:
        # 从可用列中弹出一个
        x = available_columns.pop()
        
        # 检查此列是否有足够空间让3x1的色块落下
        # 色块高度为3，所以地面最高点y坐标至少要为3 (即y=0,1,2为空)
        if ground_top_levels[x] < 3:
            continue # 空间不足，跳过此列

        # 随机生成3种颜色 (范围2-9，不包含地面颜色1)
        colors = np.random.randint(2, 10, size=3)
        
        # 在顶部放置色块
        grid[0:3, x] = colors
        
        # 记录色块信息
        objects_to_fall.append({'colors': colors, 'x': x})
        count += 1

    return grid, objects_to_fall, ground_top_levels

def apply_gravity(objects_info, ground_levels):
    """
    根据重力规则，计算并生成色块落地后的最终矩阵。

    参数:
    - objects_info (list): 包含色块颜色和x坐标的列表。
    - ground_levels (dict): 包含每列地面最高点y坐标的字典。

    返回:
    - np.ndarray: 模拟重力后的最终矩阵。
    """
    # 创建一个只有地面的新画布
    final_grid = np.zeros((HEIGHT, WIDTH), dtype=int)
    for x, top_y in ground_levels.items():
        final_grid[top_y:, x] = GROUND_COLOR
        
    # 将每个色块放置到其最终的“落地”位置
    for obj in objects_info:
        x = obj['x']
        colors = obj['colors']
        
        # 获取该列地面的最高点y坐标
        ground_top_y = ground_levels[x]
        
        # 计算落地后色块的起始y坐标
        # 色块最低端(y+2)要停在 ground_top_y - 1 的位置
        # 所以色块最高端(y)的位置是 ground_top_y - 3
        landing_start_y = ground_top_y - 3
        
        # 将色块绘制到最终位置
        final_grid[landing_start_y : landing_start_y + 3, x] = colors
        
    return final_grid

# --- 2. 主程序 ---
if __name__ == "__main__":
    
    # ================================================
    # == 在这里控制天上3x1色块的数量 (例如，设置为8) ==
    NUMBER_OF_OBJECTS = 8
    # ================================================

    # 步骤1: 创建初始场景
    initial_matrix, objects, ground_info = create_initial_scene(NUMBER_OF_OBJECTS)
    
    print("--- 初始矩阵 ---")
    print("地面由1表示，上方是待下落的色块:")
    print(initial_matrix)
    
    # 步骤2: 模拟重力，生成变化后的矩阵
    final_matrix = apply_gravity(objects, ground_info)
    
    print("\n--- 变化后的矩阵1 (模拟重力后) ---")
    print("色块已落在地面上:")
    print(final_matrix)