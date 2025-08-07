import numpy as np
from typing import Optional
from dataclasses import dataclass

@dataclass
class Config:
    """Configuration for fractal generation."""
    INPUT_SIZE: int = 3
    OUTPUT_SIZE: int = 9
    FILL_VALUE: int = 3
    EMPTY_VALUE: int = 0
    SCALE_FACTOR: int = 3

class FractalGenerator:
    """Generates fractal patterns based on self-similar rules."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        
        if self.config.OUTPUT_SIZE != self.config.INPUT_SIZE * self.config.SCALE_FACTOR:
            raise ValueError("Output size must be input size multiplied by scale factor")
    
    def create_random_seed_matrix(self) -> np.ndarray:
        """
        Creates a random seed matrix with values 0 and FILL_VALUE.
        
        Returns:
            Random 3x3 matrix with binary values scaled to 0 and FILL_VALUE
        """
        # Generate binary matrix (0, 1) then scale to (0, FILL_VALUE)
        binary_matrix = np.random.randint(0, 2, size=(self.config.INPUT_SIZE, self.config.INPUT_SIZE))
        return binary_matrix * self.config.FILL_VALUE
    
    def expand_matrix(self, seed_matrix: np.ndarray) -> np.ndarray:
        """
        Expands a matrix according to fractal self-similarity rules.
        
        For each cell in the seed matrix:
        - If cell value equals FILL_VALUE: replace with the entire seed matrix
        - If cell value is 0: replace with zeros
        
        Args:
            seed_matrix: Input matrix to expand
            
        Returns:
            Expanded matrix (9x9 if input is 3x3)
        """
        if seed_matrix.shape != (self.config.INPUT_SIZE, self.config.INPUT_SIZE):
            raise ValueError(f"Seed matrix must be {self.config.INPUT_SIZE}x{self.config.INPUT_SIZE}")
        
        # Create output matrix
        expanded_matrix = np.zeros((self.config.OUTPUT_SIZE, self.config.OUTPUT_SIZE), dtype=int)
        
        # Create zero block for empty cells
        zero_block = np.zeros((self.config.INPUT_SIZE, self.config.INPUT_SIZE), dtype=int)
        
        # Process each cell in the seed matrix
        for i in range(self.config.INPUT_SIZE):
            for j in range(self.config.INPUT_SIZE):
                # Calculate target region in expanded matrix
                start_row = i * self.config.SCALE_FACTOR
                end_row = start_row + self.config.INPUT_SIZE
                start_col = j * self.config.SCALE_FACTOR
                end_col = start_col + self.config.INPUT_SIZE
                
                # Apply fractal rule
                if seed_matrix[i, j] == self.config.FILL_VALUE:
                    # Replace with seed matrix itself
                    expanded_matrix[start_row:end_row, start_col:end_col] = seed_matrix
                else:
                    # Replace with zeros (already zeros, but explicit for clarity)
                    expanded_matrix[start_row:end_row, start_col:end_col] = zero_block
        
        return expanded_matrix
    
    def generate_fractal_case(self, case_number: Optional[int] = None) -> tuple[np.ndarray, np.ndarray]:
        """
        Generates a single fractal case.
        
        Args:
            case_number: Optional case number for display purposes
            
        Returns:
            Tuple of (seed_matrix, expanded_matrix)
        """
        seed_matrix = self.create_random_seed_matrix()
        expanded_matrix = self.expand_matrix(seed_matrix)
        
        return seed_matrix, expanded_matrix
    
    def display_case(self, seed_matrix: np.ndarray, expanded_matrix: np.ndarray, case_number: int):
        """Displays a fractal case with proper formatting."""
        print(f"--- Case {case_number} ---")
        print(f"Random {self.config.INPUT_SIZE}x{self.config.INPUT_SIZE} seed matrix:")
        print(seed_matrix)
        print(f"\nExpanded {self.config.OUTPUT_SIZE}x{self.config.OUTPUT_SIZE} fractal matrix:")
        print(expanded_matrix)
        print("-" * 30)

class FractalDemo:
    """Demonstrates the fractal generation system."""
    
    def __init__(self, num_cases: int = 4):
        self.generator = FractalGenerator()
        self.num_cases = num_cases
    
    def run_demo(self):
        """Runs the complete fractal demonstration."""
        print("=== Fractal Pattern Generator ===")
        print("Generates fractals using self-similarity rules.\n")
        
        for case_num in range(1, self.num_cases + 1):
            seed_matrix, expanded_matrix = self.generator.generate_fractal_case(case_num)
            self.generator.display_case(seed_matrix, expanded_matrix, case_num)
    
    def generate_single_case(self, case_number: int = 1) -> tuple[np.ndarray, np.ndarray]:
        """Generates and displays a single fractal case."""
        seed_matrix, expanded_matrix = self.generator.generate_fractal_case()
        self.generator.display_case(seed_matrix, expanded_matrix, case_number)
        return seed_matrix, expanded_matrix

def validate_fractal_rules(generator: FractalGenerator, seed_matrix: np.ndarray, 
                          expanded_matrix: np.ndarray) -> bool:
    """
    Validates that the expanded matrix follows fractal rules correctly.
    
    Args:
        generator: FractalGenerator instance
        seed_matrix: Original seed matrix
        expanded_matrix: Expanded matrix to validate
        
    Returns:
        True if valid, False otherwise
    """
    config = generator.config
    
    for i in range(config.INPUT_SIZE):
        for j in range(config.INPUT_SIZE):
            start_row = i * config.SCALE_FACTOR
            end_row = start_row + config.INPUT_SIZE
            start_col = j * config.SCALE_FACTOR
            end_col = start_col + config.INPUT_SIZE
            
            region = expanded_matrix[start_row:end_row, start_col:end_col]
            
            if seed_matrix[i, j] == config.FILL_VALUE:
                # Should match seed matrix
                if not np.array_equal(region, seed_matrix):
                    return False
            else:
                # Should be all zeros
                if not np.all(region == 0):
                    return False
    
    return True

def main():
    """Main entry point for fractal generation."""
    demo = FractalDemo(num_cases=4)
    demo.run_demo()
    
    # Optional: Validate one case
    print("\n=== Validation Test ===")
    generator = FractalGenerator()
    seed, expanded = generator.generate_fractal_case()
    is_valid = validate_fractal_rules(generator, seed, expanded)
    print(f"Generated fractal is valid: {is_valid}")

if __name__ == "__main__":
    main()