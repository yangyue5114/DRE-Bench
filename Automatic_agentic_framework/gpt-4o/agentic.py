import random
from itertools import permutations
from typing import List, Tuple, Optional
import numpy as np

SIZE = 11

Coordinate = Tuple[int, int]

def manhattan_distance(p1: Coordinate, p2: Coordinate) -> int:
    """Calculate the Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def setup_grid_with_points(num_waypoints: int) -> Tuple[Optional[np.ndarray], Optional[Coordinate], Optional[List[Coordinate]]]:
    """
    Create an 11x11 grid with a start point (value 2) and specified number of waypoints (value 1).
    
    Args:
        num_waypoints: Number of waypoint positions to place.

    Returns:
        grid: Numpy array with placed points.
        start_coord: Tuple with the start point coordinate.
        waypoints: List of coordinates for waypoints.
    """
    total_points = num_waypoints + 1
    if total_points > SIZE * SIZE:
        print(f"Error: total points ({total_points}) exceed grid capacity ({SIZE * SIZE}).")
        return None, None, None

    grid = np.zeros((SIZE, SIZE), dtype=int)
    possible_coords = [(y, x) for y in range(SIZE) for x in range(SIZE)]
    random.shuffle(possible_coords)

    start_coord = possible_coords.pop()
    grid[start_coord] = 2

    waypoints = [possible_coords.pop() for _ in range(num_waypoints)]
    for point in waypoints:
        grid[point] = 1

    return grid, start_coord, waypoints

def total_path_distance(path: List[Coordinate]) -> int:
    """Calculate the total Manhattan distance for a path."""
    return sum(manhattan_distance(path[i], path[i + 1]) for i in range(len(path) - 1))

def find_shortest_path(start: Coordinate, waypoints: List[Coordinate]) -> Tuple[List[Coordinate], int]:
    """
    Find the permutation of waypoints that results in the shortest path from the start.

    Args:
        start: Starting coordinate.
        waypoints: List of waypoint coordinates.

    Returns:
        shortest_path: List of coordinates representing the optimal path.
        shortest_distance: Total Manhattan distance of the optimal path.
    """
    shortest_distance = float('inf')
    shortest_path = []

    for perm in permutations(waypoints):
        current_path = [start] + list(perm)
        distance = total_path_distance(current_path)

        if distance < shortest_distance:
            shortest_distance = distance
            shortest_path = current_path

    return shortest_path, shortest_distance

def print_grid(grid: np.ndarray) -> None:
    """Print the grid with point values."""
    print("\nGrid Layout:")
    for row in grid:
        print(" ".join(map(str, row)))
