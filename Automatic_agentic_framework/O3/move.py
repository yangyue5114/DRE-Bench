# move_factory_closure.py
import numpy as np
import random
from typing import Callable

def pattern_factory(canvas: np.ndarray, pattern: np.ndarray) -> Callable:
    """A factory that returns a move function with an encapsulated state."""
    
    # State encapsulated within the closure's scope
    _pos = {'y': -1, 'x': -1}
    p_h, p_w = pattern.shape
    c_h, c_w = canvas.shape

    def mover(action: str, **kwargs):
        """The returned function that performs actions."""
        nonlocal _pos # Modify the state from the parent scope
        
        if action == "place":
            y, x = kwargs.get('y'), kwargs.get('x')
            if _pos['y'] != -1: # Erase old position
                canvas[_pos['y'] : _pos['y'] + p_h, _pos['x'] : _pos['x'] + p_w] = 0
            canvas[y : y + p_h, x : x + p_w] = pattern
            _pos = {'y': y, 'x': x}
            print(f"图案放置在: {_pos}")
            return

        # --- Handle movement ---
        if _pos['y'] == -1: return print("错误: 图案未放置。")
        
        direction, steps = kwargs['direction'], kwargs['steps']
        y, x = _pos['y'], _pos['x']
        dy, dx = {'up': (-steps, 0), 'down': (steps, 0), 'left': (0, -steps), 'right': (0, steps)}.get(direction, (0,0))
        
        ny, nx = y + dy, x + dx # New position
        
        if not (0 <= ny <= c_h - p_h and 0 <= nx <= c_w - p_w):
            print(f"移动无效: 从 {_pos} 向 {direction} 移动 {steps} 格会越界。")
        else:
            mover("place", y=ny, x=nx)
            print(f"成功移动到: {_pos}")
            
    return mover

# --- Main Execution ---
if __name__ == "__main__":
    canvas = np.zeros((10, 20), dtype=int)
    patt = np.random.randint(1, 10, size=(3, 3))
    
    # Create the "mover" instance
    move_my_pattern = pattern_factory(canvas, patt)
    
    print("--- 初始状态 (Factory/Closure Style) ---")
    print("图案:\n", patt)
    move_my_pattern("place", y=random.randint(0, 7), x=random.randint(0, 17))
    print("画布:\n", canvas)

    # Execute moves
    print("\n--- 开始移动 ---")
    move_my_pattern("move", direction='right', steps=5)
    move_my_pattern("move", direction='down', steps=3)
    move_my_pattern("move", direction='left', steps=10)
    move_my_pattern("move", direction='up', steps=10) # Expected fail
    move_my_pattern("move", direction='up', steps=2)
    print("\n最终画布:\n", canvas)