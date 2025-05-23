# import random
# import json
# from PIL import Image
# import matplotlib.pyplot as plt
# from pathlib import Path
import os



# # 配色表
# color_table = {
#     '0': (0, 0, 0),            # 背景
#     '1': (0, 116, 217),        # 蓝色目标
#     '2': (255, 65, 54),        # 红色起点
#     '7': (255, 133, 27),       # 橙色路径
# }

# def draw_grid(grid, cell_size=20):
#     H, W = len(grid), len(grid[0])
#     img = Image.new('RGB', (W * cell_size, H * cell_size), (0, 0, 0))
#     for i in range(H):
#         for j in range(W):
#             color = color_table.get(str(grid[i][j]), (0, 0, 0))
#             for dx in range(cell_size):
#                 for dy in range(cell_size):
#                     img.putpixel((j * cell_size + dx, i * cell_size + dy), color)
#     return img

# def manhattan(p1, p2):
#     return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# def is_valid_new_point(x, y, H, W, used):
#     if not (0 <= x < H and 0 <= y < W):
#         return False
#     for ux, uy in used:
#         if manhattan((x, y), (ux, uy)) < 2:
#             return False
#     return True

# def draw_path(grid, start, end):
#     sx, sy = start
#     ex, ey = end
#     if sx == ex:
#         for y in range(min(sy, ey) + 1, max(sy, ey)):
#             grid[sx][y] = 7
#     elif sy == ey:
#         for x in range(min(sx, ex) + 1, max(sx, ex)):
#             grid[x][sy] = 7
#     return grid

# def generate_stepwise_pairs(H=15, W=15, steps=9):
#     grid = [[0 for _ in range(W)] for _ in range(H)]
#     red = (random.randint(3, H - 4), random.randint(3, W - 4))
#     grid[red[0]][red[1]] = 2
#     used = set()
#     used.add(red)
#     current_tip = red
#     directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

#     stepwise_pairs = []
#     input_grid = [[0 for _ in range(W)] for _ in range(H)]
#     input_grid[red[0]][red[1]] = 2

#     for step in range(steps):
#         found = False
#         attempts = 0
#         while not found and attempts < 200:
#             dx, dy = random.choice(directions)
#             dist = random.randint(2, 5)
#             nx, ny = current_tip[0] + dx * dist, current_tip[1] + dy * dist
#             if is_valid_new_point(nx, ny, H, W, used):
#                 draw_path(grid, current_tip, (nx, ny))
#                 for i in range(1, dist):
#                     px, py = current_tip[0] + dx * i, current_tip[1] + dy * i
#                     grid[px][py] = 7
#                     used.add((px, py))
#                 grid[nx][ny] = 1
#                 used.add((nx, ny))
#                 input_grid[nx][ny] = 1
#                 current_tip = (nx, ny)
#                 found = True
#             attempts += 1

#         stepwise_pairs.append({
#             "step": step + 1,
#             "input": [row[:] for row in input_grid],
#             "output": [row[:] for row in grid],
#         })

#     return stepwise_pairs

# # 保存 JSON（带 step 字段，字典结构）
# def save_as_json_with_step_dict(pairs, path):
#     stepwise_dict = {}
#     for p in pairs:
#         stepwise_dict[f"step_{p['step']}"] = p
#     with open(path, "w") as f:
#         json.dump(stepwise_dict, f, indent=2)

# # 拼接图像保存为 .jpg
# def save_combined_visualization(pairs, out_path="stepwise_combined.jpg"):
#     fig, axs = plt.subplots(3, 3, figsize=(12, 12))
#     for i in range(min(9, len(pairs))):
#         img = draw_grid(pairs[i]["output"])
#         axs[i // 3][i % 3].imshow(img)
#         axs[i // 3][i % 3].set_title(f"Step {i+1}")
#         axs[i // 3][i % 3].axis("off")
#     plt.tight_layout()
#     fig.savefig(out_path)
#     plt.close(fig)

# # 主执行函数
# if __name__ == "__main__":
#     pairs = generate_stepwise_pairs()
#     save_as_json_with_step_dict(pairs, "stepwise_path_pairs.json")
#     save_combined_visualization(pairs, "stepwise_combined.jpg")
#     print("✅ 已保存：stepwise_path_pairs.json + stepwise_combined.jpg")




# import random
# import json
# from PIL import Image
# import matplotlib.pyplot as plt

