import json
import random
import numpy as np
import random
import os
from PIL import Image, ImageDraw
import time
patterns = np.array([
    [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,2,0,0,2,0],[0,0,0,8,8,8,8,0],[0,0,0,2,0,0,2,0],[0,0,8,8,8,0,0,0]],
    [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,2,0,2,0,0],[0,0,2,3,2,2,0,0],[0,0,0,0,2,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],             
    [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,8,0,8,0,0],[0,0,0,8,4,0,0,0],[0,0,0,8,8,8,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],                
    [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,5,6,6,5,0,0],[0,0,6,6,6,6,0,0],[0,0,6,0,0,6,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]        
    # [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,9,4,9,4,4,0],[0,4,4,4,9,0,4,0],[9,4,0,0,0,4,0,9],[9,9,9,0,0,0,0,0],[0,0,0,0,4,0,4,4]]
                    ])
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
def swap_v(arr):
    values = set()
    for row in arr:
        for value in row:
            if (value != 0 ): values.add(value)
    v1,v2 = list(values)
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if   (arr[i][j] == v1): arr[i][j] = v2
            elif (arr[i][j] == v2): arr[i][j] = v1
    return arr


def generate_2b01abd0(rows, cols, numbers):
    zero_matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    gt_matrix =  [[0 for _ in range(cols)] for _ in range(rows)]
    for row in zero_matrix: row[cols // 2] = 1
    for row in gt_matrix: row[cols // 2] = 1
    for num in range(numbers):
        rd = random.randint(0,1)
        pattern_index = random.randint(0, len(patterns) - 1) 
        if (rd == 0): 
            place_pattern(zero_matrix, patterns[pattern_index], num * (35//numbers), 0)
            place_pattern(gt_matrix, patterns[pattern_index], num * (35 // numbers), 0)
            place_pattern(gt_matrix, (np.fliplr(patterns[pattern_index])), num * (35 // numbers), 9)
        if (rd == 1): 
            place_pattern(zero_matrix, np.fliplr(patterns[pattern_index]), num * (35//numbers), 9)
            place_pattern(gt_matrix, np.fliplr(patterns[pattern_index]), num * (35//numbers), 9)
            place_pattern(gt_matrix, (patterns[pattern_index]), num * (35//numbers), 0)
    return zero_matrix,gt_matrix

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
    file_name = 'grid_image' 
    save_dir_pic = 'pictures/num=1'
    save_dir_data = 'data/num=1'
    save_dir_gt = 'pictures_gt/num=1'
    save_dir_data_gt = 'data_gt/num=1'
    ans, ans_gt= generate_2b01abd0(35, 17, 1)
    grid = convert_int(ans)
    grid_gt = convert_int(ans_gt)
    visualize_grid(grid, save_dir_pic, save_dir_data, file_name)
    visualize_grid(grid_gt, save_dir_gt, save_dir_data_gt, file_name)

