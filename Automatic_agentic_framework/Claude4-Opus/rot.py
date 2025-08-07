import numpy as np
import math
from typing import List, Tuple, NamedTuple
from dataclasses import dataclass

@dataclass
class Config:
    """Configuration for rotation system."""
    CANVAS_SIZE: int = 13
    LINE_LENGTH: int = 5  # Length from center (excluding center point)
    TOP_ENDPOINT_COLOR: int = 7
    LINE_BODY_COLOR: int = 4
    BOTTOM_ENDPOINT_COLOR: int = 9
    BACKGROUND_COLOR: int = 0

class Point(NamedTuple):
    """Represents a point with coordinates and color."""
    y: int
    x: int
    color: int

class LineRotator:
    """Handles rotation of lines around a center point."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.center = self.config.CANVAS_SIZE // 2
    
    def create_vertical_line(self) -> List[Point]:
        """
        Creates a vertical line centered on the canvas.
        
        Returns:
            List of points representing the line from bottom to top
        """
        line_points = []
        
        # Bottom endpoint (center point)
        line_points.append(Point(
            y=self.center, 
            x=self.center, 
            color=self.config.BOTTOM_ENDPOINT_COLOR
        ))
        
        # Line body (from center upward, excluding endpoints)
        for i in range(1, self.config.LINE_LENGTH):
            line_points.append(Point(
                y=self.center - i,
                x=self.center,
                color=self.config.LINE_BODY_COLOR
            ))
        
        # Top endpoint
        line_points.append(Point(
            y=self.center - self.config.LINE_LENGTH,
            x=self.center,
            color=self.config.TOP_ENDPOINT_COLOR
        ))
        
        return line_points
    
    def rotate_point(self, point: Point, angle_degrees: float) -> Point:
        """
        Rotates a point around the canvas center.
        
        Args:
            point: Point to rotate
            angle_degrees: Rotation angle in degrees
            
        Returns:
            New point at rotated position with same color
        """
        # Convert to radians
        angle_radians = math.radians(angle_degrees)
        
        # Translate to origin
        translated_x = point.x - self.center
        translated_y = point.y - self.center
        
        # Apply rotation matrix
        rotated_x = translated_x * math.cos(angle_radians) - translated_y * math.sin(angle_radians)
        rotated_y = translated_x * math.sin(angle_radians) + translated_y * math.cos(angle_radians)
        
        # Translate back and round to nearest integer
        new_x = int(round(rotated_x + self.center))
        new_y = int(round(rotated_y + self.center))
        
        return Point(y=new_y, x=new_x, color=point.color)
    
    def rotate_line(self, line_points: List[Point], angle_degrees: float) -> List[Point]:
        """
        Rotates all points in a line by the specified angle.
        
        Args:
            line_points: List of points representing the line
            angle_degrees: Rotation angle in degrees
            
        Returns:
            List of rotated points
        """
        return [self.rotate_point(point, angle_degrees) for point in line_points]
    
    def render_line_to_canvas(self, line_points: List[Point]) -> np.ndarray:
        """
        Renders a line to a canvas.
        
        Args:
            line_points: List of points to render
            
        Returns:
            Canvas with the line rendered
        """
        canvas = np.zeros((self.config.CANVAS_SIZE, self.config.CANVAS_SIZE), dtype=int)
        
        for point in line_points:
            # Boundary check
            if (0 <= point.y < self.config.CANVAS_SIZE and 
                0 <= point.x < self.config.CANVAS_SIZE):
                canvas[point.y, point.x] = point.color
        
        return canvas
    
    def generate_rotation_sequence(self, angles: List[float]) -> List[Tuple[float, np.ndarray]]:
        """
        Generates a sequence of rotated line canvases.
        
        Args:
            angles: List of rotation angles in degrees
            
        Returns:
            List of tuples (angle, canvas)
        """
        original_line = self.create_vertical_line()
        results = []
        
        for angle in angles:
            rotated_line = self.rotate_line(original_line, angle)
            canvas = self.render_line_to_canvas(rotated_line)
            results.append((angle, canvas))
        
        return results

class RotationDemo:
    """Demonstrates the line rotation system."""
    
    def __init__(self):
        self.rotator = LineRotator()
        self.standard_angles = [0, 45, 90, 135, 180, 225, 270, 315, 360]
    
    def run_demo(self):
        """Runs the complete rotation demonstration."""
        print("=== Line Rotation Demonstration ===")
        print("Rotating a vertical line around the canvas center.\n")
        
        # Generate all rotations
        rotation_sequence = self.rotator.generate_rotation_sequence(self.standard_angles)
        
        # Display results
        for angle, canvas in rotation_sequence:
            self._display_rotation(angle, canvas)
    
    def _display_rotation(self, angle: float, canvas: np.ndarray):
        """Displays a single rotation result."""
        if angle == 0:
            print("--- Initial State (0 degrees) ---")
        else:
            print(f"--- Rotation {int(angle)} degrees ---")
        
        print(canvas)
        print()
    
    def demonstrate_custom_angles(self, custom_angles: List[float]):
        """Demonstrates rotation with custom angles."""
        print("=== Custom Angle Demonstration ===")
        
        rotation_sequence = self.rotator.generate_rotation_sequence(custom_angles)
        
        for angle, canvas in rotation_sequence:
            print(f"--- Rotation {angle} degrees ---")
            print(canvas)
            print()

def validate_rotation_properties(rotator: LineRotator):
    """
    Validates mathematical properties of rotation.
    
    Args:
        rotator: LineRotator instance to test
    """
    print("=== Rotation Validation ===")
    
    original_line = rotator.create_vertical_line()
    
    # Test 360-degree rotation equals original
    rotated_360 = rotator.rotate_line(original_line, 360)
    canvas_original = rotator.render_line_to_canvas(original_line)
    canvas_360 = rotator.render_line_to_canvas(rotated_360)
    
    is_360_equal = np.array_equal(canvas_original, canvas_360)
    print(f"360-degree rotation equals original: {is_360_equal}")
    
    # Test 180-degree rotation twice equals original
    rotated_180_twice = rotator.rotate_line(
        rotator.rotate_line(original_line, 180), 180
    )
    canvas_180_twice = rotator.render_line_to_canvas(rotated_180_twice)
    
    is_180_twice_equal = np.array_equal(canvas_original, canvas_180_twice)
    print(f"Two 180-degree rotations equal original: {is_180_twice_equal}")
    
    # Test center point remains fixed
    center_point = Point(y=rotator.center, x=rotator.center, color=1)
    rotated_center = rotator.rotate_point(center_point, 45)
    
    center_fixed = (rotated_center.y == rotator.center and 
                   rotated_center.x == rotator.center)
    print(f"Center point remains fixed during rotation: {center_fixed}")

def main():
    """Main entry point for rotation demonstration."""
    demo = RotationDemo()
    demo.run_demo()
    
    # Optional: Validate rotation properties
    print()
    validate_rotation_properties(demo.rotator)
    
    # Optional: Demonstrate custom angles
    print("\n")
    custom_angles = [30, 60, 120, 150, 240, 300]
    demo.demonstrate_custom_angles(custom_angles)

if __name__ == "__main__":
    main()