# # ====== 配色表 ======
# color_table = {
#     '0': (0, 0, 0),            # 背景
#     '1': (0, 116, 217),        # 蓝色目标
#     '2': (255, 65, 54),        # 红色起点
#     '7': (255, 133, 27),       # 橙色路径
# }

# # ====== 可视化函数 ======
# def draw_grid(grid, cell_size=20):
#     H, W = len(grid), len(grid[0])
#     img = Image.new('RGB', (W * cell_size, H * cell_size), (0, 0, 0))
#     for i in range(H):
#         for j in range(W):
#             color = color_table.get(str(grid[i][j]), (0, 0, 0))
#             for dx in range(cell_size):
#                 for dy in range(cell_size):
#                     img.putpixel((j * cell_size + dx, i * cell_size + dy), color)
#     return img

# # ====== 距离检查 ======
# def manhattan(p1, p2):
#     return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# def is_valid_new_point(x, y, H, W, used):
#     if not (0 <= x < H and 0 <= y < W):
#         return False
#     for ux, uy in used:
#         if manhattan((x, y), (ux, uy)) < 2:
#             return False
#     return True

# # ====== 主函数（严格直线路径构建） ======
# def generate_stepwise_pairs(H=15, W=15, steps=9, seed=None):
#     if seed is not None:
#         random.seed(seed)

#     grid = [[0 for _ in range(W)] for _ in range(H)]
#     red = (random.randint(3, H - 4), random.randint(3, W - 4))
#     grid[red[0]][red[1]] = 2
#     blues = []
#     used = {red}  # 所有用过的格子（红、蓝、路径）

#     stepwise_pairs = []

#     for step in range(steps):
#         found = False
#         attempts = 0
#         while not found and attempts < 500:
#             dx, dy = random.choice([(-1,0), (1,0), (0,-1), (0,1)])
#             dist = random.randint(2, 5)
#             last = blues[-1] if blues else red
#             nx, ny = last[0] + dx * dist, last[1] + dy * dist
#             candidate = (nx, ny)
#             if not (0 <= nx < H and 0 <= ny < W):
#                 attempts += 1
#                 continue
#             if candidate in used or not is_valid_new_point(nx, ny, H, W, used):
#                 attempts += 1
#                 continue

#             # 检查路径中是否有冲突
#             path = []
#             conflict = False
#             if last[0] == nx:
#                 for y in range(min(last[1], ny) + 1, max(last[1], ny)):
#                     pt = (nx, y)
#                     if pt in used:
#                         conflict = True
#                         break
#                     path.append(pt)
#             elif last[1] == ny:
#                 for x in range(min(last[0], nx) + 1, max(last[0], nx)):
#                     pt = (x, ny)
#                     if pt in used:
#                         conflict = True
#                         break
#                     path.append(pt)
#             else:
#                 attempts += 1
#                 continue  # 非直线

#             if not conflict:
#                 blues.append(candidate)
#                 for pt in path:
#                     used.add(pt)
#                 used.add(candidate)
#                 found = True
#             attempts += 1

#         # === 构建 input grid ===
#         input_grid = [[0 for _ in range(W)] for _ in range(H)]
#         input_grid[red[0]][red[1]] = 2
#         for bx, by in blues:
#             input_grid[bx][by] = 1

#         # === 构建 output grid ===
#         output_grid = [row[:] for row in input_grid]
#         current = red
#         for blue in blues:
#             if current[0] == blue[0]:
#                 for y in range(min(current[1], blue[1]) + 1, max(current[1], blue[1])):
#                     output_grid[current[0]][y] = 7
#             elif current[1] == blue[1]:
#                 for x in range(min(current[0], blue[0]) + 1, max(current[0], blue[0])):
#                     output_grid[x][current[1]] = 7
#             current = blue

#         stepwise_pairs.append({
#             "step": step + 1,
#             "input": input_grid,
#             "output": output_grid
#         })

#     return stepwise_pairs

# # ====== JSON 保存 ======
# def save_as_json_with_step_dict(pairs, path):
#     stepwise_dict = {}
#     for p in pairs:
#         stepwise_dict[f"step_{p['step']}"] = p
#     with open(path, "w") as f:
#         json.dump(stepwise_dict, f, indent=2)

# # ====== 拼图保存 ======
# def save_combined_visualization(pairs, out_path="stepwise_combined.jpg"):
#     fig, axs = plt.subplots(3, 3, figsize=(12, 12))
#     for i in range(min(9, len(pairs))):
#         img = draw_grid(pairs[i]["output"])
#         axs[i // 3][i % 3].imshow(img)
#         axs[i // 3][i % 3].set_title(f"Step {i+1}")
#         axs[i // 3][i % 3].axis("off")
#     plt.tight_layout()
#     fig.savefig(out_path)
#     plt.close(fig)

