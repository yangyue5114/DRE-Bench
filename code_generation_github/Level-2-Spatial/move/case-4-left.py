import os, json
import random
from copy import deepcopy

# main


def gen(distance) -> tuple:
    lenx = 10
    leny = 30

    input_gird = [[0] * leny for _ in range(lenx)]
    
    color = random.randint(1, 9)

    def is_valid(x, y):
        return 0 <= x < lenx and 0 <= y < leny - distance and input_gird[x][y] == 0

    def get_neighbors(x, y):
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                neighbors.append((nx, ny))
        return neighbors

    def generate_connected_block():
        start_x, start_y = random.randint(0, lenx - 1), random.randint(0, leny - 1 - distance)
        input_gird[start_x][start_y] = color
        frontier = [(start_x, start_y)]
        cnt = 1
        while cnt < 6:
            x, y = random.choice(frontier)
            neighbors = get_neighbors(x, y)
            if neighbors:
                nx, ny = random.choice(neighbors)
                input_gird[nx][ny] = color
                cnt += 1
                frontier.append((nx, ny))
            else:
                frontier.remove((x, y))
                
    generate_connected_block()

    def move(grid):
        d_grid = deepcopy(grid)
        for i in range(leny - 1, -1, -1):
            for j in range(lenx):
                if i - distance >= 0:
                    d_grid[j][i] = d_grid[j][i - distance]
                else:
                    d_grid[j][i] = 0
        return d_grid
    
    output_gird = move(input_gird)

    return output_gird, input_gird

# main
data_folder = 'data/Move/left/data'
os.makedirs(data_folder, exist_ok=True)

result = {
    'train': [],
    'test': []
}
# train
# srun -p Gveval2-S1 --gres=gpu:0 --cpus-per-task=4 python /mnt/petrelfs/liuqihua.p/arc-dsl-3d/data/Move/left/vis.py
for var in range(1, 21):
    task_folder = os.path.join(data_folder, f'{var}')
    os.makedirs(task_folder, exist_ok=True)

    result['train'] = []
    for i in range(3):
        input_gird, output_gird = gen(var)
        result['train'].append({
            'input': input_gird,
            'output': output_gird
        })

    for idx in range(0, 30):
        task_file = os.path.join(task_folder, f'{idx}.json')
        
        result['test'] = []
        input_gird, output_gird = gen(var)
        result['test'].append({
            'input': input_gird,
            'output': output_gird
        })

        with open(task_file, 'w') as f:
            json.dump(result, f)





