import numpy as np
import random
import json
import numpy as np
import matplotlib.pyplot as plt
import random
import os
import json

# 颜色值表（你提供的）
color_table = {
    '0': (0, 0, 0),
    '1': (0, 116, 217),     # 蓝色
    '2': (255, 65, 54),     # 红色
    '3': (46, 204, 64),     # 绿色
    '4': (255, 220, 0),     # 黄色
    '5': (170, 170, 170),   # 灰色
    '6': (240, 18, 190),    # 紫红
    '7': (255, 133, 27),    # 橙色
    '8': (127, 219, 255),   # 浅蓝
    '9': (135, 12, 37),     # 暗红
}

def generate_origianl_matrix(n=30):
    # 参数设定
    # n = 28             # 矩阵尺寸
    border = 2         # 固定边框的行列数
    border_top_color = 1  # 顶部蓝色
    border_left_color = 4  # 左侧黄色

    # 从 0-9 中随机选 4 种颜色（排除 1 和 4）
    available_colors = [i for i in range(1, 10) if i not in [border_top_color, border_left_color]]
    cycle_colors = random.sample(available_colors, 4)

    # 初始化矩阵
    matrix = np.zeros((n, n), dtype=int)

    # 填充前三行与前三列
    matrix[:border, :] = border_top_color
    matrix[:, :border] = border_top_color

    row, col = 2, 2  # 第三行第三列
    for j in range(matrix.shape[1]):
        if matrix[row, j] != border_top_color:
            matrix[row, j] = border_left_color
    for i in range(matrix.shape[0]):
        if matrix[i, col] != border_top_color:
            matrix[i, col] = border_left_color

    # 填充剩余区域
    for i in range(border + 1, n):
        for j in range(border + 1, n):
            idx = (i + j) % len(cycle_colors)
            matrix[i][j] = cycle_colors[idx]


    return matrix

# with open("/mnt/petrelfs/yangyue/continuous_evaluation/arc-dsl/dsl_change_input/object/4aab4007.json", "r") as f:
#     data = json.load(f)
    
# matrix = data["train"][1]["output"]

# matrix= [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], [1, 1, 4, 3, 2, 1, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7], [1, 1, 4, 2, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9], [1, 1, 4, 1, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2], [1, 1, 4, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4], [1, 1, 4, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6], [1, 1, 4, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8], [1, 1, 4, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1], [1, 1, 4, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3], [1, 1, 4, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5], [1, 1, 4, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7], [1, 1, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9], [1, 1, 4, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2], [1, 1, 4, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4], [1, 1, 4, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6], [1, 1, 4, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8], [1, 1, 4, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1], [1, 1, 4, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3], [1, 1, 4, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5], [1, 1, 4, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7], [1, 1, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9], [1, 1, 4, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2], [1, 1, 4, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4], [1, 1, 4, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6], [1, 1, 4, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8], [1, 1, 4, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1, 3, 5, 7, 9, 2, 4, 6, 8, 1]]



def generate_object_in_region(r_start, c_start, r_end, c_end, min_obj, max_obj):
    """
    在区域 [r_start, r_end] x [c_start, c_end] 内生成一个随机连通物体。
    物体大小随机，在 [min_obj, max_obj] 之间（即物体包含的单元格数）。
    使用随机生长方法：
      1. 随机选择区域内的一个起始单元。
      2. 重复：收集物体边界（物体���任一单元的4邻域中，位于区域内且尚未加入物体的单元），
         随机从中选取一个加入物体，直到物体达到预设目标大小或无法扩展。
    返回：
      object_set: 该物体的单元格位置集合，集合中每个元素为 (r, c)。
    """
    rows = r_end - r_start + 1
    cols = c_end - c_start + 1
    target_size = random.randint(min_obj, max_obj)
    
    # 随机选取区域内的起始单元
    start_r = random.randint(r_start, r_end)
    start_c = random.randint(c_start, c_end)
    obj = {(start_r, start_c)}
    
    def get_border_cells():
        border = set()
        for (r, c) in obj:
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = r + dr, c + dc
                if r_start <= nr <= r_end and c_start <= nc <= c_end:
                    if (nr, nc) not in obj:
                        border.add((nr, nc))
        return border
    
    while len(obj) < target_size:
        border = list(get_border_cells())
        if not border:
            break
        cell = random.choice(border)
        obj.add(cell)
    
    return obj

