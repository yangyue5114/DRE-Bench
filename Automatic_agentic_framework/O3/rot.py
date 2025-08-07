# rot_linear_algebra.py
import numpy as np

def get_rotation_matrix(angle_deg: float) -> np.ndarray:
    """Returns a 2D rotation matrix for a given angle in degrees."""
    angle_rad = np.deg2rad(angle_deg)
    c, s = np.cos(angle_rad), np.sin(angle_rad)
    return np.array([[c, -s], [s, c]])

def create_rotated_grid(line_points: np.ndarray, angle_deg: float, size: int, colors: dict) -> np.ndarray:
    """Rotates a set of points using matrix multiplication and renders them to a grid."""
    center = size // 2
    
    # 1. Define the rotation matrix
    rot_matrix = get_rotation_matrix(angle_deg)
    
    # 2. Translate points to origin, rotate, then translate back
    translated_points = line_points - center
    rotated_points = translated_points @ rot_matrix.T # Using matrix multiplication
    final_coords = np.round(rotated_points + center).astype(int)

    # 3. Render to grid
    grid = np.zeros((size, size), dtype=int)
    valid_mask = (final_coords[:, 0] >= 0) & (final_coords[:, 0] < size) & \
                 (final_coords[:, 1] >= 0) & (final_coords[:, 1] < size)
    
    # Use tuple indexing for advanced assignment
    coords_to_draw = final_coords[valid_mask]
    colors_to_draw = colors['all'][valid_mask]
    grid[coords_to_draw[:, 0], coords_to_draw[:, 1]] = colors_to_draw
    
    return grid

# --- Main Execution ---
if __name__ == "__main__":
    SIZE, CENTER = 13, 6
    LINE_LEN = 5

    # Define the initial vertical line as a matrix of (y, x) coordinates
    original_line = np.array(
        [[CENTER, CENTER]] + # Bottom point
        [[CENTER - i, CENTER] for i in range(1, LINE_LEN)] + # Body
        [[CENTER - LINE_LEN, CENTER]] # Top point
    )
    
    # Corresponding colors for each point
    line_colors = np.array([9] + [4]*(LINE_LEN - 1) + [7])

    for angle in [0, 45, 90, 135, 180, 225, 270, 315, 360]:
        print(f"\n--- 旋转 {angle} 度 (Linear Algebra Style) ---")
        canvas = create_rotated_grid(original_line, angle, SIZE, {'all': line_colors})
        print(canvas)