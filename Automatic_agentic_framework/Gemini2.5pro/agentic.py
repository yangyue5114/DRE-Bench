import numpy as np
import random
from itertools import permutations

# --- 1. 定义和辅助函数 ---

SIZE = 11

def manhattan_distance(p1, p2):
    """计算两个坐标点之间的曼哈顿距离。"""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def setup_grid_with_points(num_waypoints):
    """
    创建11x11的网格，并随机放置起点和指定数量的途径点。

    参数:
    - num_waypoints (int): 要放置的途径点的数量。

    返回:
    - grid (np.ndarray): 包含点的初始网格。
    - start_coord (tuple): 起点(2)的坐标。
    - waypoints (list): 途径点(1)的坐标列表。
    """
    grid = np.zeros((SIZE, SIZE), dtype=int)
    
    # 检查请求的点数是否超过了网格容量
    total_points = num_waypoints + 1 # 途径点 + 1个起点
    if total_points > SIZE * SIZE:
        print(f"错误：请求的总点数({total_points})超过了网格容量({SIZE*SIZE})。")
        return None, None, None

    # 生成所有可能的坐标位置
    possible_coords = [(y, x) for y in range(SIZE) for x in range(SIZE)]
    random.shuffle(possible_coords)
    
    # 放置起点(2)
    start_coord = possible_coords.pop()
    grid[start_coord] = 2
    
    # 放置指定数量的途径点(1)
    waypoints = []
    for _ in range(num_waypoints):
        waypoint_coord = possible_coords.pop()
        grid[waypoint_coord] = 1
        waypoints.append(waypoint_coord)
        
    return grid, start_coord, waypoints

def find_shortest_path_order(start_coord, waypoints):
    """
    通过遍历所有可能的路径顺序，找到总距离最短的那个。
    
    返回:
    - list: 最优的访问顺序，以坐标列表形式返回，起点在最前面。
    """
    if not waypoints:
        return [start_coord]

    min_path_len = float('inf')
    best_order = None

    # 获取途径点所有可能的排列组合
    # 注意：如果途径点数量超过10个，排列组合的数量会非常巨大，计算会很慢。
    # 对于8个点（8! = 40320）或9个点（9! = 362880），计算是很快的。
    for p in permutations(waypoints):
        current_path_len = 0
        last_point = start_coord
        
        # 计算当前排列顺序的总长度
        for waypoint in p:
            current_path_len += manhattan_distance(last_point, waypoint)
            last_point = waypoint
        
        # 如果找到了更短的路径，则更新记录
        if current_path_len < min_path_len:
            min_path_len = current_path_len
            best_order = p
            
    # 将起点加在最前面，构成完整路径
    return [start_coord] + list(best_order)

def draw_path_on_grid(grid, full_path_order):
    """
    在网格上根据最优路径顺序，用5填充路径。
    """
    for i in range(len(full_path_order) - 1):
        p1 = full_path_order[i]
        p2 = full_path_order[i+1]
        
        y1, x1 = p1
        y2, x2 = p2
        
        # 先走横向，再走纵向
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if grid[y1, x] == 0:
                grid[y1, x] = 5
        
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if grid[y, x2] == 0:
                grid[y, x2] = 5
    return grid

# --- 2. 主程序 ---
if __name__ == "__main__":
    
    # ======================================================
    # == 在这里控制途径点的数量 (例如，设置为5) ==
    NUMBER_OF_WAYPOINTS = 8
    # ======================================================

    # 检查设置的数量是否在合理范围内
    if not 1 <= NUMBER_OF_WAYPOINTS <= 10:
        print("警告：为获得最佳性能和避免计算时间过长，建议将途径点数量设置在1到10之间。")
        # 即使超出建议范围，程序仍会尝试运行
    
    # 步骤1: 创建带有指定数量点的地图
    initial_grid, start_point, waypoints_list = setup_grid_with_points(NUMBER_OF_WAYPOINTS)
    
    # 检查地图是否成功创建
    if initial_grid is not None:
        print("--- 初始地图 ---")
        print(f"起点(2)位置: {start_point}")
        print(f"途径点(1)位置: {waypoints_list}")
        print(initial_grid)
        
        # 步骤2: 找到最短的访问顺序
        print("\n--- 正在计算最短路径顺序... ---")
        optimal_order = find_shortest_path_order(start_point, waypoints_list)
        print(f"找到的最优路径顺序: {optimal_order}")
        
        # 步骤3: 在地图上绘制这条最优路径
        final_grid = draw_path_on_grid(initial_grid.copy(), optimal_order)
        
        print("\n--- 最终路径图 ---")
        print("路径用5表示，连接起点(2)和所有途径点(1):")
        print(final_grid)