def mask_random_objects(x, n,
                        min_region_height=3, min_region_width=3,
                        max_region_height=8, max_region_width=8,
                        min_obj=3, max_obj=15,
                        max_attempts=1000):
    """
    对给定矩阵 x（numpy 数组），随机挑选 n 个不重叠的矩形区域，
    然后在每个区域内生成一个随机连通物体（使用随机生长方法），
    最后将这些物体所在位置置为 0（“mask”）。
    
    为了避免两个区域的边界直接相邻（从而导致区域内生成的0连通成一个整体），
    在选取区域时会对区域扩展1个像素作为保护区，要求保护区不与已选区域重叠。
    
    参数:
      x: 2D numpy 数组（不改变原矩阵，返回拷贝）
      n: 要生成的物体个数（对应 n ���不重叠的区域）
      min_region_height, min_region_width: 区域随机尺寸的最小值
      max_region_height, max_region_width: 区域随机尺寸的最大值
      min_obj, max_obj: 每个物体的最小与最大单元格数（连通区域大小）
      max_attempts: 尝试生成不重叠区域的最大次数
      
    返回:
      masked: 处理后的矩阵（numpy 数组）
      regions: 一个列表，每个元素是一个字典，包含区域信息和生成的物体位置：
         {
           'region': (r_start, c_start, r_end, c_end),
           'object': set((r, c), ...)
         }
    """
    masked = x.copy()
    rows, cols = masked.shape
    # 用一个布尔矩阵记录哪些单元格已被区域（含保护区）占用
    used = np.zeros_like(masked, dtype=bool)
    regions_info = []
    count = 0
    attempts = 0
    while count < n and attempts < max_attempts:
        attempts += 1
        # 随机生成区域尺寸（保证尺寸不超过矩阵）
        region_height = random.randint(min_region_height, min(max_region_height, rows))
        region_width  = random.randint(min_region_width, min(max_region_width, cols))
        # 随机选择区域左上角位置，保证区域在矩阵内
        r_start = random.randint(0, rows - region_height)
        c_start = random.randint(0, cols - region_width)
        r_end = r_start + region_height - 1
        c_end = c_start + region_width - 1
        
        # 计算保护区（扩展区域）：扩展1个像素，受矩阵边界限制
        ext_r_start = max(0, r_start - 1)
        ext_c_start = max(0, c_start - 1)
        ext_r_end = min(rows - 1, r_end + 1)
        ext_c_end = min(cols - 1, c_end + 1)
        
        # 检查扩展区域是否与已有区域重叠
        if np.any(used[ext_r_start:ext_r_end+1, ext_c_start:ext_c_end+1]):
            continue
        
        # 合法区域，标记扩展区域为已占用
        used[ext_r_start:ext_r_end+1, ext_c_start:ext_c_end+1] = True
        
        # 在原始区域内生成随机连通物体
        obj = generate_object_in_region(r_start, c_start, r_end, c_end, min_obj, max_obj)
        
        # 将物体所在位置置为 0（mask）
        for (r, c) in obj:
            masked[r, c] = 0
        
        regions_info.append({
            'region': (r_start, c_start, r_end, c_end),
            'object': obj
        })
        count += 1
        attempts = 0  # 成功生成后重置尝试次数
        
    if count < n:
        print(f"仅生成了 {count} 个不重叠区域（目标 {n} 个）")
    return masked, regions_info

# 示例调用
if __name__ == "__main__":
    # 构造一个示例 20x20 矩阵，初始全部为 1

    for index in range(1, 11):
        matrix =generate_origianl_matrix(30)
        x = np.array(matrix)
        
        num_rows = len(x)
        num_cols = len(x[0])
        print(num_rows, num_cols)
        # print("原始矩阵：")
        # print(x)
        
        for k in range(1, 20):
            half_rows = num_rows - k  # 或任意你想缩小的尺寸
            half_cols = num_cols - k

            
            # 取前一半的行和前一半的列
            reduced_matrix = x[:half_rows, :half_cols]
            # print(f"length:{half_rows}")
            print(len(reduced_matrix), len(reduced_matrix[0]))
            print(reduced_matrix)
            x = reduced_matrix
            
            mask_num = 1
            # 随机生成 3 个物体区域，每个区域内部随机生成一个连通的物体（mask 置为 0）
            masked_matrix, regions = mask_random_objects(x, n=mask_num,
                                                        min_region_height=3, min_region_width=3,
                                                        max_region_height=5, max_region_width=5,
                                                        min_obj=8, max_obj=9)
            
            test_json_sample= {
                        "test": {
                                "input":  masked_matrix.tolist(),
                                "output": reduced_matrix.tolist()
                                }
                            }
            
            per_size_folder_name = os.path.join("/mnt/petrelfs/yangyue/continuous_evaluation/continous_change_input/grid_size/4aab4007/data_1", f'denosing_size_{half_rows}_{half_cols}')
            os.makedirs(per_size_folder_name, exist_ok=True)
            
            with open(f"{per_size_folder_name}/index_{index}_mask_{mask_num}_size_{half_rows}_{half_cols}.json", "w", encoding="utf-8") as f:
                json.dump(test_json_sample, f, ensure_ascii=False, indent=4)
            
            # print("Mask 后的矩阵：")
            # print(masked_matrix)
        # 打印矩阵（可选）
        # for row in masked_matrix:
        #     print(row)

        # with open(f"/mnt/petrelfs/yangyue/continuous_evaluation/arc-dsl/dsl_change_input/grid_size/4aab4007/variants/masked_{mask_num}_reduce_{k}.json", "w", encoding="utf-8") as f:
        #     json.dump(masked_matrix.tolist(), f, ensure_ascii=False, indent=4)