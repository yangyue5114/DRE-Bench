import numpy as np
import random
from itertools import permutations
from typing import List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Config:
    """Configuration for the pathfinding system."""
    GRID_SIZE: int = 11
    START_MARKER: int = 2
    WAYPOINT_MARKER: int = 1
    PATH_MARKER: int = 5
    EMPTY_SPACE: int = 0
    MAX_WAYPOINTS_WARNING: int = 10

class PathFinder:
    """Handles pathfinding operations on a grid."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
    
    def manhattan_distance(self, p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
        """Calculates Manhattan distance between two points."""
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    def setup_grid_with_points(self, num_waypoints: int) -> Tuple[Optional[np.ndarray], 
                                                                 Optional[Tuple[int, int]], 
                                                                 Optional[List[Tuple[int, int]]]]:
        """
        Creates grid with start point and waypoints.
        
        Args:
            num_waypoints: Number of waypoints to place
            
        Returns:
            Tuple of (grid, start_coord, waypoints_list) or (None, None, None) if invalid
        """
        if not self._validate_waypoint_count(num_waypoints):
            return None, None, None
        
        grid = np.zeros((self.config.GRID_SIZE, self.config.GRID_SIZE), dtype=int)
        available_coords = self._get_all_coordinates()
        
        # Place start point
        start_coord = available_coords.pop()
        grid[start_coord] = self.config.START_MARKER
        
        # Place waypoints
        waypoints = []
        for _ in range(num_waypoints):
            waypoint_coord = available_coords.pop()
            grid[waypoint_coord] = self.config.WAYPOINT_MARKER
            waypoints.append(waypoint_coord)
        
        return grid, start_coord, waypoints
    
    def _validate_waypoint_count(self, num_waypoints: int) -> bool:
        """Validates if the requested number of waypoints can fit in the grid."""
        total_points = num_waypoints + 1  # waypoints + start point
        max_capacity = self.config.GRID_SIZE * self.config.GRID_SIZE
        
        if total_points > max_capacity:
            print(f"Error: Requested points ({total_points}) exceed grid capacity ({max_capacity}).")
            return False
        return True
    
    def _get_all_coordinates(self) -> List[Tuple[int, int]]:
        """Returns shuffled list of all grid coordinates."""
        coords = [(y, x) for y in range(self.config.GRID_SIZE) 
                          for x in range(self.config.GRID_SIZE)]
        random.shuffle(coords)
        return coords
    
    def find_optimal_path_order(self, start_coord: Tuple[int, int], 
                               waypoints: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Finds the shortest path order using brute force permutation.
        
        Args:
            start_coord: Starting coordinate
            waypoints: List of waypoint coordinates
            
        Returns:
            Optimal path order starting with start_coord
        """
        if not waypoints:
            return [start_coord]
        
        if len(waypoints) > self.config.MAX_WAYPOINTS_WARNING:
            print(f"Warning: {len(waypoints)} waypoints may cause slow computation.")
        
        min_distance = float('inf')
        best_order = None
        
        # Try all permutations of waypoints
        for permutation in permutations(waypoints):
            total_distance = self._calculate_path_distance(start_coord, permutation)
            
            if total_distance < min_distance:
                min_distance = total_distance
                best_order = permutation
        
        return [start_coord] + list(best_order)
    
    def _calculate_path_distance(self, start: Tuple[int, int], 
                                waypoint_order: Tuple[Tuple[int, int], ...]) -> int:
        """Calculates total Manhattan distance for a given path order."""
        total_distance = 0
        current_point = start
        
        for waypoint in waypoint_order:
            total_distance += self.manhattan_distance(current_point, waypoint)
            current_point = waypoint
        
        return total_distance
    
    def draw_path_on_grid(self, grid: np.ndarray, 
                         path_order: List[Tuple[int, int]]) -> np.ndarray:
        """
        Draws the optimal path on the grid using Manhattan routing.
        
        Args:
            grid: The grid to draw on (will be modified)
            path_order: Ordered list of coordinates to connect
            
        Returns:
            Modified grid with path drawn
        """
        for i in range(len(path_order) - 1):
            self._draw_manhattan_segment(grid, path_order[i], path_order[i + 1])
        
        return grid
    
    def _draw_manhattan_segment(self, grid: np.ndarray, 
                               start: Tuple[int, int], end: Tuple[int, int]):
        """Draws a Manhattan path segment between two points."""
        y1, x1 = start
        y2, x2 = end
        
        # Draw horizontal line first
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if grid[y1, x] == self.config.EMPTY_SPACE:
                grid[y1, x] = self.config.PATH_MARKER
        
        # Then draw vertical line
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if grid[y, x2] == self.config.EMPTY_SPACE:
                grid[y, x2] = self.config.PATH_MARKER

def main():
    """Main demonstration of the pathfinding algorithm."""
    NUM_WAYPOINTS = 8
    
    pathfinder = PathFinder()
    
    # Validate waypoint count
    if not 1 <= NUM_WAYPOINTS <= 10:
        print("Warning: For optimal performance, keep waypoints between 1-10.")
    
    print("=== Pathfinding Algorithm ===\n")
    
    # Create grid with points
    grid, start_point, waypoints_list = pathfinder.setup_grid_with_points(NUM_WAYPOINTS)
    
    if grid is None:
        print("Failed to create grid. Exiting.")
        return
    
    print("--- Initial Grid ---")
    print(f"Start point (2) at: {start_point}")
    print(f"Waypoints (1) at: {waypoints_list}")
    print(grid)
    
    # Find optimal path
    print("\n--- Computing shortest path order... ---")
    optimal_path = pathfinder.find_optimal_path_order(start_point, waypoints_list)
    print(f"Optimal path order: {optimal_path}")
    
    # Draw path on grid
    final_grid = pathfinder.draw_path_on_grid(grid.copy(), optimal_path)
    
    print("\n--- Final Path Visualization ---")
    print("Path marked with 5, connecting start (2) and waypoints (1):")
    print(final_grid)

if __name__ == "__main__":
    main()