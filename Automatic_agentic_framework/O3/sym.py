# sym_generator_style.py
import numpy as np
import random
from typing import Generator, Tuple

def find_symmetric_spot(canvas: np.ndarray, p_h: int, p_w: int, axis_y: int) -> Generator[Tuple, None, None]:
    """A generator that yields valid symmetric coordinates for a pattern."""
    c_h, c_w = canvas.shape
    max_placement_attempts = 100
    
    for _ in range(max_placement_attempts):
        # Find a random spot above the axis
        y1 = random.randint(0, axis_y - p_h)
        x = random.randint(0, c_w - p_w)
        
        # Calculate reflected coordinate
        y2 = 2 * axis_y - y1 - p_h + 1
        
        # Check if both areas are clear
        if np.all(canvas[y1:y1+p_h, x:x+p_w] == 0) and np.all(canvas[y2:y2+p_h, x:x+p_w] == 0):
            yield (y1, x), (y2, x)
    # The generator is exhausted if no spot is found
    
# --- Main Execution ---
if __name__ == "__main__":
    H, W, AXIS_Y, N_PAIRS = 11, 20, 5, 4
    
    # Setup canvas
    canvas = np.zeros((H, W), dtype=int)
    canvas[AXIS_Y, :] = 1
    
    print("--- 初始画布 (Generator Style) ---\n", canvas)
    print(f"\n--- 开始生成 {N_PAIRS} 组对称图案 ---")

    for i in range(N_PAIRS):
        p_h, p_w = random.randint(1, 3), random.randint(1, 3)
        pattern = np.random.randint(2, 10, size=(p_h, p_w))
        
        # Create a new generator for this specific pattern size
        spot_finder = find_symmetric_spot(canvas, p_h, p_w, AXIS_Y)
        
        try:
            # Try to get the first valid spot from the generator
            (y1, x1), (y2, x2) = next(spot_finder)
            canvas[y1:y1+p_h, x1:x1+p_w] = pattern
            canvas[y2:y2+p_h, x2:x2+p_w] = np.flipud(pattern)
            print(f"  成功: 放置第 {i+1} 组 {p_h}x{p_w} 图案。")
        except StopIteration:
            # This happens if the generator finishes without yielding a spot
            print(f"  警告: 未能为第 {i+1} 组 {p_h}x{p_w} 图案找到位置。")
            
    print("\n--- 最终完成的画布 ---\n", canvas)