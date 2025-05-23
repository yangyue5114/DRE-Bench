import json
import numpy as np
import random
import os
from PIL import Image, ImageDraw
import time
patterns = np.array([
                    [[0,0,0,0,0],[0,0,0,0,0],[0,0,2,0,0],[0,0,2,2,2],[0,0,0,2,0]],
                    [[0,0,0,0,0],[0,0,0,0,0],[0,0,1,1,0],[0,0,1,0,1],[0,0,0,1,0]],
                    [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,4,4,4],[0,0,0,4,0]],
                    [[0,0,0,0,0],[3,0,0,3,3],[0,3,3,3,0],[0,0,3,0,0],[0,0,3,0,0]],
                    [[0,0,0,0,0],[0,7,0,0,0],[0,0,7,0,0],[0,0,0,7,7],[0,0,0,0,7]]
                    ])
legal_starter = np.array([
    [ 0,  0],[ 0,  6],[ 0, 12],[ 0, 18],[ 0, 24],[ 0, 30],
    [ 6,  0],[ 6,  6],[ 6, 12],[ 6, 18],[ 6, 24],[ 6, 30],
    [12,  0],[12,  6],[12, 12],[12, 18],[12, 24],[12, 30],
    [18,  0],[18,  6],[18, 12],[18, 18],[18, 24],[18, 30],
    [24,  0],[24,  6],[24, 12],[24, 18],[24, 24],[24, 30],  
])
offset=np.array([(6, 0), (0, 6),(6, 6)])
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
file_name = 'grid_image' 
save_dir_pic = 'pictures/num=6'
save_dir_data = 'data/num=6'
save_dir_gt = 'pictures_gt/num=6'
save_dir_data_gt = 'data_gt/num=6'
def place_pattern(matrix, pattern, start_row, start_col):
    for i in range(len(pattern)):
        for j in range(len(pattern[0])):
            if 0 <= start_row + i < len(matrix) and 0 <= start_col + j < len(matrix[0]):
                matrix[start_row + i][start_col + j] = pattern[i][j]
def convert_int(gird):
    return [[int(item) for item in sublist] for sublist in gird]
def generate_2546ccf6(rows, cols, bgcolor, pattern_numbers):
    global legal_starter
    flag = [0] * 50
    zero_matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    gt_matrix = [[0 for _ in range(cols)] for _ in range(rows)]

    for i in range(rows):
        if i % 6 == 5:
            zero_matrix[i] = [bgcolor] * cols
            gt_matrix[i] = [bgcolor] * cols
    for j in range(cols):
        if j % 6 == 5:
            for i in range(rows):
                zero_matrix[i][j] = bgcolor
                gt_matrix[i][j] = bgcolor

    for i in range(pattern_numbers):
        pattern_index = random.randint(0, len(patterns) - 1) 
        starter_index = random.randint(0, len(legal_starter) - 1)  
        while (flag[starter_index] == 1 or flag[starter_index + 1] == 1 or flag[starter_index + 6] == 1 or flag[starter_index + 7] == 1):
            starter_index = random.randint(0, len(legal_starter) - 1)
        flag[starter_index] = 1 
        flag[starter_index + 1] = 1 
        flag[starter_index + 6] = 1 
        flag[starter_index + 7] = 1
        place_pattern(zero_matrix, patterns[pattern_index], legal_starter[starter_index][0],legal_starter[starter_index][1])
        first, second= random.sample(list(offset), 2)
        if (tuple(first) == (0, 6)):place_pattern(zero_matrix, np.fliplr(patterns[pattern_index]), 
                                           legal_starter[starter_index][0],legal_starter[starter_index][1] + 6)
        if (tuple(first) == (6, 0)):place_pattern(zero_matrix, np.flipud(patterns[pattern_index]), 
                                           legal_starter[starter_index][0] + 6,legal_starter[starter_index][1])
        if (tuple(first) == (6, 6)):place_pattern(zero_matrix, np.flip(patterns[pattern_index]), 
                                           legal_starter[starter_index][0] + 6,legal_starter[starter_index][1] + 6)
        if (tuple(second) == (0, 6)): place_pattern(zero_matrix, np.fliplr(patterns[pattern_index]), 
                                           legal_starter[starter_index][0],legal_starter[starter_index][1] + 6)
        if (tuple(second) == (6, 0)):place_pattern(zero_matrix, np.flipud(patterns[pattern_index]), 
                                           legal_starter[starter_index][0] + 6,legal_starter[starter_index][1])
        if (tuple(second) == (6, 6)):place_pattern(zero_matrix, np.flip(patterns[pattern_index]), 
                                           legal_starter[starter_index][0] + 6,legal_starter[starter_index][1] + 6)
        
        place_pattern(gt_matrix, patterns[pattern_index], 
                      legal_starter[starter_index][0],legal_starter[starter_index][1])
        place_pattern(gt_matrix, np.fliplr(patterns[pattern_index]), 
                      legal_starter[starter_index][0], legal_starter[starter_index][1] + 6)
        place_pattern(gt_matrix, np.flipud(patterns[pattern_index]), 
                      legal_starter[starter_index][0] + 6, legal_starter[starter_index][1])
        place_pattern(gt_matrix, np.flip(patterns[pattern_index]), 
                                           legal_starter[starter_index][0] + 6,legal_starter[starter_index][1] + 6)
    return zero_matrix, gt_matrix
ans, ans_gt = generate_2546ccf6(36, 42, 8, 6)
grid = convert_int(ans)
grid_gt = convert_int(ans_gt)
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


visualize_grid(grid, save_dir_pic, save_dir_data, file_name)
visualize_grid(grid_gt, save_dir_gt, save_dir_data_gt,file_name)