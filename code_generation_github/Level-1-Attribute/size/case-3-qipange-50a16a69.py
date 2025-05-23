import numpy as np
import matplotlib.pyplot as plt
import random
import os
import json

# 自定义颜色表
color_table = {
    '0' : (0, 0, 0),
    '1' : (0, 116, 217),
    '2' : (255, 65, 54),
    '3' : (46, 204, 64),
    '4': (255, 220, 0),
    '5': (170, 170, 170),
    '6': (240, 18, 190),
    '7': (255, 133, 27),
    '8': (127, 219, 255),
    '9': (135, 12, 37),
}
WHITE = (255, 255, 255)
GRAY = (161, 161, 161)

def generate_fixed_checkerboard(grid_size, pattern_size, used_colors, override_color, x=3):
    base_binary = (np.indices((pattern_size, pattern_size)).sum(axis=0) % 2)
    color_map = np.vectorize(lambda v: used_colors[v])
    base_tile = color_map(base_binary)
    repeat_x = int(np.ceil(grid_size / pattern_size))
    repeat_y = int(np.ceil(grid_size / pattern_size))
    tiled = np.tile(base_tile, (repeat_y, repeat_x))
    full_matrix = tiled[:grid_size, :grid_size].astype(int)

    # ✅ 保存未替换的原始棋盘
    matrix_before_override = full_matrix.copy()

    # ✅ 替换右下角
    full_matrix[-x:, :] = override_color
    full_matrix[:, -x:] = override_color

    return full_matrix, matrix_before_override

def matrix_to_rgb(matrix):
    h, w = matrix.shape
    rgb_image = np.zeros((h, w, 3), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            val = str(matrix[i, j])
            rgb_image[i, j] = color_table[val]
    return rgb_image



if __name__ == "__main__":
    # 参数
    num_groups = 10
    pattern_size = 2
    x = 1
    size_range = range(5, 30)
    grouped_by_size = {size: [] for size in size_range}

    # 多组生成（颜色不能为0）
    for group_id in range(num_groups):
        # 棋盘格颜色从 1~9 中选两个
        used_colors = random.sample(range(1, 10), 2)

        # override color 从剩余非0的数中选
        override_color = random.choice(list(set(range(1, 10)) - set(used_colors)))
        
        for size in size_range:
            matrix, original_matrix = generate_fixed_checkerboard(
                grid_size=size,
                pattern_size=pattern_size,
                used_colors=used_colors,
                override_color=override_color,
                x=x
            )
            grouped_by_size[size].append({
                'matrix': matrix,
                'original': original_matrix,  # ✅ 新增保存未替换的版本
                'used_colors': tuple(used_colors),
                'override_color': override_color,
                'group_id': group_id
            })


    # 输出：按 size 分组，每组输出所有矩阵
    for size in size_range:
        print(f"\n====== Grid Size {size}x{size} ======")
        for idx, data in enumerate(grouped_by_size[size]):
            print(f"\n[Group {data['group_id']}] Colors: {data['used_colors']} | Override: {data['override_color']}")
            # print("input Matrix:")
            # print(data['matrix'])
            # print("Output Matrix:")
            # print(data['original'])
            
            test_json_sample= {
                    "test": {
                            "input":  data['matrix'].tolist(),
                            "output": data['original'].tolist()
                            }
                        }
            
            per_size_folder_name = os.path.join("/mnt/petrelfs/yangyue/continuous_evaluation/continous_change_input/grid_size/50a16a69/data", f'qipange_size_{size}_{size}')
            os.makedirs(per_size_folder_name, exist_ok=True)
            
            with open(f"{per_size_folder_name}/index_{data['group_id']+1}_masked_{x}_size_{size}_{size}.json", "w", encoding="utf-8") as f:
                json.dump(test_json_sample, f, ensure_ascii=False, indent=4)
