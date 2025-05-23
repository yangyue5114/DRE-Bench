import os, json
import random
from copy import deepcopy

# main


def gen(var) -> tuple:
    leny = 4 * var - 1
    lenx = 2 + 2 * var

    input_gird = [[0 for _ in range(leny)] for _ in range(lenx)]
    output_gird = deepcopy(input_gird)

    color = random.randint(1, 9)
    data = [i for i in range(1, var + 1)]
    random.shuffle(data)

    for i in range(var):
        val = data[i]
        for x in range(lenx):
            input_gird[x][4 * i] = color
            input_gird[x][4 * i + 1] = color
            input_gird[x][4 * i + 2] = color
            output_gird[x][4 * (val - 1)] = color
            output_gird[x][4 * (val - 1) + 1] = color
            output_gird[x][4 * (val - 1) + 2] = color

        choices = random.sample([i for i in range(1, lenx - 1) if i % 2 == 1], val)
        for x in choices:
            input_gird[x][4 * i + 1] = 0
            output_gird[x][4 * (val - 1) + 1] = 0

    return input_gird, output_gird

# main
data_folder = 'data/Number_series-sort/42a15761/data'
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
input_gird, output_gird = gen(5)
result['train'].append({
    'input': input_gird,
    'output': output_gird
})
input_gird, output_gird = gen(7)
result['train'].append({
    'input': input_gird,
    'output': output_gird
})
# test
for var in range(2, 10):
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