# # ====== 运行入口 ======
# if __name__ == "__main__":
#     seed = None  # 设置为 None 表示随机
#     pairs = generate_stepwise_pairs(seed=seed)
#     save_as_json_with_step_dict(pairs, "stepwise_path_pairs.json")
#     save_combined_visualization(pairs, "stepwise_combined.jpg")
#     print("✅ 已保存：stepwise_path_pairs.json + stepwise_combined.jpg")
#     print(f"📌 使用随机种子: {seed}")




# import random
# import json
# from itertools import permutations
# from PIL import Image
# import matplotlib.pyplot as plt

# # ===== 配色 =====
# color_table = {
#     '0': (0, 0, 0),            # 背景
#     '1': (0, 116, 217),        # 蓝色目标
#     '2': (255, 65, 54),        # 红色起点
#     '7': (255, 133, 27),       # 橙色路径
# }

# def draw_grid(grid, cell_size=20):
#     H, W = len(grid), len(grid[0])
#     img = Image.new('RGB', (W * cell_size, H * cell_size), (0, 0, 0))
#     for i in range(H):
#         for j in range(W):
#             color = color_table.get(str(grid[i][j]), (0, 0, 0))
#             for dx in range(cell_size):
#                 for dy in range(cell_size):
#                     img.putpixel((j * cell_size + dx, i * cell_size + dy), color)
#     return img

# def valid_straight_path(a, b, used):
#     ax, ay = a
#     bx, by = b
#     path = []
#     if ax == bx:
#         for y in range(min(ay, by) + 1, max(ay, by)):
#             if (ax, y) in used:
#                 return []
#             path.append((ax, y))
#     elif ay == by:
#         for x in range(min(ax, bx) + 1, max(ax, bx)):
#             if (x, ay) in used:
#                 return []
#             path.append((x, ay))
#     else:
#         return []
#     return path

# def find_best_order(start, blues, used):
#     best_order = None
#     best_len = float('inf')
#     for perm in permutations(blues):
#         curr = start
#         total_len = 0
#         temp_used = set(used)
#         valid = True
#         for pt in perm:
#             segment = valid_straight_path(curr, pt, temp_used)
#             if not segment:
#                 valid = False
#                 break
#             total_len += len(segment)
#             temp_used.update(segment)
#             temp_used.add(pt)
#             curr = pt
#         if valid and total_len < best_len:
#             best_order = perm
#             best_len = total_len
#     return best_order

# def is_valid_new_point(x, y, used, H, W):
#     if not (0 <= x < H and 0 <= y < W):
#         return False
#     for ux, uy in used:
#         if abs(x - ux) + abs(y - uy) < 2:
#             return False
#     return True

# def generate_stepwise_pairs(H=15, W=15, steps=9, seed=42, max_dist=5):
#     if seed is not None:
#         random.seed(seed)

#     red = (random.randint(3, H - 4), random.randint(3, W - 4))
#     blues = []
#     used = {red}
#     pairs = []

#     while len(pairs) < steps:
#         # 生成一个候选蓝点
#         valid_blue = None
#         for attempt in range(500):
#             dx, dy = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
#             dist = random.randint(2, max_dist)
#             last = blues[-1] if blues else red
#             nx, ny = last[0] + dx * dist, last[1] + dy * dist
#             candidate = (nx, ny)
#             if is_valid_new_point(nx, ny, used, H, W) and candidate not in blues:
#                 blues.append(candidate)
#                 used.add(candidate)
#                 valid_blue = candidate
#                 break

#         if valid_blue is None:
#             continue

#         # 最优路径连接顺序
#         order = find_best_order(red, blues, used - set(blues))
#         if not order:
#             blues.pop()
#             used.remove(valid_blue)
#             continue

#         # 构建 input grid
#         input_grid = [[0 for _ in range(W)] for _ in range(H)]
#         input_grid[red[0]][red[1]] = 2
#         for bx, by in blues:
#             input_grid[bx][by] = 1

#         # 构建 output grid
#         output_grid = [row[:] for row in input_grid]
#         curr = red
#         path_used = {red}
#         for pt in order:
#             segment = valid_straight_path(curr, pt, path_used)
#             for px, py in segment:
#                 output_grid[px][py] = 7
#                 path_used.add((px, py))
#             path_used.add(pt)
#             curr = pt

