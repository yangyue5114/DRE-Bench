# shape_declarative.py
import numpy as np

def expand_matrix_declarative(initial_matrix):
    """
    Expands a 3x3 matrix to a 9x9 using the Kronecker product.
    This approach is declarative, specifying the 'what' not the 'how'.
    
    Rule: A cell with '3' becomes the initial matrix, a cell with '0' becomes a zero block.
    This is equivalent to the Kronecker product of the initial matrix (scaled to 0s and 1s)
    and the initial matrix itself.
    """
    # Scale the matrix so its elements are 0 or 1 instead of 0 or 3.
    # This acts as the "selector" grid.
    selector_grid = initial_matrix / 3
    
    # The Kronecker product multiplies each element of the selector_grid
    # by the entire initial_matrix, achieving the expansion in one operation.
    return np.kron(selector_grid, initial_matrix).astype(int)

def main():
    """Main function to demonstrate the declarative expansion."""
    print("本任务将根据分形规则，将随机的3x3矩阵扩展为9x9矩阵 (Declarative Style)。\n")
    
    for case_num in range(1, 5):
        print(f"--- 案例 {case_num} ---")
        
        # 1. Generate a random 3x3 matrix of 0s and 3s.
        initial_3x3_matrix = np.random.choice([0, 3], size=(3, 3))
        
        print("随机生成的初始 3x3 矩阵:")
        print(initial_3x3_matrix)
        
        # 2. Expand it using the declarative NumPy function.
        final_9x9_matrix = expand_matrix_declarative(initial_3x3_matrix)
        
        print("\n按规则扩展后的 9x9 矩阵:")
        print(final_9x9_matrix)
        print("-" * 25)

if __name__ == "__main__":
    main()