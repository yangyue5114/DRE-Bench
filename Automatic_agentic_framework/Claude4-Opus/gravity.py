import numpy as np
import random
from typing import Dict, List, Tuple, NamedTuple

class Config:
    """Configuration constants for the gravity simulation."""
    HEIGHT = 10
    WIDTH = 20
    GROUND_COLOR = 1
    COLOR_RANGE = (2, 10)  # Exclusive upper bound
    BLOCK_SIZE = 3

class BlockInfo(NamedTuple):
    """Information about a falling block."""
    colors: np.ndarray
    x: int

class GravitySimulator:
    """Simulates falling blocks with gravity physics."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
    
    def create_initial_scene(self, num_blocks: int) -> Tuple[np.ndarray, List[BlockInfo], Dict[int, int]]:
        """
        Creates initial scene with ground and falling blocks.
        
        Args:
            num_blocks: Number of 3x1 blocks to generate
            
        Returns:
            Tuple of (grid, blocks_info, ground_levels)
        """
        if num_blocks < 0:
            raise ValueError("Number of blocks must be non-negative")
        
        # Initialize empty canvas
        grid = np.zeros((self.config.HEIGHT, self.config.WIDTH), dtype=int)
        
        # Generate ground with random heights
        ground_levels = self._generate_ground(grid)
        
        # Place blocks
        blocks_info = self._place_blocks(grid, ground_levels, num_blocks)
        
        return grid, blocks_info, ground_levels
    
    def _generate_ground(self, grid: np.ndarray) -> Dict[int, int]:
        """Generates random ground heights."""
        ground_levels = {}
        
        for x in range(self.config.WIDTH):
            ground_height = random.randint(1, 4)
            top_y = self.config.HEIGHT - ground_height
            grid[top_y:, x] = self.config.GROUND_COLOR
            ground_levels[x] = top_y
        
        return ground_levels
    
    def _place_blocks(self, grid: np.ndarray, ground_levels: Dict[int, int], 
                     num_blocks: int) -> List[BlockInfo]:
        """Places blocks at the top of the grid."""
        blocks_info = []
        available_columns = list(range(self.config.WIDTH))
        random.shuffle(available_columns)
        
        placed_count = 0
        while placed_count < num_blocks and available_columns:
            x = available_columns.pop()
            
            # Check if column has enough space for 3x1 block
            if ground_levels[x] < self.config.BLOCK_SIZE:
                continue
            
            # Generate random colors for the block
            colors = np.random.randint(*self.config.COLOR_RANGE, size=self.config.BLOCK_SIZE)
            
            # Place block at top
            grid[0:self.config.BLOCK_SIZE, x] = colors
            
            blocks_info.append(BlockInfo(colors=colors, x=x))
            placed_count += 1
        
        return blocks_info
    
    def apply_gravity(self, blocks_info: List[BlockInfo], 
                     ground_levels: Dict[int, int]) -> np.ndarray:
        """
        Applies gravity to blocks and returns final state.
        
        Args:
            blocks_info: List of block information
            ground_levels: Ground height information
            
        Returns:
            Final grid after gravity is applied
        """
        # Create new grid with only ground
        final_grid = np.zeros((self.config.HEIGHT, self.config.WIDTH), dtype=int)
        
        # Restore ground
        for x, top_y in ground_levels.items():
            final_grid[top_y:, x] = self.config.GROUND_COLOR
        
        # Apply gravity to each block
        for block in blocks_info:
            self._place_fallen_block(final_grid, block, ground_levels[block.x])
        
        return final_grid
    
    def _place_fallen_block(self, grid: np.ndarray, block: BlockInfo, ground_top_y: int):
        """Places a single block after it has fallen due to gravity."""
        landing_start_y = ground_top_y - self.config.BLOCK_SIZE
        grid[landing_start_y:landing_start_y + self.config.BLOCK_SIZE, block.x] = block.colors

def main():
    """Main demonstration of the gravity simulation."""
    NUM_BLOCKS = 8
    
    simulator = GravitySimulator()
    
    print("=== Gravity Simulation ===\n")
    
    # Create initial scene
    initial_grid, blocks, ground_info = simulator.create_initial_scene(NUM_BLOCKS)
    
    print("--- Initial State ---")
    print("Ground represented by 1, falling blocks above:")
    print(initial_grid)
    
    # Apply gravity
    final_grid = simulator.apply_gravity(blocks, ground_info)
    
    print("\n--- After Gravity Applied ---")
    print("Blocks have fallen and landed on ground:")
    print(final_grid)

if __name__ == "__main__":
    main()