import numpy as np

def expand_matrix(base: np.ndarray) -> np.ndarray:
    """
    将一个 3x3 矩阵按照分形规则扩展为 9x9。
    如果某个位置为 3，则将整个 base 矩阵填充到该 3x3 区域；否则填充全 0。
    
    Args:
        base (np.ndarray): 原始 3x3 矩阵，仅包含 0 和 3。
        
    Returns:
        np.ndarray: 扩展后的 9x9 矩阵。
    """
    result = np.zeros((9, 9), dtype=int)
    
    for i in range(3):
        for j in range(3):
            block = base if base[i, j] == 3 else 0
            result[i*3:(i+1)*3, j*3:(j+1)*3] = block

    return result

def generate_random_base() -> np.ndarray:
    """
    随机生成一个 3x3 的初始矩阵，元素为 0 或 3。
    
    Returns:
        np.ndarray: 随机生成的 3x3 矩阵。
    """
    return np.random.choice([0, 3], size=(3, 3))

def display_case(case_id: int, base: np.ndarray, expanded: np.ndarray) -> None:
    """
    打印一个扩展案例，包括原始和扩展矩阵。
    
    Args:
        case_id (int): 案例编号。
        base (np.ndarray): 初始 3x3 矩阵。
        expanded (np.ndarray): 扩展后的 9x9 矩阵。
    """
    print(f"\n--- 案例 {case_id} ---")
    print("初始 3x3 矩阵:")
    print(base)
    print("\n扩展后的 9x9 矩阵:")
    print(expanded)

def main():
    """
    主程序：生成多个案例，展示矩阵扩展效果。
    """
    num_cases = 4
    print("将 3x3 矩阵按规则扩展为 9x9：")
    
    for i in range(1, num_cases + 1):
        base = generate_random_base()
        expanded = expand_matrix(base)
        display_case(i, base, expanded)

if __name__ == "__main__":
    main()
