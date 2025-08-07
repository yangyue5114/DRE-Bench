# agentic_numpy_optimized.py
import numpy as np
import random
from itertools import permutations

SIZE = 11

def setup_grid(num_waypoints):
    """
    Creates an 11x11 grid, placing a start point and waypoints.
    
    Returns:
    - Tuple of (grid, start_coord, waypoints_list)
    """
    if num_waypoints + 1 > SIZE * SIZE:
        raise ValueError(f"Too many points requested for a {SIZE}x{SIZE} grid.")

    # Generate all possible coordinates and shuffle them
    coords = np.random.permutation([(y, x) for y in range(SIZE) for x in range(SIZE)])
    
    # Assign coordinates
    start_coord = tuple(coords[0])
    waypoint_coords = [tuple(c) for c in coords[1:num_waypoints+1]]
    
    # Create grid and place points
    grid = np.zeros((SIZE, SIZE), dtype=int)
    grid[start_coord] = 2
    for wp in waypoint_coords:
        grid[wp] = 1
        
    return grid, start_coord, waypoint_coords

def find_shortest_path_tsp(start_point, waypoints):
    """
    Solves the Traveling Salesperson Problem using a brute-force permutation check.
    WARNING: Computationally expensive. Infeasible for >10 waypoints.
    """
    if not waypoints:
        return [start_point]

    best_path = None
    min_distance = float('inf')
    
    # Pre-calculate distances to avoid recalculation
    all_points = [start_point] + waypoints
    dist_cache = {p1: {p2: abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]) for p2 in all_points} for p1 in all_points}

    for p_order in permutations(waypoints):
        current_distance = dist_cache[start_point][p_order[0]]
        for i in range(len(p_order) - 1):
            current_distance += dist_cache[p_order[i]][p_order[i+1]]
        
        if current_distance < min_distance:
            min_distance = current_distance
            best_path = p_order
            
    return [start_point] + list(best_path)

def draw_path_vectorized(grid, path):
    """
    Draws the path on the grid using NumPy slicing for better performance.
    """
    grid_with_path = grid.copy()
    for p1, p2 in zip(path, path[1:]):
        y1, x1 = p1
        y2, x2 = p2
        
        # Define the path's bounding box and fill it
        # Note: This draws L-shaped paths (horizontal then vertical)
        x_min, x_max = min(x1, x2), max(x1, x2)
        y_min, y_max = min(y1, y2), max(y1, y2)
        
        # Fill horizontal segment
        grid_with_path[y1, x_min:x_max+1][grid_with_path[y1, x_min:x_max+1] == 0] = 5
        # Fill vertical segment
        grid_with_path[y_min:y_max+1, x2][grid_with_path[y_min:y_max+1, x2] == 0] = 5
        
    return grid_with_path

# --- Main Execution ---
if __name__ == "__main__":
    NUMBER_OF_WAYPOINTS = 8
    if not 1 <= NUMBER_OF_WAYPOINTS <= 10:
        print("Warning: Waypoint count is outside the recommended range of 1-10 for performance.")

    try:
        initial_grid, start, waypoints = setup_grid(NUMBER_OF_WAYPOINTS)
        print("--- 初始地图 (NumPy-Optimized Style) ---")
        print(f"起点(2): {start}, 途径点(1): {waypoints}")
        print(initial_grid)

        print("\n--- 计算最短路径... ---")
        optimal_path = find_shortest_path_tsp(start, waypoints)
        print(f"最优路径顺序: {optimal_path}")

        final_grid = draw_path_vectorized(initial_grid, optimal_path)
        print("\n--- 最终路径图 ---")
        print("路径(5)连接起点(2)和所有途径点(1):")
        print(final_grid)

    except ValueError as e:
        print(f"Error: {e}")