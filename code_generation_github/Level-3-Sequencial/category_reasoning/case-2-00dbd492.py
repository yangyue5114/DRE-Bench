import json
import numpy as np
import random
import os
from PIL import Image, ImageDraw
import time
import copy
patterns = np.array([
    [[2,2,2,2,2],[2,0,0,0,2],[2,0,2,0,2],[2,0,0,0,2],[2,2,2,2,2]],
    [[2,2,2,2,2,2,2],[2,0,0,0,0,0,2],[2,0,0,0,0,0,2],[2,0,0,2,0,0,2],[2,0,0,0,0,0,2],[2,0,0,0,0,0,2],[2,2,2,2,2,2,2]],
    [[2,2,2,2,2,2,2,2,2],[2,0,0,0,0,0,0,0,2],[2,0,0,0,0,0,0,0,2],[2,0,0,0,0,0,0,0,2],[2,0,0,0,2,0,0,0,2],[2,0,0,0,0,0,0,0,2],[2,0,0,0,0,0,0,0,2],[2,0,0,0,0,0,0,0,2],[2,2,2,2,2,2,2,2,2]]
])
position = [(12,12), (0,0), (0,12),(12,0)]
colors = [8, 4, 3]
color_table = {
    "0": (0, 0, 0),        # black
    "1": (0, 116, 217),    # blue
    "2": (255, 65, 54),    # red
    "3": (46, 204, 64),    # green
    "4": (255, 220, 0),    # yellow
    "5": (170, 170, 170),  # grey
    "6": (240, 18, 190),   # fuschia
    "7": (255, 133, 27),   # orange
    "8": (127, 219, 255),  # teal
    "9": (135, 12, 37)     # brown
}
WHITE = (255, 255, 255)

def convert_int(gird):
    return [[int(item) for item in sublist] for sublist in gird]

def place_pattern(matrix, pattern, start_row, start_col):
    for i in range(len(pattern)):
        for j in range(len(pattern[0])):
            if 0 <= start_row + i < len(matrix) and 0 <= start_col + j < len(matrix[0]):
                matrix[start_row + i][start_col + j] = pattern[i][j]


def fill_color(matrix, color):
    new_matrix = copy.deepcopy(matrix)
    rows, cols =  len(matrix), len(matrix[0])
    for i in range(rows):
        for j in range(cols):
            if (new_matrix[i][j] == 0): new_matrix[i][j] = color
    return new_matrix


def generate_254ccf6(rows, cols, numbers):
    matrix = [[0] * cols for _ in range(rows)]
    gt_matrix = [[0] * cols for _ in range(rows)]


    for num in range(numbers):
        pt = [[0] * 12 for _ in range(12)]
        gt = [[0] * 12 for _ in range(12)]
        pattern_index = random.randint(0, 2)
        if   (pattern_index == 0):
            x = random.randint(0, 6)
            y = random.randint(0, 6)
        elif (pattern_index == 1):
            x = random.randint(0, 4)
            y = random.randint(0, 4)
        else:
            x = random.randint(0, 2)
            y = random.randint(0, 2)
        place_pattern(pt, patterns[pattern_index], x, y)
        place_pattern(gt, fill_color(patterns[pattern_index] ,colors[pattern_index]), x, y)
        x, y = random.choice(position)
        place_pattern(matrix, pt, x, y)
        place_pattern(gt_matrix, gt, x, y)
    return matrix, gt_matrix


def visualize_grid(grid, save_dir_pic, save_dir_dt, file_name, image_size=500):
    rows, cols = len(grid), len(grid[0])
    cell_size = image_size // max(rows, cols)  
    img_width, img_height = cols * cell_size, rows * cell_size  
    image = Image.new('RGB', (img_width, img_height), WHITE)
    draw = ImageDraw.Draw(image)
    grid_line_color = (200, 200, 200) 
    for i in range(rows):
        for j in range(cols):
            color = color_table.get(str(grid[i][j]), WHITE)
            left = j * cell_size
            top = i * cell_size
            right = left + cell_size - 1
            bottom = top + cell_size - 1
            draw.rectangle([left, top, right, bottom], fill=color, outline=grid_line_color)
    os.makedirs(save_dir_pic, exist_ok=True)
    os.makedirs(save_dir_dt, exist_ok=True)
    timestamp = int(time.time())
    save_path = os.path.join(save_dir_pic, f"{file_name}_{timestamp}.png")
    save_path_2 = os.path.join(save_dir_dt, f"{file_name}_{timestamp}.json")
    image.save(save_path)
    print(f"Saved image: {save_path}")
    with open(save_path_2,"w") as f: json.dump(grid, f, indent=4)

for i in range(8):
    time.sleep(1)
    ans, ans_gt= generate_254ccf6(24, 24, 1)
    grid = convert_int(ans)
    grid_gt = convert_int(ans_gt)
    file_name = 'grid_image' 
    save_dir_pic = 'pictures/num = 1'
    save_dir_data = 'data/num = 1'
    save_dir_gt = 'pictures_gt/num = 1'
    save_dir_data_gt = 'data_gt/num = 1'
    visualize_grid(grid, save_dir_pic, save_dir_data, file_name)
    visualize_grid(grid_gt, save_dir_gt, save_dir_data_gt, file_name)