#         pairs.append({
#             "step": len(pairs),
#             "input": input_grid,
#             "output": output_grid
#         })

#     return pairs

# def save_as_json_with_step_dict(pairs, path):
#     stepwise_dict = {}
#     for p in pairs:
#         stepwise_dict[f"step_{p['step']}"] = p
#     with open(path, "w") as f:
#         json.dump(stepwise_dict, f, indent=2)

# def save_combined_visualization(pairs, out_path="stepwise_combined.jpg"):
#     fig, axs = plt.subplots(3, 3, figsize=(12, 12))
#     for i in range(9):
#         ax = axs[i // 3][i % 3]
#         if i < len(pairs):
#             img = draw_grid(pairs[i]["output"])
#             ax.imshow(img)
#             ax.set_title(f"Step {i+1}")
#         ax.axis("off")
#     plt.tight_layout()
#     fig.savefig(out_path)
#     plt.close(fig)

# if __name__ == "__main__":
#     seed = None  # 设置为 None 表示完全随机
#     pairs = generate_stepwise_pairs(seed=seed)
#     save_as_json_with_step_dict(pairs, "stepwise_path_pairs.json")
#     save_combined_visualization(pairs, "stepwise_combined.jpg")
#     print("✅ 已保存：stepwise_path_pairs.json + stepwise_combined.jpg")
#     print(f"📌 使用随机种子: {seed}")




# import random
# import json
# from PIL import Image
# import matplotlib.pyplot as plt

# # ===== 配色表 =====
# color_table = {
#     '0': (0, 0, 0),
#     '1': (0, 116, 217),
#     '2': (255, 65, 54),
#     '7': (255, 133, 27),
# }

# def draw_grid(grid, cell_size=20):
#     H, W = len(grid), len(grid[0])
#     img = Image.new('RGB', (W * cell_size, H * cell_size))
#     for i in range(H):
#         for j in range(W):
#             color = color_table.get(str(grid[i][j]), (0, 0, 0))
#             for dx in range(cell_size):
#                 for dy in range(cell_size):
#                     img.putpixel((j * cell_size + dx, i * cell_size + dy), color)
#     return img

# # ===== 主函数：尾部递增连接 + 无歧义 =====
# def generate_stepwise_pairs(H=15, W=15, steps=9, seed=42, max_dist=3):
#     if seed is not None:
#         random.seed(seed)

#     red = (random.randint(3, H - 4), random.randint(3, W - 4))
#     used = {red}
#     blues = []
#     path_segments = []
#     current_tail = red
#     total_path_len = 0

#     pairs = []

#     while len(pairs) < steps:
#         found = False
#         for attempt in range(300):
#             dx, dy = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
#             dist = random.randint(2, max_dist)
#             nx, ny = current_tail[0] + dx * dist, current_tail[1] + dy * dist
#             candidate = (nx, ny)

#             if not (0 <= nx < H and 0 <= ny < W):
#                 continue
#             if candidate in used:
#                 continue

#             segment = []
#             conflict = False
#             if current_tail[0] == nx:
#                 for y in range(min(current_tail[1], ny) + 1, max(current_tail[1], ny)):
#                     if (nx, y) in used:
#                         conflict = True
#                         break
#                     segment.append((nx, y))
#             elif current_tail[1] == ny:
#                 for x in range(min(current_tail[0], nx) + 1, max(current_tail[0], nx)):
#                     if (x, ny) in used:
#                         conflict = True
#                         break
#                     segment.append((x, ny))
#             else:
#                 continue

#             if conflict or len(segment) <= 0:
#                 continue

#             # ✅ 严格距离大于上一步，避免等距歧义
#             if len(segment) <= 1:
#                 continue

#             # 合法路径
#             blues.append(candidate)
#             used.add(candidate)
#             used.update(segment)
#             path_segments.append(segment)
#             current_tail = candidate
#             total_path_len += len(segment)
#             found = True
#             break

#         if not found:
#             continue

#         # ==== 构建 input/output grid ====
#         input_grid = [[0 for _ in range(W)] for _ in range(H)]
#         output_grid = [[0 for _ in range(W)] for _ in range(H)]
#         input_grid[red[0]][red[1]] = 2
#         output_grid[red[0]][red[1]] = 2
#         for bx, by in blues:
#             input_grid[bx][by] = 1
#             output_grid[bx][by] = 1
#         for seg in path_segments:
#             for px, py in seg:
#                 output_grid[px][py] = 7

