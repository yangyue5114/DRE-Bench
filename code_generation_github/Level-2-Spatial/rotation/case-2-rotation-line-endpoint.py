import json
import random
import numpy as np
import random
import os
from PIL import Image, ImageDraw
import time
import math
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
def rot_45_hv(matrix):
    rows, cols = len(matrix), len(matrix[0])
    new_matrix = [[0] * cols for _ in range(rows)]
    centerx = rows // 2
    centery = cols // 2
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] != 0:
                dx = i - centerx
                dy = j - centery
                new_i = i + dy
                new_j = j + dx
                if 0 <= new_i < rows and 0 <= new_j < cols:
                    new_matrix[new_i][new_j] = matrix[i][j]
    return new_matrix
def rot_45_vh(matrix):
    rows, cols = len(matrix), len(matrix[0])
    new_matrix = [[0] * cols for _ in range(rows)]
    centerx = rows // 2
    centery = cols // 2
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] != 0:
                dx = i - centerx
                dy = j - centery
                new_i = i - dy
                new_j = j - dx
                if 0 <= new_i < rows and 0 <= new_j < cols:
                    new_matrix[new_i][new_j] = matrix[i][j]
    return new_matrix
def rotate_matrix_90(matrix):
    rows, cols = len(matrix), len(matrix[0])
    new_matrix = [[0] * rows for _ in range(cols)]
    for i in range(rows):
        for j in range(cols):
            new_matrix[j][rows - 1 - i] = matrix[i][j]
    return new_matrix
def rotate_matrix_180(matrix):
    rows, cols = len(matrix), len(matrix[0])
    new_matrix = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            new_matrix[rows - 1 - i][cols - 1 - j] = matrix[i][j]
    return new_matrix
def rotate_matrix_270(matrix):
    rows, cols = len(matrix), len(matrix[0])
    new_matrix = [[0] * rows for _ in range(cols)]
    for i in range(rows):
        for j in range(cols):
            new_matrix[cols - 1 - j][i] = matrix[i][j]
    return new_matrix
functions={
    45 : rot_45_hv,
    90 : rotate_matrix_90,
    135: lambda matrix: rot_45_vh(rotate_matrix_90(matrix)),
    180 :rotate_matrix_180,
    225 :lambda matrix: rot_45_hv(rotate_matrix_180(matrix)),
    270 :rotate_matrix_270,
    315 :lambda matrix: rot_45_vh(rotate_matrix_270(matrix)),
    -45 :rot_45_vh,
    -90 :rotate_matrix_90,
    -135:lambda matrix: rot_45_hv(rotate_matrix_90(matrix)),
    -180:rotate_matrix_180,
    -225:lambda matrix: rot_45_vh(rotate_matrix_180(matrix)),
    -270:rotate_matrix_270,
    -315:lambda matrix: rot_45_hv(rotate_matrix_270(matrix)),
}
def generate_rot2(rows, cols, angles):
    length1, length2 = random.sample([5, 7, 9, 11, 13], 2)
    color1, color2, color3, color4, color5 = random.sample(range(1, 10), 5)


    matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    start_row = rows // 2
    start_col = (cols - length1) // 2
    for i in range(length1): matrix[start_row][start_col + i] = color1
    matrix[start_row][start_col] = color2
    rot_matrix = functions[angles](matrix)         

   

    matrix_2 = [[0 for _ in range(cols)] for _ in range(rows)]
    start_row = (rows - length2) // 2
    start_col = cols // 2
    for i in range(length2): matrix_2[start_row + i][start_col] = color3
    matrix_2[start_row][start_col] = color4
    rot_matrix_2 = functions[-angles](matrix_2)

    f_matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    gt_matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if   (matrix[i][j] == 0 and matrix_2[i][j] == 0): f_matrix[i][j] = 0
            elif (matrix[i][j] == 0 and matrix_2[i][j] != 0): f_matrix[i][j] = matrix_2[i][j]
            elif (matrix[i][j] != 0 and matrix_2[i][j] == 0): f_matrix[i][j] = matrix[i][j]
            else: f_matrix[i][j] = color5
            if   (rot_matrix[i][j] == 0 and rot_matrix_2[i][j] == 0): gt_matrix[i][j] = 0
            elif (rot_matrix[i][j] == 0 and rot_matrix_2[i][j] != 0): gt_matrix[i][j] = rot_matrix_2[i][j]
            elif (rot_matrix[i][j] != 0 and rot_matrix_2[i][j] == 0): gt_matrix[i][j] = rot_matrix[i][j]
            else: gt_matrix[i][j] = color5

    return f_matrix, gt_matrix



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

file_name = 'grid_image' 
save_dir_pic = 'pictures/rot315'
save_dir_data = 'data/rot315'
save_dir_gt = 'pictures_gt/rot315'
save_dir_data_gt = 'data_gt/rot315'
ans, ans_gt= generate_rot2(13, 13, 315)
grid = convert_int(ans)
grid_gt = convert_int(ans_gt)
visualize_grid(grid, save_dir_pic, save_dir_data, file_name)
visualize_grid(grid_gt, save_dir_gt, save_dir_data_gt, file_name)
