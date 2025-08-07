import numpy as np
import random
from typing import Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class Direction(Enum):
    """Valid movement directions."""
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'

@dataclass
class Config:
    """Configuration for the movement system."""
    CANVAS_HEIGHT: int = 10
    CANVAS_WIDTH: int = 20
    PATTERN_SIZE: int = 3
    BACKGROUND_COLOR: int = 0
    COLOR_RANGE: Tuple[int, int] = (1, 10)  # Exclusive upper bound

@dataclass
class Position:
    """Represents a 2D position."""
    y: int
    x: int
    
    def to_dict(self) -> Dict[str, int]:
        """Converts position to dictionary format."""
        return {'y': self.y, 'x': self.x}
    
    @classmethod
    def from_dict(cls, pos_dict: Dict[str, int]) -> 'Position':
        """Creates position from dictionary format."""
        return cls(y=pos_dict['y'], x=pos_dict['x'])

class MovementResult:
    """Result of a movement operation."""
    
    def __init__(self, success: bool, canvas: np.ndarray, position: Position, message: str = ""):
        self.success = success
        self.canvas = canvas
        self.position = position
        self.message = message

class PatternMover:
    """Handles pattern movement on a canvas."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
    
    def create_canvas(self) -> np.ndarray:
        """Creates an empty canvas."""
        return np.zeros((self.config.CANVAS_HEIGHT, self.config.CANVAS_WIDTH), dtype=int)
    
    def generate_random_pattern(self) -> np.ndarray:
        """Generates a random 3x3 pattern."""
        return np.random.randint(*self.config.COLOR_RANGE, 
                                size=(self.config.PATTERN_SIZE, self.config.PATTERN_SIZE))
    
    def get_random_valid_position(self, pattern: np.ndarray) -> Position:
        """Gets a random valid starting position for the pattern."""
        pattern_height, pattern_width = pattern.shape
        
        max_y = self.config.CANVAS_HEIGHT - pattern_height
        max_x = self.config.CANVAS_WIDTH - pattern_width
        
        if max_y < 0 or max_x < 0:
            raise ValueError("Pattern is too large for canvas")
        
        return Position(
            y=random.randint(0, max_y),
            x=random.randint(0, max_x)
        )
    
    def place_pattern(self, canvas: np.ndarray, pattern: np.ndarray, position: Position) -> np.ndarray:
        """Places a pattern at the specified position on the canvas."""
        p_height, p_width = pattern.shape
        canvas[position.y:position.y + p_height, position.x:position.x + p_width] = pattern
        return canvas
    
    def clear_pattern(self, canvas: np.ndarray, pattern: np.ndarray, position: Position) -> np.ndarray:
        """Clears a pattern from the specified position on the canvas."""
        p_height, p_width = pattern.shape
        canvas[position.y:position.y + p_height, position.x:position.x + p_width] = self.config.BACKGROUND_COLOR
        return canvas
    
    def move_pattern(self, canvas: np.ndarray, pattern: np.ndarray, 
                    current_pos: Position, direction: Direction, steps: int) -> MovementResult:
        """
        Moves a pattern on the canvas in the specified direction.
        
        Args:
            canvas: The canvas containing the pattern
            pattern: The pattern to move
            current_pos: Current position of the pattern
            direction: Direction to move
            steps: Number of steps to move
            
        Returns:
            MovementResult with success status, updated canvas and position
        """
        if steps < 0:
            return MovementResult(False, canvas, current_pos, "Steps must be non-negative")
        
        # Calculate new position
        new_position = self._calculate_new_position(current_pos, direction, steps)
        
        # Validate bounds
        if not self._is_position_valid(pattern, new_position):
            message = (f"Invalid move: from ({current_pos.y}, {current_pos.x}) "
                      f"{direction.value} {steps} steps would exceed bounds")
            return MovementResult(False, canvas, current_pos, message)
        
        # Perform the move
        updated_canvas = canvas.copy()
        self.clear_pattern(updated_canvas, pattern, current_pos)
        self.place_pattern(updated_canvas, pattern, new_position)
        
        message = (f"Success: Pattern moved from ({current_pos.y}, {current_pos.x}) "
                  f"to ({new_position.y}, {new_position.x})")
        
        return MovementResult(True, updated_canvas, new_position, message)
    
    def _calculate_new_position(self, current_pos: Position, direction: Direction, steps: int) -> Position:
        """Calculates new position based on direction and steps."""
        new_y, new_x = current_pos.y, current_pos.x
        
        if direction == Direction.UP:
            new_y -= steps
        elif direction == Direction.DOWN:
            new_y += steps
        elif direction == Direction.LEFT:
            new_x -= steps
        elif direction == Direction.RIGHT:
            new_x += steps
        
        return Position(y=new_y, x=new_x)
    
    def _is_position_valid(self, pattern: np.ndarray, position: Position) -> bool:
        """Checks if a position is valid for the given pattern."""
        pattern_height, pattern_width = pattern.shape
        
        return (0 <= position.y <= self.config.CANVAS_HEIGHT - pattern_height and
                0 <= position.x <= self.config.CANVAS_WIDTH - pattern_width)

class MovementDemo:
    """Demonstrates the pattern movement system."""
    
    def __init__(self):
        self.mover = PatternMover()
        self.canvas = None
        self.pattern = None
        self.position = None
    
    def run_demo(self):
        """Runs a complete movement demonstration."""
        print("=== Pattern Movement Demonstration ===\n")
        
        self._initialize()
        self._show_initial_state()
        self._execute_movement_sequence()
    
    def _initialize(self):
        """Initializes the demo environment."""
        print("--- 1. Initialization ---")
        
        # Create canvas and pattern
        self.canvas = self.mover.create_canvas()
        self.pattern = self.mover.generate_random_pattern()
        
        print("Generated 3x3 pattern:")
        print(self.pattern)
        
        # Get random starting position and place pattern
        self.position = self.mover.get_random_valid_position(self.pattern)
        self.canvas = self.mover.place_pattern(self.canvas, self.pattern, self.position)
    
    def _show_initial_state(self):
        """Shows the initial state of the canvas."""
        print("\n--- 2. Initial State ---")
        print("Initial canvas:")
        print(self.canvas)
        print(f"Pattern position (top-left y, x): ({self.position.y}, {self.position.x})")
    
    def _execute_movement_sequence(self):
        """Executes a sequence of movements."""
        print("\n--- 3. Movement Sequence ---")
        
        movements = [
            (Direction.RIGHT, 5),
            (Direction.DOWN, 3),
            (Direction.LEFT, 10),
            (Direction.UP, 10),  # This should fail
            (Direction.UP, 2)    # This should succeed
        ]
        
        for i, (direction, steps) in enumerate(movements, 1):
            print(f"\n>>> Operation {i}: Move {direction.value} {steps} steps")
            
            result = self.mover.move_pattern(
                self.canvas, self.pattern, self.position, direction, steps
            )
            
            print(result.message)
            
            if result.success:
                self.canvas = result.canvas
                self.position = result.position
                print(self.canvas)
            else:
                print("Canvas and position remain unchanged:")
                print(self.canvas)
            
            print(f"Current position: ({self.position.y}, {self.position.x})")

def main():
    """Main entry point."""
    demo = MovementDemo()
    demo.run_demo()

if __name__ == "__main__":
    main()