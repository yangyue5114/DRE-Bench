# move_modular.py
import numpy as np
import random

class MovableEntity:
    """A reusable class for an object that can move on a 2D canvas."""
    def __init__(self, pattern, canvas):
        if not isinstance(canvas, np.ndarray) or not isinstance(pattern, np.ndarray):
            raise TypeError("Canvas and pattern must be NumPy arrays.")
        self.pattern = pattern
        self.canvas = canvas
        self.p_h, self.p_w = pattern.shape
        self.c_h, self.c_w = canvas.shape
        self.pos = {'y': -1, 'x': -1} # Not placed yet
        self.is_placed = False

    def place_at(self, y, x):
        """Places the entity's pattern at a specific location on the canvas."""
        # Erase previous location if it exists
        if self.is_placed:
            self._erase()
            
        self.canvas[y : y + self.p_h, x : x + self.p_w] = self.pattern
        self.pos = {'y': y, 'x': x}
        self.is_placed = True
        print(f"图案已放置在 ({y}, {x})。")

    def place_at_random(self):
        """Finds a valid random spot and places the entity there."""
        max_y = self.c_h - self.p_h
        max_x = self.c_w - self.p_w
        if max_y < 0 or max_x < 0:
            raise ValueError("Pattern is larger than the canvas.")
        self.place_at(random.randint(0, max_y), random.randint(0, max_x))

    def _erase(self):
        """Erases the pattern from its current position."""
        if self.is_placed:
            y, x = self.pos['y'], self.pos['x']
            self.canvas[y : y + self.p_h, x : x + self.p_w] = 0

    def move(self, direction, steps):
        """Moves the entity by n steps in a given direction."""
        if not self.is_placed:
            print("错误: 无法移动, 图案尚未被放置。")
            return
            
        y, x = self.pos['y'], self.pos['x']
        target_y, target_x = y, x

        moves = {'up': (-steps, 0), 'down': (steps, 0), 'left': (0, -steps), 'right': (0, steps)}
        if direction not in moves:
            print(f"错误: 无效的方向 '{direction}'。")
            return
        
        dy, dx = moves[direction]
        target_y, target_x = y + dy, x + dx

        # Boundary check
        if not (0 <= target_y <= self.c_h - self.p_h and 0 <= target_x <= self.c_w - self.p_w):
            print(f"移动无效: 从 ({y}, {x}) 向 {direction} 移动 {steps} 格会导致越界。")
            return
        
        # If valid, perform the move
        self._erase()
        self.place_at(target_y, target_x)
        print(f"成功: 图案已移动到 ({target_y}, {target_x})。")

# --- Main Demonstration ---
if __name__ == "__main__":
    # 1. Initialization
    main_canvas = np.zeros((10, 20), dtype=int)
    random_pattern = np.random.randint(1, 10, size=(3, 3))
    
    # 2. Create a reusable entity
    entity = MovableEntity(pattern=random_pattern, canvas=main_canvas)
    
    print("--- 初始状态 (Modular Style) ---")
    print("生成的 3x3 图案:\n", entity.pattern)
    entity.place_at_random()
    print("初始画布:\n", main_canvas)

    # 3. Execute moves using the entity's methods
    print("\n--- 开始移动图案 ---")
    
    def perform_move(direction, steps):
        print(f"\n>>> 操作: 向{direction}移动 {steps} 格")
        entity.move(direction, steps)
        print(main_canvas)

    perform_move('right', 5)
    perform_move('down', 3)
    perform_move('left', 10)
    
    print("\n>>> 操作: 尝试向上移动 10 格 (预期失败)")
    entity.move('up', 10)
    print("由于移动无效，画布保持不变。")
    print(f"图案当前位置仍然是: {entity.pos}")

    perform_move('up', 2)
    print(f"\n图案最终位置: {entity.pos}")