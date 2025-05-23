import json
import random
import numpy as np
import random
import os
from PIL import Image, ImageDraw
import time
import math
import copy

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



def shoot_left_up(matrix, start_rows, start_cols):
    new_i = start_rows
    new_j = start_cols
    while (matrix[new_i][new_j] == 0 and new_i < len(matrix) and new_j < len(matrix[0])):
        matrix[new_i][new_j] = 7
        new_i -= 1
        new_j -= 1
    if (matrix[new_i][new_j + 1] == 1 or matrix[new_i][new_j - 1] == 1): return new_i + 2, new_j, 1
    elif (matrix[new_i + 1][new_j] == 1 or matrix[new_i - 1][new_j] == 1): return new_i, new_j + 2, 2
    else: return -1, -1, 0 

def shoot_left_down(matrix, start_rows, start_cols):
    new_i = start_rows
    new_j = start_cols
    while (matrix[new_i][new_j] == 0 and new_i < len(matrix) and new_j < len(matrix[0])):
        matrix[new_i][new_j] = 7
        new_i += 1
        new_j -= 1
    if (matrix[new_i][new_j + 1] == 1 or matrix[new_i][new_j - 1] == 1): return new_i - 2, new_j, 0
    elif (matrix[new_i + 1][new_j] == 1 or matrix[new_i - 1][new_j] == 1): return new_i, new_j + 2, 3
    else: return -1, -1, 0

def shoot_right_down(matrix, start_rows, start_cols):
    new_i = start_rows
    new_j = start_cols
    while (new_i < len(matrix)  and new_j < len(matrix[0])  and matrix[new_i][new_j] == 0):
        matrix[new_i][new_j] = 7
        new_i += 1
        new_j += 1
    if (matrix[new_i][new_j + 1] == 1 or matrix[new_i][new_j - 1] == 1): return new_i - 2, new_j, 2
    elif (matrix[new_i + 1][new_j] == 1 or matrix[new_i - 1][new_j] == 1): return new_i, new_j - 2, 1
    else: return -1, -1, 0

def shoot_right_up(matrix, start_rows, start_cols):
    new_i = start_rows
    new_j = start_cols
    while (matrix[new_i][new_j] == 0 and new_i < len(matrix) and new_j < len(matrix[0])):
        matrix[new_i][new_j] = 7
        new_i -= 1
        new_j += 1


    if (matrix[new_i][new_j + 1] == 1 or matrix[new_i][new_j - 1] == 1): return new_i + 2, new_j, 3
    elif (matrix[new_i + 1][new_j] == 1 or matrix[new_i - 1][new_j] == 1): return new_i, new_j - 2, 0
    else: return -1, -1, 0

def build_h(new_matrix, matrix, x, y, len):
    for i in range(y, y + len):
        new_matrix[x][i], matrix[x][i] = 1, 1
def build_v(new_matrix, matrix, x, y, len):
    for i in range(x, x + len):
        new_matrix[i][y], matrix[i][y] = 1, 1

functions={
    0: shoot_left_up,
    1: shoot_left_down,
    2: shoot_right_up,
    3: shoot_right_down
}
def generate(rows, cols, numbers):
    matrix = [[0] * cols for _ in range(rows)]
    # for j in range(cols):
    #     matrix[0][j] = 1
    #     matrix[rows - 1][j] = 1
    # for j in range(rows):
    #     matrix[j][0] =1
    #     matrix[j][cols - 1] = 1
    new_matrix = copy.deepcopy(matrix)
    directions = 0
    sr = 5
    sc = 19
    new_matrix[sr][sc] = 7
    build_h(new_matrix, matrix, 0, 13, 4)
    build_h(new_matrix, matrix, 7, 1, 4)
    build_h(new_matrix, matrix, 16, 8, 4)
    build_v(new_matrix, matrix, 10, 0, 4)
    build_v(new_matrix, matrix, 3, 10, 4)
    build_v(new_matrix, matrix, 9, 17, 4)
    
    for num in range(numbers):
        sr ,sc, directions = functions[directions](matrix, sr, sc)
        print(sr,sc,directions)
    return new_matrix, matrix



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


ans, ans_gt= generate(21, 21, 6)
grid = convert_int(ans)
grid_gt = convert_int(ans_gt)
file_name = 'grid_image' 
save_dir_pic = 'pictures/frequency = 5'
save_dir_data = 'data/frequency = 5'
save_dir_gt = 'pictures_gt/frequency = 5'
save_dir_data_gt = 'data_gt/frequency = 5'
visualize_grid(grid, save_dir_pic, save_dir_data, file_name)
visualize_grid(grid_gt, save_dir_gt, save_dir_data_gt, file_name)
