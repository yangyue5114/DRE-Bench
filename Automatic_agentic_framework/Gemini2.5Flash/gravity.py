# gravity_oop.py
import numpy as np
import random

class FallingObject:
    """Represents a single 3x1 object with its own properties."""
    def __init__(self, x_coord, colors):
        self.x = x_coord
        self.colors = colors
        self.height = 3

class GravityScene:
    """Manages the scene, including the grid, ground, and all objects."""
    def __init__(self, height, width, num_objects):
        self.height = height
        self.width = width
        self.num_objects = num_objects
        self.grid = np.zeros((height, width), dtype=int)
        self.ground_color = 1
        self.ground_top_levels = {}
        self.objects_to_fall = []

    def _generate_ground(self):
        """Creates a randomly undulating ground level."""
        for x in range(self.width):
            ground_height = random.randint(1, 4)
            top_y = self.height - ground_height
            self.grid[top_y:, x] = self.ground_color
            self.ground_top_levels[x] = top_y

    def _generate_objects(self):
        """Creates and places falling objects at the top of the grid."""
        available_columns = list(range(self.width))
        random.shuffle(available_columns)
        
        count = 0
        while count < self.num_objects and available_columns:
            x = available_columns.pop()
            
            # Skip if there isn't enough vertical space for the object to fall
            if self.ground_top_levels[x] < 3:
                continue

            colors = np.random.randint(2, 10, size=3)
            new_obj = FallingObject(x, colors)
            self.objects_to_fall.append(new_obj)
            
            # Place object visually at the top
            self.grid[0:new_obj.height, x] = new_obj.colors
            count += 1
            
    def create_initial_scene(self):
        """Builds the complete initial scene with ground and objects."""
        self._generate_ground()
        self._generate_objects()
        return self.grid

    def simulate_gravity(self):
        """Calculates the final state of the grid after objects have fallen."""
        final_grid = np.zeros((self.height, self.width), dtype=int)
        
        # Re-draw the ground on the new grid
        for x, top_y in self.ground_top_levels.items():
            final_grid[top_y:, x] = self.ground_color
            
        # Place each object in its final resting position
        for obj in self.objects_to_fall:
            ground_top_y = self.ground_top_levels[obj.x]
            landing_start_y = ground_top_y - obj.height
            final_grid[landing_start_y : landing_start_y + obj.height, obj.x] = obj.colors
            
        return final_grid

# --- Main Execution ---
if __name__ == "__main__":
    NUMBER_OF_OBJECTS = 8
    
    # 1. Instantiate the scene
    scene = GravityScene(height=10, width=20, num_objects=NUMBER_OF_OBJECTS)
    
    # 2. Create the initial state
    initial_matrix = scene.create_initial_scene()
    print("--- 初始矩阵 (OOP Style) ---")
    print("地面由1表示，上方是待下落的色块:")
    print(initial_matrix)
    
    # 3. Simulate gravity to get the final state
    final_matrix = scene.simulate_gravity()
    print("\n--- 变化后的矩阵 (模拟重力后) ---")
    print("色块已落在地面上:")
    print(final_matrix)