#         pairs.append({
#             "step": len(pairs),
#             "input": input_grid,
#             "output": output_grid
#         })

#     return pairs

# # ===== JSON 保存 =====
# def save_as_json_with_step_dict(pairs, path):
#     stepwise_dict = {}
#     for p in pairs:
#         stepwise_dict[f"step_{p['step']}"] = p
#     with open(path, "w") as f:
#         json.dump(stepwise_dict, f, indent=2)

# # ===== 拼图保存 =====
# def save_combined_visualization(pairs, out_path="stepwise_combined.jpg"):
#     fig, axs = plt.subplots(3, 3, figsize=(12, 12))
#     for i in range(9):
#         ax = axs[i // 3][i % 3]
#         if i < len(pairs):
#             img = draw_grid(pairs[i]["output"])
#             ax.imshow(img)
#             ax.set_title(f"Step {i+1}")
#         ax.axis("off")
#     plt.tight_layout()
#     fig.savefig(out_path)
#     plt.close(fig)

# # ===== 主执行入口 =====
# if __name__ == "__main__":
#     # seed = 42  # 设置随机种子
    
#     for seed in range(30, 45):
#         # random.seed(seed)
        
#         max_dist = 5  # 控制路径跨度
#         pairs = generate_stepwise_pairs(seed=seed)
#         for pair in pairs:
#             test_json_sample= {
#                     "test": {
#                             "input":  pair["input"],
#                             "output": pair["output"]
#                             }
#                         }
#             per_size_folder_name = os.path.join("/mnt/petrelfs/yangyue/continuous_evaluation/continous_change_input/agentness/3490cc26/data", f'agent1_step_{pair["step"]}')
#             os.makedirs(per_size_folder_name, exist_ok=True)
            
#             with open(f"{per_size_folder_name}/index_{seed}_step_{pair['step']}.json", "w", encoding="utf-8") as f:
#                 json.dump(test_json_sample, f, ensure_ascii=False, indent=4)

        
        
#         # save_as_json_with_step_dict(pairs, "stepwise_path_pairs.json")
#         save_combined_visualization(pairs, os.path.join("/mnt/petrelfs/yangyue/continuous_evaluation/continous_change_input/agentness/3490cc26/imgs_9",f"seed_{seed}_stepwise_combined.jpg"))
#         print("✅ 已保存：stepwise_path_pairs.json + stepwise_combined.jpg")
        
    

    # pairs = generate_stepwise_pairs(seed=seed, max_dist=max_dist)
    # save_as_json_with_step_dict(pairs, "stepwise_path_pairs.json")
    # save_combined_visualization(pairs, "stepwise_combined.jpg")
    # print("✅ 已保存 stepwise_path_pairs.json + stepwise_combined.jpg")
    # print(f"📌 设置：seed={seed}, max_dist={max_dist}, 无路径歧义，递增尾部连接")




import random
import json
from PIL import Image
import matplotlib.pyplot as plt

# ===== 配色表 =====
color_table = {
    '0': (0, 0, 0),
    '1': (0, 116, 217),
    '2': (255, 65, 54),
    '7': (255, 133, 27),
}

def draw_grid(grid, cell_size=20):
    H, W = len(grid), len(grid[0])
    img = Image.new('RGB', (W * cell_size, H * cell_size))
    for i in range(H):
        for j in range(W):
            color = color_table.get(str(grid[i][j]), (0, 0, 0))
            for dx in range(cell_size):
                for dy in range(cell_size):
                    img.putpixel((j * cell_size + dx, i * cell_size + dy), color)
    return img

