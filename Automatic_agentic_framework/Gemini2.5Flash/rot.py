# rot_functional.py
import numpy as np
import math
from functools import partial

# --- Configuration (kept separate from logic) ---
SIZE = 13
CENTER_XY = SIZE // 2
LINE_LENGTH_FROM_CENTER = 5
COLORS = {'top': 7, 'body': 4, 'bottom': 9}

# --- Pure Functions ---

def create_line_definition(center, length, colors):
    """
    Generates a data structure representing the line, not drawing it.
    This is a pure function: returns data, has no side effects.
    """
    points = [{'y': center - i, 'x': center, 'color': colors['body']} for i in range(1, length)]
    points.append({'y': center, 'x': center, 'color': colors['bottom']})
    points.append({'y': center - length, 'x': center, 'color': colors['top']})
    return points

def _rotate_single_point(point, angle_deg, center_xy):
    """Helper function to rotate one point dictionary."""
    angle_rad = math.radians(angle_deg)
    cx, cy = center_xy, center_xy
    
    # Translate to origin
    translated_x = point['x'] - cx
    translated_y = point['y'] + cy
    
    # Rotate
    rotated_x = translated_x * math.cos(angle_rad) - translated_y * math.sin(angle_rad)
    rotated_y = translated_x * math.sin(angle_rad) + translated_y * math.cos(angle_rad)
    
    # Translate back and create new point
    return {
        'y': int(round(rotated_y + cy)),
        'x': int(round(rotated_x + cx)),
        'color': point['color']
    }

def rotate_line(line_points, angle_deg, center_xy):
    """
    Takes a line definition and returns a new, rotated line definition.
    This is a pure function.
    """
    # Create a specialized rotation function for the given angle and center
    rotator = partial(_rotate_single_point, angle_deg=angle_deg, center_xy=center_xy)
    # Use map to apply the rotation to every point in the list
    return list(map(rotator, line_points))

def render_to_grid(points, size):
    """
    Takes a list of points and renders them onto a new, blank grid.
    This is a pure function.
    """
    grid = np.zeros((size, size), dtype=int)
    for p in points:
        if 0 <= p['y'] < size and 0 <= p['x'] < size:
            grid[p['y'], p['x']] = p['color']
    return grid

# --- Main Execution ---
def main():
    print("本任务将一条中心垂直线围绕画布中心进行旋转 (Functional Style)。")
    
    # 1. Define the initial data structure (immutable)
    original_line = create_line_definition(CENTER_XY, LINE_LENGTH_FROM_CENTER, COLORS)

    # 2. Define the transformations to apply
    angles_to_process = [0, 45, 90, 135, 180, 225, 270, 315, 360]

    # 3. Process and print results through a pipeline
    for angle in angles_to_process:
        print(f"\n--- 旋转 {angle} 度 ---")
        # Functional pipeline: rotate the data, then render it to a grid
        rotated_line_data = rotate_line(original_line, angle, CENTER_XY)
        final_grid = render_to_grid(rotated_line_data, SIZE)
        print(final_grid)

if __name__ == "__main__":
    main()