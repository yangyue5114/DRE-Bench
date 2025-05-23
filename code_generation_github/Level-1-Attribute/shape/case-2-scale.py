import os, json
import random
from copy import deepcopy
import numpy as np
import math
# main
def gen(var) -> tuple:
    lenx = 3
    leny = 3
    
    input_grid = [[0 for j in range(leny)] for i in range(lenx)]
    choices_list = random.sample(range(0, 9), var)
    color = random.randint(1, 9)
    
    for i in range(lenx):
        for j in range(leny):
            if i * 3 + j in choices_list:
                input_grid[i][j] = color
    
    output_grid = [[0 for j in range(3 * leny)] for i in range(3 * lenx)]
    for i in range(lenx):
        for j in range(leny):
            if input_grid[i][j] != 0:
                for k in range(3):
                    for l in range(3):
                        output_grid[i * 3 + k][j * 3 + l] = input_grid[k][l]

    return input_grid, output_grid
    
# main
data_folder = 'data/Shape/scale/data'
os.makedirs(data_folder, exist_ok=True)

result = {
    'train': [],
    'test': []
}
# train
input_grid, output_grid = gen(1)
result['train'].append({
    'input': input_grid,
    'output': output_grid
})
input_grid, output_grid = gen(2)
result['train'].append({
    'input': input_grid,
    'output': output_grid
})
input_grid, output_grid = gen(3)
result['train'].append({
    'input': input_grid,
    'output': output_grid
})
# test
for var in range(1, 7):
    task_folder = os.path.join(data_folder, f'{var}')
    os.makedirs(task_folder, exist_ok=True)

    for idx in range(0, 30):
        task_file = os.path.join(task_folder, f'{idx}.json')
        
        result['test'] = []
        input_grid, output_grid = gen(var)
        result['test'].append({
            'input': input_grid,
            'output': output_grid
        })

        with open(task_file, 'w') as f:
            json.dump(result, f)





