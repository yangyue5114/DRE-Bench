import os, json
import random
from copy import deepcopy
import numpy as np
import math
# main


def gen(var) -> tuple:
    lenx = 25
    leny = 25

    input_grid = [[8] * leny for _ in range(lenx)]

    lx = random.randint(max(2, int(math.sqrt(var)) - 1), min(var // 2, int(math.sqrt(var)) + 1))
    ly = var // lx

    # 左边10格 模式
    border = 10
    sx, sy = random.randint(1, 9 - lx), random.randint(1, leny - 2 - ly)
    for i in range(sx, sx + lx):
        for j in range(sy, sy + ly):
            input_grid[i][j] = 0
    
    centercol = random.randint(1, 3)
    cx, cy = random.randint(sx, sx + lx - 1), random.randint(sy, sy + ly - 1)
    input_grid[cx][cy] = centercol

    def check(x, y):
        if x < sx or x >= sx + lx or y < sy or y >= sy + ly:
            return False
        return True

    nx, ny = cx, cy
    queue = []
    for i in range(var // 3 * 2):
        dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        while check(nx + dx, ny + dy) == False:
            dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        queue.append((dx, dy))
        nx += dx
        ny += dy
        if nx != cx or ny != cy:
            input_grid[nx][ny] = 4

    # 右边
    Lx = random.randint(lx + 1, 12)
    Ly = random.randint(ly + 1, 12)

    Sx, Sy = random.randint(11, 23 - Lx), random.randint(1, leny - 2 - Ly)
    for i in range(Sx, Sx + Lx):
        for j in range(Sy, Sy + Ly):
            input_grid[i][j] = 0

    Cx, Cy = random.randint(Sx + cx - sx, Sx + Lx - 1 - (sx + lx - 1 - cx)), random.randint(Sy + cy - sy, Sy + Ly - 1 - (sy + ly - 1 - cy))
    input_grid[Cx][Cy] = centercol

    output_grid = [[0] * Ly for _ in range(Lx)]
    nx, ny = Cx - Sx, Cy - Sy
    for dx, dy in queue:
        nx += dx
        ny += dy
        output_grid[nx][ny] = 4
    
    output_grid[Cx - Sx][Cy - Sy] = centercol

    tg = random.randint(0, 1)
    if tg == 0:
        input_grid = [row[::-1] for row in input_grid]
        output_grid = [row[::-1] for row in output_grid]

    return input_grid, output_grid
    
# main
data_folder = 'data/Shape/2f0c5170/data'
os.makedirs(data_folder, exist_ok=True)

result = {
    'train': [],
    'test': []
}
# train
input_grid, output_grid = gen(10)
result['train'].append({
    'input': input_grid,
    'output': output_grid
})
input_grid, output_grid = gen(30)
result['train'].append({
    'input': input_grid,
    'output': output_grid
})
input_grid, output_grid = gen(50)
result['train'].append({
    'input': input_grid,
    'output': output_grid
})
# test
for var in range(10, 51, 5):
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





