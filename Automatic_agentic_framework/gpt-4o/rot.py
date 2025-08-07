import random
import numpy as np

class FallingObject:
    """Represents a single 3x1 falling object with its own properties."""

    def __init__(self, x_coord: int, colors: np.ndarray):
        self.x = x_coord
        self.colors = colors  # Shape: (3,)
        self.height = 3


class GravityScene:
    """Manages the 2D scene with falling objects and a generated ground."""

    def __init__(self, height: int, width: int, num_objects: int):
        self.height = height
        self.width = width
        self.num_objects = num_objects
        self.grid = np.zeros((height, width), dtype=int)
        self.ground_color = 1
        self.ground_top_levels: dict[int, int] = {}
        self.objects_to_fall: list[FallingObject] = []

    def _generate_ground(self) -> None:
        """Randomly generate undulating ground level for each column."""
        for x in range(self.width):
            ground_height = random.randint(1, 4)
            top_y = self.height - ground_height
            self.grid[top_y:, x] = self.ground_color
            self.ground_top_levels[x] = top_y

    def _generate_objects(self) -> None:
        """Create colored 3x1 objects and place them at the top of the grid."""
        available_columns = list(range(self.width))
        random.shuffle(available_columns)

        while len(self.objects_to_fall) < self.num_objects and available_columns:
            x = available_columns.pop()
            if self.ground_top_levels.get(x, 0) < 3:
                continue

            colors = np.random.randint(2, 10, size=3)
            obj = FallingObject(x, colors)
            self.objects_to_fall.append(obj)

            # Place the object at the top of the grid
            self.grid[:obj.height, x] = obj.colors

    def create_initial_scene(self) -> np.ndarray:
        """Build initial scene with terrain and object placement."""
        self._generate_ground()
        self._generate_objects()
        return self.grid

    def simulate_gravity(self) -> np.ndarray:
        """Simulate gravity, placing each object above the ground."""
        final_grid = np.zeros_like(self.grid)

        for x, top_y in self.ground_top_levels.items():
            final_grid[top_y:, x] = self.ground_color

        for obj in self.objects_to_fall:
            landing_start_y = self.ground_top_levels[obj.x] - obj.height
            final_grid[landing_start_y : landing_start_y + obj.height, obj.x] = obj.colors

        return final_grid


if __name__ == "__main__":
    scene = GravityScene(height=10, width=20, num_objects=8)

    print("--- 初始矩阵 (OOP Style) ---")
    initial = scene.create_initial_scene()
    print(initial)

    print("\n--- 变化后的矩阵 (模拟重力后) ---")
    final = scene.simulate_gravity()
    print(final)
