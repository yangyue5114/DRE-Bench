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
def rot_45_hv(matrix, pivot):
    rows, cols = len(matrix), len(matrix[0])
    new_matrix = [[0] * cols for _ in range(rows)]
    centerx,centery = pivot 
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
def rot_45_vh(matrix, pivot):
    rows, cols = len(matrix), len(matrix[0])
    new_matrix = [[0] * cols for _ in range(rows)]
    centerx,centery = pivot 
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
def rotate_matrix_90(matrix, pivot):
    rows, cols = len(matrix), len(matrix[0])
    new_matrix = [[0] * rows for _ in range(cols)]

    pivot_row, pivot_col = pivot

    for row in range(rows):
        for col in range(cols):
            new_row = pivot_row + (col - pivot_col)
            new_col = pivot_col - (row - pivot_row)
            if 0 <= new_row < rows and 0 <= new_col < cols:
                new_matrix[new_row][new_col] = matrix[row][col]

    return new_matrix

def rotate_matrix_135(matrix, pivot):
    new_matrix = rotate_matrix_90(matrix, pivot)
    new_matrix_2 = rot_45_vh(new_matrix, pivot)
    return new_matrix_2
def rotate_matrix_180(matrix, pivot):
    rows, cols = len(matrix), len(matrix[0])
    new_matrix = [[0] * rows for _ in range(cols)]

    pivot_row, pivot_col = pivot

    for row in range(rows):
        for col in range(cols):

            new_row = pivot_row + (pivot_row - row)
            new_col = pivot_col + (pivot_col - col)


            if 0 <= new_row < rows and 0 <= new_col < cols:
                new_matrix[new_row][new_col] = matrix[row][col]
    return new_matrix
def rotate_matrix_225(matrix, pivot):
    new_matrix = rotate_matrix_180(matrix, pivot)
    new_matrix2 = rot_45_hv(new_matrix, pivot)
    return new_matrix2
def rotate_matrix_270(matrix, pivot):
    rows, cols = len(matrix), len(matrix[0])
    new_matrix = [[0] * rows for _ in range(cols)]

    pivot_row, pivot_col = pivot

    for row in range(rows):
        for col in range(cols):
    
            new_row = pivot_row - (col - pivot_col)  
            new_col = pivot_col + (row - pivot_row)

   
            if 0 <= new_row < rows and 0 <= new_col < cols:
                new_matrix[new_row][new_col] = matrix[row][col]
    return new_matrix
def rotate_matrix_315(matrix, pivot):
    new_matrix = rotate_matrix_270(matrix, pivot)
    new_matrix_2 = rot_45_vh(new_matrix, pivot)
    return new_matrix_2
functions={
    45 : rot_45_hv,
    90 : rotate_matrix_90,
    135: rotate_matrix_135,
    180 :rotate_matrix_180,
    225 :rotate_matrix_225,
    270 :rotate_matrix_270,
    315 :rotate_matrix_315
}
def generate_rot1(rows, cols, angles):
    matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    gt_matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    length = random.choice([5, 7, 9])
    start_row = rows // 2 
    start_col = cols // 2 
    color1, color2 = random.sample(range(1, 10), 2)
    for i in range(length): matrix[start_row][start_col + i] = color1
    matrix[start_row][start_col] = color2
    gt_matrix = functions[angles](matrix,(start_row,start_col))            
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


ans, ans_gt= generate_rot1(19, 19, 315)
grid = convert_int(ans)
grid_gt = convert_int(ans_gt)
file_name = 'grid_image' 
save_dir_pic = 'pictures/rot315'
save_dir_data = 'data/rot315'
save_dir_gt = 'pictures_gt/rot315'
save_dir_data_gt = 'data_gt/rot315'
visualize_grid(grid, save_dir_pic, save_dir_data, file_name)
visualize_grid(grid_gt, save_dir_gt, save_dir_data_gt, file_name)
