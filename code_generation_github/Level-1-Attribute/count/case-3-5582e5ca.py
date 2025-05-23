import os, json
import random
from copy import deepcopy

# main


def gen(var) -> tuple:
    lenx = 5
    leny = lenx

    input_gird = [[0] * leny for _ in range(lenx)]
    
    colors = random.sample([i for i in range(1, 10)], var)
    color_counts = {color: 1 for color in colors}
    for col in colors:
        x, y = random.randint(0, lenx - 1), random.randint(0, leny - 1)
        while input_gird[x][y] != 0:
            x, y = random.randint(0, lenx - 1), random.randint(0, leny - 1)
        input_gird[x][y] = col

    for i in range(lenx):
        for j in range(leny):
            if input_gird[i][j] != 0:
                continue
            color = random.choice(colors)
            input_gird[i][j] = color
            color_counts[color] += 1
    
    max_count = max(color_counts.values())
    max_colors = [color for color, count in color_counts.items() if count == max_count]

    if len(max_colors) > 1:
        color_to_change = max_colors[0]
        target_color = max_colors[1]

        tag = 0
        for i in range(lenx):
            for j in range(leny):
                if input_gird[i][j] == color_to_change:
                    input_gird[i][j] = target_color
                    color_counts[color_to_change] -= 1
                    color_counts[target_color] += 1
                    tag = 1
                    break
            if tag == 1:
                break

    max_count = max(color_counts.values())
    max_colors = [color for color, count in color_counts.items() if count == max_count]
    assert len(max_colors) == 1, f"Error: {max_colors}"

    output_gird = [[max_colors[0]] * leny for _ in range(lenx)]

    return input_gird, output_gird

# main
data_folder = 'data/Number_series-count/5582e5ca/data'
os.makedirs(data_folder, exist_ok=True)

result = {
    'train': [],
    'test': []
}
# train
input_gird, output_gird = gen(2)
result['train'].append({
    'input': input_gird,
    'output': output_gird
})
input_gird, output_gird = gen(4)
result['train'].append({
    'input': input_gird,
    'output': output_gird
})
input_gird, output_gird = gen(6)
result['train'].append({
    'input': input_gird,
    'output': output_gird
})
# test
for var in range(2, 9):
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




