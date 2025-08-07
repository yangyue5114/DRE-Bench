# gravity_typed_procedural.py
import numpy as np
import random
from typing import List, Dict, Tuple

Grid = np.ndarray
Objects = List[Dict]
GroundLevels = Dict[int, int]

def setup_scene(height: int, width: int, num_objects: int) -> Tuple[Grid, Objects, GroundLevels]:
    """Initializes the grid, ground, and objects in a single procedural pass."""
    grid = np.zeros((height, width), dtype=int)
    ground_levels = {x: height - random.randint(1, 4) for x in range(width)}
    
    # Draw ground
    for x, top_y in ground_levels.items():
        grid[top_y:, x] = 1

    # Generate objects
    available_cols = [x for x, top_y in ground_levels.items() if top_y >= 3]
    random.shuffle(available_cols)
    
    objects = []
    for x in available_cols[:num_objects]:
        colors = np.random.randint(2, 10, size=3)
        grid[0:3, x] = colors
        objects.append({'colors': colors, 'x': x})
        
    return grid, objects, ground_levels

def run_gravity_simulation(objects: Objects, ground_levels: GroundLevels, height: int, width: int) -> Grid:
    """Computes the final state after gravity is applied."""
    final_grid = np.zeros((height, width), dtype=int)
    
    # Recreate ground
    for x, top_y in ground_levels.items():
        final_grid[top_y:, x] = 1
    
    # Place objects at their final destination
    for obj in objects:
        landing_y = ground_levels[obj['x']] - 3
        final_grid[landing_y:landing_y + 3, obj['x']] = obj['colors']
        
    return final_grid

# --- Main Execution ---
if __name__ == "__main__":
    H, W, N_OBJECTS = 10, 20, 8
    
    initial_grid, falling_objects, ground = setup_scene(H, W, N_OBJECTS)
    print("--- 初始矩阵 (Typed Procedural Style) ---\n", initial_grid)
    
    final_grid = run_gravity_simulation(falling_objects, ground, H, W)
    print("\n--- 变化后的矩阵 ---\n", final_grid)