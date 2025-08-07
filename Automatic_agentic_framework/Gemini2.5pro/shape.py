import numpy as np

def expand_matrix_according_to_rule(initial_matrix):
    """
    根据指定的分形规则，将一个3x3矩阵扩展为一个9x9矩阵。

    参数:
    - initial_matrix (np.ndarray): 一个3x3的输入矩阵，由0和3组成。

    返回:
    - np.ndarray: 扩展后的9x9结果矩阵。
    """
    # 准备一个9x9的空白画布（结果矩阵），用0填充
    final_matrix = np.zeros((9, 9), dtype=int)
    
    # 准备一个3x3的全0矩阵，用于填充
    zero_block = np.zeros((3, 3), dtype=int)

    # 遍历初始3x3矩阵的每一个单元格
    for i in range(3):
        for j in range(3):
            # 计算当前单元格在9x9大矩阵中对应的3x3区域的起始坐标
            start_row = i * 3
            start_col = j * 3
            
            # 获取当前单元格的值 (0 或 3)
            cell_value = initial_matrix[i, j]
            
            # 根据规则进行填充
            if cell_value == 3:
                # 如果值为3，则将整个初始矩阵填充到这个3x3区域
                final_matrix[start_row : start_row + 3, start_col : start_col + 3] = initial_matrix
            else: # 如果值为0
                # 如果值为0，则用全0矩阵填充这个3x3区域
                final_matrix[start_row : start_row + 3, start_col : start_col + 3] = zero_block
                
    return final_matrix


def main():
    """
    主函数，循环4次，每次都生成并展示一次矩阵扩展。
    """
    print("本任务将根据分形规则，将随机的3x3矩阵扩展为9x9矩阵。\n")
    
    # 定义要生成的案例数量
    number_of_cases = 4
    
    for case_num in range(1, number_of_cases + 1):
        print(f"--- 案例 {case_num} ---")
        
        # 1. 随机生成一个3x3的初始矩阵
        #    方法: 生成一个0和1的随机矩阵，然后乘以3，即可得到0和3的随机矩阵。
        initial_3x3_matrix = np.random.randint(0, 2, size=(3, 3)) * 3
        
        print("随机生成的初始 3x3 矩阵:")
        print(initial_3x3_matrix)
        
        # 2. 根据规则计算出9x9的结果矩阵
        final_9x9_matrix = expand_matrix_according_to_rule(initial_3x3_matrix)
        
        print("\n按规则扩展后的 9x9 矩阵:")
        print(final_9x9_matrix)
        print("-" * 25) # 分隔线

# --- 程序入口 ---
if __name__ == "__main__":
    main()