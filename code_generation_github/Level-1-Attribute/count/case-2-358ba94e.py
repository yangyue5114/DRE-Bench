import os, json
import random
from copy import deepcopy

# main


def gen(var) -> tuple:
    lenx = 20
    leny = 20

    input_gird = [[0] * leny for _ in range(lenx)]
    color = random.randint(1, 9)

    visited = [[0] * leny for _ in range(lenx)]

    def check(x, y):
        if x + 4 >= lenx or y + 4 >= leny:
            return False
        for i in range(x, x + 5):
            for j in range(y, y + 5):
                if visited[i][j] == 1:
                    return False
        return True

    def find():
        tag = 0
        for i in range(lenx):
            for j in range(leny):
                if check(i, j):
                    tag = 1
                    break
        if tag == 0:
            return -1, -1
        x, y = random.randint(0, lenx - 1), random.randint(0, leny - 1)
        while True:
            if check(x, y):
                break
            x, y = random.randint(0, lenx - 1), random.randint(0, leny - 1)
        return x, y
    
    tag = 0
    pattern = random.sample(range(1, 9), 2)
    random.shuffle(pattern)
    s_1 = random.sample(range(0, 9), pattern[0])
    s_2 = random.sample(range(0, 9), pattern[1])
    pattern_matrix = [[0 if x in s_1 else color for x in range(0, 9)],
                [0 if x in s_2 else color for x in range(0, 9)]]
   
    while True:
        if tag == 1:
            break
        input_gird = [[0] * leny for _ in range(lenx)]
        visited = [[0] * leny for _ in range(lenx)]
        x, y = find()
        assert x != -1 and y != -1
        for i in range(x, x + 5):
            for j in range(y, y + 5):
                input_gird[i][j] = color if i == x or i == x + 4 or j ==  y or j == y + 4 else pattern_matrix[0][(i - x - 1) * 3 + (j - y - 1)]
                
        for i in range(max(0, x - 1), min(lenx, x + 6)):
            for j in range(max(0, y - 1), min(leny, y + 6)):
                visited[i][j] = 1
        tag = 1
        for _ in range(var - 1):
            x, y = find()
            if (x == -1 and y == -1):
                tag = 0
                break
            for i in range(x, x + 5):
                for j in range(y, y + 5):
                    input_gird[i][j] = color if i == x or i == x + 4 or j ==  y or j == y + 4 else pattern_matrix[1][(i - x - 1) * 3 + (j - y - 1)]
            for i in range(max(0, x - 1), min(lenx, x + 6)):
                        for j in range(max(0, y - 1), min(leny, y + 6)):
                            visited[i][j] = 1

    output_gird = [[color] * 5 for _ in range(5)]
    for i in range(1, 4):
        for j in range(1, 4):
            output_gird[i][j] = pattern_matrix[0][(i - 1) * 3 + j - 1]
    
    return input_gird, output_gird
        
# main
data_folder = 'data/Number_series-count/358ba94e/data'
os.makedirs(data_folder, exist_ok=True)

result = {
    'train': [],
    'test': []
}
# train
input_gird, output_gird = gen(3)
result['train'].append({
    'input': input_gird,
    'output': output_gird
})
input_gird, output_gird = gen(4)
result['train'].append({
    'input': input_gird,
    'output': output_gird
})
input_gird, output_gird = gen(5)
result['train'].append({
    'input': input_gird,
    'output': output_gird
})
# test
for var in range(3, 8):
    task_folder = os.path.join(data_folder, f'{var}')
    os.makedirs(task_folder, exist_ok=True)

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




