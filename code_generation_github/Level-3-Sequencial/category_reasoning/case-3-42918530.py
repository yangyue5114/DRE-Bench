import json
import numpy as np
import random
import os
from PIL import Image, ImageDraw
import time
import copy

colors = np.array([1,3,2,4])
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


patterns= np.array([
    [[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]],
    [[2, 2, 2, 2, 2], [2, 0, 0, 0, 2], [2, 0, 0, 0, 2], [2, 0, 0, 0, 2], [2, 2, 2, 2, 2]],
    [[3, 3, 3, 3, 3], [3, 0, 0, 0, 3], [3, 0, 0, 0, 3], [3, 0, 0, 0, 3], [3, 3, 3, 3, 3]],
    [[4, 4, 4, 4, 4], [4, 0, 0, 0, 4], [4, 0, 0, 0, 4], [4, 0, 0, 0, 4], [4, 4, 4, 4, 4]],
    [[8, 8, 8, 8, 8], [8, 0, 0, 0, 8], [8, 0, 0, 0, 8], [8, 0, 0, 0, 8], [8, 8, 8, 8, 8]],
    [[6, 6, 6, 6, 6], [6, 0, 0, 0, 6], [6, 0, 0, 0, 6], [6, 0, 0, 0, 6], [6, 6, 6, 6, 6]],
    [[7, 7, 7, 7, 7], [7, 0, 0, 0, 7], [7, 0, 0, 0, 7], [7, 0, 0, 0, 7], [7, 7, 7, 7, 7]]
])
gt_patterns = np.array([
    [[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]],
    [[2, 2, 2, 2, 2], [2, 0, 2, 0, 2], [2, 2, 2, 0, 2], [2, 0, 2, 0, 2], [2, 2, 2, 2, 2]],
    [[3, 3, 3, 3, 3], [3, 3, 0, 0, 3], [3, 0, 3, 0, 3], [3, 0, 0, 3, 3], [3, 3, 3, 3, 3]],
    [[4, 4, 4, 4, 4], [4, 0, 4, 0, 4], [4, 4, 4, 4, 4], [4, 0, 4, 0, 4], [4, 4, 4, 4, 4]],
    [[8, 8, 8, 8, 8], [8, 0, 0, 0, 8], [8, 8, 8, 0, 8], [8, 0, 8, 0, 8], [8, 8, 8, 8, 8]],
    [[6, 6, 6, 6, 6], [6, 0, 6, 0, 6], [6, 0, 6, 6, 6], [6, 0, 0, 0, 6], [6, 6, 6, 6, 6]],
    [[7, 7, 7, 7, 7], [7, 0, 7, 0, 7], [7, 0, 7, 0, 7], [7, 0, 7, 0, 7], [7, 7, 7, 7, 7]]
])
pos = [(1, 1), (1, 7), (1, 13), (1, 19), (7, 1), (7, 7), (7, 13), (7, 19),
       (13, 1), (13, 7), (13, 13), (13, 19), (19, 1), (19, 7), (19, 13), (19, 19)]
idx = [0, 4, 2, 6, 5, 1, 0, 1, 4, 3, 2, 3, 6, 4, 1, 5]
first_appear = [(1, 1), (7, 7), (1, 13), (13 ,7), (1, 7), (19, 19), (1, 19)]

def place_pattern(matrix, pattern, start_row, start_col):
    for i in range(len(pattern)):
        for j in range(len(pattern[0])):
            if 0 <= start_row + i < len(matrix) and 0 <= start_col + j < len(matrix[0]):
                matrix[start_row + i][start_col + j] = pattern[i][j]
    
def convert_int(gird):
    return [[int(item) for item in sublist] for sublist in gird]

def generate_4291850(rows ,cols, numbers):
    matrix = [[0] * cols for _ in range(rows)]
    gt_matrix = [[0] * cols for _ in range(rows)]
    fill_list = random.sample([i for i in range(7)], numbers)

    for i in range(16):
        x, y = pos[i]
        place_pattern(matrix, patterns[idx[i]], x, y)
        place_pattern(gt_matrix, patterns[idx[i]], x, y)
    for index in fill_list:
        x, y = first_appear[index]
        place_pattern(matrix, gt_patterns[index], x, y)
        for i, index2 in enumerate(idx):
            if (index2 == index): 
                xx, yy = pos[i]
                place_pattern(gt_matrix, gt_patterns[index], xx, yy)
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
    ans, ans_gt= generate_4291850(25, 25, 5)
    grid = convert_int(ans)
    grid_gt = convert_int(ans_gt)
    file_name = 'grid_image' 
    save_dir_pic = 'pictures/num = 5'
    save_dir_data = 'data/num = 5'
    save_dir_gt = 'pictures_gt/num = 5'
    save_dir_data_gt = 'data_gt/num = 5'
    visualize_grid(grid, save_dir_pic, save_dir_data, file_name)
    visualize_grid(grid_gt, save_dir_gt, save_dir_data_gt, file_name)