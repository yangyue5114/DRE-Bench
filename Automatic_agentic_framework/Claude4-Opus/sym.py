import numpy as np
import random
from typing import Tuple, Optional, List
from dataclasses import dataclass
from enum import Enum

class PlacementSide(Enum):
    """Represents which side of the symmetry axis to place patterns."""
    ABOVE = "above"
    BELOW = "below"

@dataclass
class Config:
    """Configuration for symmetry system."""
    CANVAS_HEIGHT: int = 11
    CANVAS_WIDTH: int = 20
    SYMMETRY_AXIS_ROW: int = 5  # Middle row (0-indexed)
    AXIS_COLOR: int = 1
    MAX_PATTERN_SIZE: int = 3
    MIN_PATTERN_SIZE: int = 1
    COLOR_RANGE: Tuple[int, int] = (2, 10)  # Avoid axis color
    MAX_PLACEMENT_ATTEMPTS: int = 100

@dataclass
class PatternInfo:
    """Information about a pattern and its placement."""
    pattern: np.ndarray
    original_position: Tuple[int, int]  # (y, x)
    reflected_position: Tuple[int, int]  # (y, x)

class SymmetryManager:
    """Manages symmetric pattern placement on a canvas."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.placed_patterns: List[PatternInfo] = []
    
    def create_canvas_with_axis(self) -> np.ndarray:
        """Creates a canvas with a horizontal symmetry axis."""
        canvas = np.zeros((self.config.CANVAS_HEIGHT, self.config.CANVAS_WIDTH), dtype=int)
        canvas[self.config.SYMMETRY_AXIS_ROW, :] = self.config.AXIS_COLOR
        return canvas
    
    def generate_random_pattern(self) -> np.ndarray:
        """Generates a random-sized pattern with random colors."""
        height = random.randint(self.config.MIN_PATTERN_SIZE, self.config.MAX_PATTERN_SIZE)
        width = random.randint(self.config.MIN_PATTERN_SIZE, self.config.MAX_PATTERN_SIZE)
        
        return np.random.randint(*self.config.COLOR_RANGE, size=(height, width))
    
    def calculate_reflection_position(self, original_pos: Tuple[int, int], 
                                    pattern_height: int) -> Tuple[int, int]:
        """
        Calculates the reflected position across the symmetry axis.
        
        Args:
            original_pos: (y, x) position of original pattern
            pattern_height: Height of the pattern
            
        Returns:
            (y, x) position of reflected pattern
        """
        y_orig, x_orig = original_pos
        axis_y = self.config.SYMMETRY_AXIS_ROW
        
        # Calculate reflection using the formula: y_refl = 2*axis_y - y_orig - height + 1
        y_refl = (2 * axis_y) - y_orig - pattern_height + 1
        
        return (y_refl, x_orig)
    
    def is_area_free(self, canvas: np.ndarray, position: Tuple[int, int], 
                    pattern_shape: Tuple[int, int]) -> bool:
        """
        Checks if a rectangular area on the canvas is free (contains only zeros).
        
        Args:
            canvas: The canvas to check
            position: Top-left position (y, x) of the area
            pattern_shape: (height, width) of the area to check
            
        Returns:
            True if area is free, False otherwise
        """
        y, x = position
        height, width = pattern_shape
        
        # Boundary check
        if (y < 0 or x < 0 or 
            y + height > self.config.CANVAS_HEIGHT or 
            x + width > self.config.CANVAS_WIDTH):
            return False
        
        # Check if area contains only zeros
        area = canvas[y:y + height, x:x + width]
        return np.all(area == 0)
    
    def place_pattern_at_position(self, canvas: np.ndarray, pattern: np.ndarray, 
                                position: Tuple[int, int]) -> np.ndarray:
        """Places a pattern at the specified position on the canvas."""
        y, x = position
        height, width = pattern.shape
        canvas[y:y + height, x:x + width] = pattern
        return canvas
    
    def get_valid_placement_bounds(self, pattern_height: int) -> Tuple[Optional[Tuple[int, int]], 
                                                                     Optional[Tuple[int, int]]]:
        """
        Gets valid placement bounds for a pattern above and below the axis.
        
        Args:
            pattern_height: Height of the pattern
            
        Returns:
            Tuple of (above_bounds, below_bounds) where each is (min_y, max_y) or None if invalid
        """
        axis_y = self.config.SYMMETRY_AXIS_ROW
        
        # Above axis bounds
        above_bounds = None
        if axis_y - pattern_height >= 0:
            above_bounds = (0, axis_y - pattern_height)
        
        # Below axis bounds
        below_bounds = None
        if axis_y + 1 <= self.config.CANVAS_HEIGHT - pattern_height:
            below_bounds = (axis_y + 1, self.config.CANVAS_HEIGHT - pattern_height)
        
        return above_bounds, below_bounds
    
    def place_symmetric_pattern(self, canvas: np.ndarray, pattern: np.ndarray) -> Tuple[bool, np.ndarray]:
        """
        Attempts to place a pattern and its reflection symmetrically on the canvas.
        
        Args:
            canvas: Canvas to place patterns on
            pattern: Pattern to place
            
        Returns:
            Tuple of (success, updated_canvas)
        """
        pattern_height, pattern_width = pattern.shape
        
        # Get placement bounds
        above_bounds, below_bounds = self.get_valid_placement_bounds(pattern_height)
        
        # If pattern is too large for either side
        if above_bounds is None and below_bounds is None:
            return False, canvas
        
        # Try multiple placement attempts
        for attempt in range(self.config.MAX_PLACEMENT_ATTEMPTS):
            # Choose a random side that can accommodate the pattern
            available_sides = []
            if above_bounds is not None:
                available_sides.append((PlacementSide.ABOVE, above_bounds))
            if below_bounds is not None:
                available_sides.append((PlacementSide.BELOW, below_bounds))
            
            if not available_sides:
                break
            
            # Random selection
            side, (min_y, max_y) = random.choice(available_sides)
            
            # Generate random position within bounds
            y_orig = random.randint(min_y, max_y)
            x_orig = random.randint(0, self.config.CANVAS_WIDTH - pattern_width)
            
            original_pos = (y_orig, x_orig)
            reflected_pos = self.calculate_reflection_position(original_pos, pattern_height)
            
            # Check if both positions are free
            if (self.is_area_free(canvas, original_pos, pattern.shape) and
                self.is_area_free(canvas, reflected_pos, pattern.shape)):
                
                # Place both patterns
                reflected_pattern = np.flipud(pattern)
                updated_canvas = canvas.copy()
                updated_canvas = self.place_pattern_at_position(updated_canvas, pattern, original_pos)
                updated_canvas = self.place_pattern_at_position(updated_canvas, reflected_pattern, reflected_pos)
                
                # Record successful placement
                pattern_info = PatternInfo(
                    pattern=pattern,
                    original_position=original_pos,
                    reflected_position=reflected_pos
                )
                self.placed_patterns.append(pattern_info)
                
                return True, updated_canvas
        
        return False, canvas
    
    def place_asymmetric_pattern(self, canvas: np.ndarray, pattern: np.ndarray) -> Tuple[bool, np.ndarray]:
        """
        Places a single (non-symmetric) pattern on the canvas.
        
        Args:
            canvas: Canvas to place pattern on
            pattern: Pattern to place
            
        Returns:
            Tuple of (success, updated_canvas)
        """
        pattern_height, pattern_width = pattern.shape
        above_bounds, below_bounds = self.get_valid_placement_bounds(pattern_height)
        
        for attempt in range(self.config.MAX_PLACEMENT_ATTEMPTS):
            # Choose random side
            side = random.choice([PlacementSide.ABOVE, PlacementSide.BELOW])
            
            if side == PlacementSide.ABOVE and above_bounds is not None:
                min_y, max_y = above_bounds
                y = random.randint(min_y, max_y)
            elif side == PlacementSide.BELOW and below_bounds is not None:
                min_y, max_y = below_bounds
                y = random.randint(min_y, max_y)
            else:
                continue
            
            x = random.randint(0, self.config.CANVAS_WIDTH - pattern_width)
            position = (y, x)
            
            if self.is_area_free(canvas, position, pattern.shape):
                updated_canvas = canvas.copy()
                updated_canvas = self.place_pattern_at_position(updated_canvas, pattern, position)
                return True, updated_canvas
        
        return False, canvas

class SymmetryDemo:
    """Demonstrates the symmetry pattern system."""
    
    def __init__(self, num_symmetric_pairs: int = 4, num_asymmetric: int = 0):
        self.manager = SymmetryManager()
        self.num_symmetric_pairs = num_symmetric_pairs
        self.num_asymmetric = num_asymmetric
    
    def run_demo(self):
        """Runs the complete symmetry demonstration."""
        print("=== Symmetric Pattern Placement System ===\n")
        
        # Create initial canvas
        canvas = self.manager.create_canvas_with_axis()
        
        print("--- Initial Canvas (with symmetry axis) ---")
        print(canvas)
        
        # Place symmetric patterns
        print(f"\n--- Placing {self.num_symmetric_pairs} symmetric pattern pairs ---")
        
        successful_placements = 0
        for i in range(self.num_symmetric_pairs):
            print(f"\n>>> Attempting to place symmetric pair {i + 1}")
            
            pattern = self.manager.generate_random_pattern()
            success, canvas = self.manager.place_symmetric_pattern(canvas, pattern)
            
            if success:
                successful_placements += 1
                latest_info = self.manager.placed_patterns[-1]
                print(f"✓ Success: Pattern {pattern.shape} placed at {latest_info.original_position} "
                      f"and reflected at {latest_info.reflected_position}")
            else:
                print(f"✗ Failed: Could not find space for pattern {pattern.shape}")
        
        print(f"\nSuccessfully placed {successful_placements}/{self.num_symmetric_pairs} symmetric pairs")
        
        # Place asymmetric patterns if requested
        if self.num_asymmetric > 0:
            print(f"\n--- Placing {self.num_asymmetric} asymmetric patterns ---")
            
            for i in range(self.num_asymmetric):
                pattern = self.manager.generate_random_pattern()
                success, canvas = self.manager.place_asymmetric_pattern(canvas, pattern)
                
                if success:
                    print(f"✓ Asymmetric pattern {i + 1} placed successfully")
                else:
                    print(f"✗ Failed to place asymmetric pattern {i + 1}")
        
        # Show final result
        print("\n--- Final Canvas ---")
        print("Symmetry axis (1) with symmetric patterns reflected across it:")
        print(canvas)
        
        return canvas

def validate_symmetry(canvas: np.ndarray, axis_row: int) -> bool:
    """
    Validates that non-axis patterns are properly symmetric.
    
    Args:
        canvas: Canvas to validate
        axis_row: Row index of symmetry axis
        
    Returns:
        True if symmetric patterns are valid, False otherwise
    """
    height, width = canvas.shape
    
    for x in range(width):
        for y in range(height):
            if y == axis_row:
                continue  # Skip axis row
            
            # Calculate corresponding symmetric position
            symmetric_y = 2 * axis_row - y
            
            # Check if symmetric position is within bounds
            if 0 <= symmetric_y < height:
                # For true symmetry, we'd need to check pattern boundaries
                # This is a simplified check
                if canvas[y, x] != 0 and canvas[symmetric_y, x] == 0:
                    return False
    
    return True

def main():
    """Main entry point for symmetry demonstration."""
    demo = SymmetryDemo(num_symmetric_pairs=4, num_asymmetric=2)
    final_canvas = demo.run_demo()
    
    # Optional: Validate symmetry
    print("\n=== Symmetry Validation ===")
    config = Config()
    is_valid = validate_symmetry(final_canvas, config.SYMMETRY_AXIS_ROW)
    print(f"Canvas symmetry is valid: {is_valid}")

if __name__ == "__main__":
    main()