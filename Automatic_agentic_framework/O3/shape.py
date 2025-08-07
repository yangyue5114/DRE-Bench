# shape_block_composition.py
import numpy as np

def expand_with_blocks(matrix: np.ndarray) -> np.ndarray:
    """Expands a matrix using np.block for compositional construction."""
    # Create the two building blocks
    block_3 = matrix
    block_0 = np.zeros_like(matrix) # A zero block of the same shape
    
    # Create a grid of blocks based on the input matrix's values
    # A list comprehension builds the list of lists required by np.block
    block_grid = [
        [block_3 if cell == 3 else block_0 for cell in row]
        for row in matrix
    ]
    
    # Assemble the blocks into the final matrix
    return np.block(block_grid)

# --- Main Execution ---
if __name__ == "__main__":
    print("本任务将根据分形规则，将随机的3x3矩阵扩展为9x9矩阵 (Block Composition Style)。\n")
    for i in range(1, 5):
        print(f"--- 案例 {i} ---")
        initial_mat = np.random.randint(0, 2, size=(3, 3)) * 3
        print("初始 3x3 矩阵:\n", initial_mat)
        
        final_mat = expand_with_blocks(initial_mat)
        print("\n扩展后的 9x9 矩阵:\n", final_mat)
        print("-" * 25)