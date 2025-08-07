import random
from typing import Literal
import numpy as np

Direction = Literal['up', 'down', 'left', 'right']

class MovableEntity:
    """A class representing a movable 2D pattern on a canvas."""

    def __init__(self, pattern: np.ndarray, canvas: np.ndarray):
        if not (isinstance(pattern, np.ndarray) and isinstance(canvas, np.ndarray)):
            raise TypeError("Canvas and pattern must be NumPy arrays.")

        self.pattern = pattern
        self.canvas = canvas
        self.p_h, self.p_w = pattern.shape
        self.c_h, self.c_w = canvas.shape
        self.pos = {'y': -1, 'x': -1}  # Initial position (not placed)
        self.is_placed = False

    def place_at(self, y: int, x: int) -> None:
        """Place the pattern at a given (y, x) position on the canvas."""
        if self.is_placed:
            self._erase()

        self.canvas[y:y + self.p_h, x:x + self.p_w] = self.pattern
        self.pos.update({'y': y, 'x': x})
        self.is_placed = True
        print(f"图案已放置在 ({y}, {x})。")

    def place_at_random(self) -> None:
        """Place the pattern at a valid random position within canvas bounds."""
        max_y, max_x = self.c_h - self.p_h, self.c_w - self.p_w
        if max_y < 0 or max_x < 0:
            raise ValueError("Pattern is larger than the canvas.")

        self.place_at(random.randint(0, max_y), random.randint(0, max_x))

    def _erase(self) -> None:
        """Erase the pattern from the canvas."""
        y, x = self.pos['y'], self.pos['x']
        self.canvas[y:y + self.p_h, x:x + self.p_w] = 0

    def move(self, direction: Direction, steps: int) -> None:
        """Move the pattern in a specified direction by given steps."""
        if not self.is_placed:
            print("错误: 无法移动, 图案尚未被放置。")
            return

        moves = {
            'up': (-steps, 0),
            'down': (steps, 0),
            'left': (0, -steps),
            'right': (0, steps)
        }

        if direction not in moves:
            print(f"错误: 无效的方向 '{direction}'。")
            return

        dy, dx = moves[direction]
        target_y = self.pos['y'] + dy
        target_x = self.pos['x'] + dx

        if not (0 <= target_y <= self.c_h - self.p_h and 0 <= target_x <= self.c_w - self.p_w):
            print(f"移动无效: 从 ({self.pos['y']}, {self.pos['x']}) 向 {direction} 移动 {steps} 格会导致越界。")
            return

        self._erase()
        self.place_at(target_y, target_x)
        print(f"成功: 图案已移动到 ({target_y}, {target_x})。")


if __name__ == "__main__":
    canvas = np.zeros((10, 20), dtype=int)
    pattern = np.random.randint(1, 10, size=(3, 3))
    entity = MovableEntity(pattern, canvas)

    print("--- 初始状态 ---")
    print("生成图案:\n", pattern)
    entity.place_at_random()
    print("画布:\n", canvas)

    def perform_move(direction: Direction, steps: int):
        print(f"\n>>> 向{direction}移动 {steps} 格")
        entity.move(direction, steps)
        print(canvas)

    perform_move('right', 5)
    perform_move('down', 3)
    perform_move('left', 10)

    print("\n>>> 尝试向上移动 10 格 (预期失败)")
    entity.move('up', 10)
    print("当前位置:", entity.pos)

    perform_move('up', 2)
    print("最终位置:", entity.pos)
