# sym_config_driven.py
import numpy as np
import random

# --- Centralized Configuration ---
CONFIG = {
    'canvas_height': 11,
    'canvas_width': 20,
    'axis_row_index': 5,        # The row index for the line of symmetry
    'axis_color': 1,
    'background_color': 0,
    'max_pattern_height': 3,
    'max_pattern_width': 3,
    'num_symmetric_pairs': 4,   # Number of symmetric pairs to generate
    'max_placement_attempts': 100, # Prevents infinite loops
}

class SymmetryManager:
    """Manages the creation of a symmetrically patterned canvas based on a config."""
    def __init__(self, config):
        self.config = config
        self.canvas = np.full(
            (config['canvas_height'], config['canvas_width']),
            config['background_color'],
            dtype=int
        )
        # Draw the axis of symmetry
        self.canvas[config['axis_row_index'], :] = config['axis_color']
        
    def _generate_random_pattern(self):
        """Generates a random pattern according to config."""
        p_h = random.randint(1, self.config['max_pattern_height'])
        p_w = random.randint(1, self.config['max_pattern_width'])
        # Colors start at 2 to avoid conflict with background and axis
        return np.random.randint(2, 10, size=(p_h, p_w))

    def _is_area_free(self, y, x, h, w):
        """Checks if a rectangular area on the canvas is free."""
        if not (0 <= y and y + h <= self.config['canvas_height'] and 
                0 <= x and x + w <= self.config['canvas_width']):
            return False
        return np.all(self.canvas[y:y+h, x:x+w] == self.config['background_color'])

    def place_symmetric_pair(self):
        """Generates one pattern and attempts to place it and its reflection."""
        pattern = self._generate_random_pattern()
        p_h, p_w = pattern.shape
        reflected_pattern = np.flipud(pattern)
        axis_y = self.config['axis_row_index']

        for _ in range(self.config['max_placement_attempts']):
            # Choose a random position above the axis
            max_y = axis_y - p_h
            if max_y < 0: continue # Pattern too tall to fit
            
            y1 = random.randint(0, max_y)
            x = random.randint(0, self.config['canvas_width'] - p_w)
            
            # Calculate the reflected position
            y2 = axis_y + (axis_y - (y1 + p_h) + 1)
            
            # Check if both original and reflected locations are free
            if self._is_area_free(y1, x, p_h, p_w) and self._is_area_free(y2, x, p_h, p_w):
                self.canvas[y1:y1+p_h, x:x+p_w] = pattern
                self.canvas[y2:y2+p_h, x:x+p_w] = reflected_pattern
                print(f"  成功: 放置了一对 {p_h}x{p_w} 的对称图案。")
                return True
        
        print(f"  警告: 未能为 {p_h}x{p_w} 的图案找到对称位置。")
        return False

    def populate(self):
        """Populates the canvas with the configured number of symmetric pairs."""
        print(f"--- 开始生成 {self.config['num_symmetric_pairs']} 组对称图案 ---")
        for i in range(self.config['num_symmetric_pairs']):
            print(f"--> 正在尝试第 {i + 1} 组:")
            self.place_symmetric_pair()
        return self.canvas

# --- Main Execution ---
if __name__ == "__main__":
    # 1. Initialize the manager with the global configuration
    manager = SymmetryManager(CONFIG)
    
    print("--- 初始画布 (Config-Driven Style) ---")
    # The canvas with the axis is already created upon initialization
    print(manager.canvas)
    
    # 2. Run the population process
    final_canvas = manager.populate()
    
    print("\n--- 最终完成的画布 ---")
    print(final_canvas)