import numpy as np
import os
import json

def generate_filled_matrix(n, blue_value, black_value=0):
    """
    生成一个 n x n 的矩阵，按照规则：
    - 先全部填充为 blue_value
    - 然后对于所有 (i, j) 满足 i % 2 == 1 且 j % 2 == 1 的位置，
      将其置为 black_value（0）
    """
    # 创建全部填充为 blue_value 的矩阵
    filled = np.full((n, n), blue_value, dtype=int)
    # 对于满足条件的位置填入 black_value
    for i in range(n):
        for j in range(n):
            if i % 2 == 1 and j % 2 == 1:
                filled[i, j] = black_value
    return filled

# 存放结果的字典，每个 n 对应一个列表，每个列表中是多个 pair（原始矩阵, 填充后的矩阵）
results_by_size = {}

for n in range(5, 30, 2):  # n从5到15，只取奇数
    pair_list = []
    for blue_value in range(1, 10):  # blue_value从1到9
        # 原始全0矩阵
        original = np.zeros((n, n), dtype=int)
        original[0][0] = blue_value
        # 根据规则生成填充矩阵
        filled = generate_filled_matrix(n, blue_value, black_value=0)
        pair_list.append({
            'blue_value': blue_value,
            'original': original,
            'filled': filled
        })
    results_by_size[n] = pair_list

# 逐个输出所有结果
for n, pairs in results_by_size.items():
    print(f"\n====== Matrix Size: {n}x{n} ======")
    
    for pair in pairs:
        print(f"\n[Blue Value: {pair['blue_value']}]")
        # print("原始全0矩阵:")
        # print(pair['original'])
        # print("填充后的矩阵:")
        # print(pair['filled'])
    
        test_json_sample= {
                        "test": {
                                "input":  pair['original'].tolist(),
                                "output": pair['filled'].tolist()
                                }
                            }
            
        per_size_folder_name = os.path.join("/mnt/petrelfs/yangyue/continuous_evaluation/continous_change_input/grid_size/332efdb3/data", f'fill_empty_size_{n}_{n}')
        os.makedirs(per_size_folder_name, exist_ok=True)
        
        with open(f"{per_size_folder_name}/index_{pair['blue_value']}_color_{pair['blue_value']}_size_{n}_{n}.json", "w", encoding="utf-8") as f:
            json.dump(test_json_sample, f, ensure_ascii=False, indent=4)