# ===== 主函数：尾部递增连接 + 无歧义 =====
def generate_stepwise_pairs(H=15, W=15, steps=9, seed=42, max_dist=3):
    if seed is not None:
        random.seed(seed)

    red = (random.randint(3, H - 4), random.randint(3, W - 4))
    used = {red}
    blues = []
    path_segments = []
    current_tail = red
    total_path_len = 0
    blue_to_dist = {}  # ✅ 新增：记录蓝点连接距离

    pairs = []

    while len(pairs) < steps:
        found = False
        for attempt in range(50):
            dx, dy = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
            dist = random.randint(2, max_dist)
            nx, ny = current_tail[0] + dx * dist, current_tail[1] + dy * dist
            candidate = (nx, ny)

            if not (0 <= nx < H and 0 <= ny < W):
                continue
            if candidate in used:
                continue

            # ✅ 新增：不能让 candidate 与任意蓝点的距离 == 该蓝点已连接的路径距离
            conflict_distance = False
            for blue, d in blue_to_dist.items():
                manhattan = abs(blue[0] - candidate[0]) + abs(blue[1] - candidate[1])
                if manhattan == d:
                    conflict_distance = True
                    break
            if conflict_distance:
                continue

            segment = []
            conflict = False
            if current_tail[0] == nx:
                for y in range(min(current_tail[1], ny) + 1, max(current_tail[1], ny)):
                    if (nx, y) in used:
                        conflict = True
                        break
                    segment.append((nx, y))
            elif current_tail[1] == ny:
                for x in range(min(current_tail[0], nx) + 1, max(current_tail[0], nx)):
                    if (x, ny) in used:
                        conflict = True
                        break
                    segment.append((x, ny))
            else:
                continue

            if conflict or len(segment) <= 0:
                continue

            # ✅ 严格距离大于上一步，避免等距歧义
            if len(segment) <= 1:
                continue

            # ✅ 添加成功后记录当前蓝点连接的路径长度
            blue_to_dist[current_tail] = dist

            # 合法路径
            blues.append(candidate)
            used.add(candidate)
            used.update(segment)
            path_segments.append(segment)
            current_tail = candidate
            total_path_len += len(segment)
            found = True
            break

        if not found:
            continue

        # ==== 构建 input/output grid ====
        input_grid = [[0 for _ in range(W)] for _ in range(H)]
        output_grid = [[0 for _ in range(W)] for _ in range(H)]
        input_grid[red[0]][red[1]] = 2
        output_grid[red[0]][red[1]] = 2
        for bx, by in blues:
            input_grid[bx][by] = 1
            output_grid[bx][by] = 1
        for seg in path_segments:
            for px, py in seg:
                output_grid[px][py] = 7

        pairs.append({
            "step": len(pairs),
            "input": input_grid,
            "output": output_grid
        })

    
    if len(pairs) < steps:
        return None  # ❌ 没生成够，直接返回 None

    return pairs  # ✅ 正常返回
    # return pairs

# ===== JSON 保存 =====
def save_as_json_with_step_dict(pairs, path):
    stepwise_dict = {}
    for p in pairs:
        stepwise_dict[f"step_{p['step']}"] = p
    with open(path, "w") as f:
        json.dump(stepwise_dict, f, indent=2)

# ===== 拼图保存 =====
def save_combined_visualization(pairs, out_path="stepwise_combined.jpg"):
    fig, axs = plt.subplots(3, 3, figsize=(12, 12))
    for i in range(9):
        ax = axs[i // 3][i % 3]
        if i < len(pairs):
            img = draw_grid(pairs[i]["output"])
            ax.imshow(img)
            ax.set_title(f"Step {i+1}")
        ax.axis("off")
    plt.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)



# ===== 主执行入口 =====
if __name__ == "__main__":
    # seed = 42  # 设置随机种子
    
    for seed in range(48, 50):
        # random.seed(seed)
        
        max_dist = 5  # 控制路径跨度
        pairs = generate_stepwise_pairs(seed=seed)
        
        if pairs is None:
            print(f"❌ Seed {seed} skipped (not enough valid paths)")
            continue  # 跳过失败的 seed
        
        for pair in pairs:
            print(pair["step"])
            test_json_sample= {
                    "test": {
                            "input":  pair["input"],
                            "output": pair["output"]
                            }
                        }
            per_size_folder_name = os.path.join("/mnt/petrelfs/yangyue/continuous_evaluation/continous_change_input/agentness/3490cc26/data", f'agent1_step_{pair["step"]}')
            os.makedirs(per_size_folder_name, exist_ok=True)
            
            with open(f"{per_size_folder_name}/index_{seed}_step_{pair['step']}.json", "w", encoding="utf-8") as f:
                json.dump(test_json_sample, f, ensure_ascii=False, indent=4)

        
        
        # save_as_json_with_step_dict(pairs, "stepwise_path_pairs.json")
        save_combined_visualization(pairs, os.path.join("/mnt/petrelfs/yangyue/continuous_evaluation/continous_change_input/agentness/3490cc26/imgs_9",f"seed_{seed}_stepwise_combined.jpg"))
        print("✅ 已保存：stepwise_path_pairs.json + stepwise_combined.jpg")