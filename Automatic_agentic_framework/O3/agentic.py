# agentic_algorithmic.py
import numpy as np
import random
from itertools import permutations
from typing import List, Tuple

Coord = Tuple[int, int]
Path = List[Coord]

def manhattan_dist(p1: Coord, p2: Coord) -> int:
    """Calculates Manhattan distance."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def solve_tsp_bruteforce(start: Coord, waypoints: List[Coord]) -> Path:
    """Finds the shortest path order by checking all permutations."""
    if not waypoints:
        return [start]
    
    # Find the permutation with the minimum total distance
    best_perm = min(
        permutations(waypoints),
        key=lambda p: manhattan_dist(start, p[0]) + sum(manhattan_dist(p[i], p[i+1]) for i in range(len(p)-1))
    )
    return [start] + list(best_perm)

def render_grid_with_path(start: Coord, waypoints: List[Coord], path: Path, size: int) -> np.ndarray:
    """Renders the final grid including points and the calculated path."""
    grid = np.zeros((size, size), dtype=int)
    grid[start] = 2
    for wp in waypoints:
        grid[wp] = 1

    for i in range(len(path) - 1):
        y1, x1 = path[i]
        y2, x2 = path[i+1]
        
        # Draw path segment (horizontal then vertical)
        curr_x, curr_y = x1, y1
        while curr_x != x2:
            if grid[curr_y, curr_x] == 0: grid[curr_y, curr_x] = 5
            curr_x += 1 if x2 > x1 else -1
        while curr_y != y2:
            if grid[curr_y, curr_x] == 0: grid[curr_y, curr_x] = 5
            curr_y += 1 if y2 > y1 else -1

    return grid

# --- Main Execution ---
if __name__ == "__main__":
    GRID_SIZE, N_WAYPOINTS = 11, 8
    
    # Generate unique random points
    all_coords = random.sample([(y, x) for y in range(GRID_SIZE) for x in range(GRID_SIZE)], N_WAYPOINTS + 1)
    start_point, waypoint_list = all_coords[0], all_coords[1:]

    print("--- 初始点位 (Algorithmic Style) ---")
    print(f"起点: {start_point}, 途径点: {waypoint_list}")

    optimal_path = solve_tsp_bruteforce(start_point, waypoint_list)
    print(f"\n最优路径: {optimal_path}")
    
    final_grid = render_grid_with_path(start_point, waypoint_list, optimal_path, GRID_SIZE)
    print("\n--- 最终路径图 ---\n", final_grid)