from settings import *
import pygame
from numba.core import types
from numba.typed import Dict
from numba import int32

_ = False
matrix_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, 2, _, _, 2, 4, 3, _, _, _, _, _, 3, 2, 1, 4, _, _, _, _, _, 1],
    [4, _, _, 2, _, _, _, _, _, 2, 2, 2, _, _, _, _, _, _, _, 4, _, 1, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, 3, 4, _, 4, _, _, _, _, _, _, 1],
    [1, _, _, 2, _, _, _, _, _, 2, 2, 2, _, _, _, _, _, _, _, 4, _, 1, _, 1],
    [1, _, _, 2, _, _, 1, _, 4, _, _, _, _, _, 3, 2, 1, 4, _, _, _, _, _, 1],
    [1, 3, 3, 4, 1, 1, 2, _, _, 4, 4, 4, 4, 4, _, _, _, _, 1, 1, _, 2, 3, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 2, _, _, _, 4, 1],
    [1, _, 7, 7, 7, 8, 8, 8, 7, 7, 8, 8, 7, 7, 7, _, _, 1, _, _, _, _, _, 1],
    [1, _, 7, _, _, _, _, _, _, _, _, _, _, _, 8, _, _, 2, _, _, _, _, _, 1],
    [1, _, 7, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 4, _, _, _, 3, 1],
    [1, _, 7, _, _, _, _, _, _, _, _, _, _, _, 8, _, _, 2, _, _, _, _, _, 1],
    [1, _, 7, 7, 7, 8, 8, 7, 7, 7, 8, 8, 7, 7, 7, _, _, 2, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, _, _, 3, 1],
    [1, _, 1, _, _, _, _, _, 2, _, _, _, _, _, 3, _, _, _, _, _, _, _, 4, 1],
    [1, 1, 1, 4, 3, 3, 4, 1, 1, 1, 1, 1, 3, 4, 3, 1, 1, 1, 1, 4, 4, 1, 1, 1]
]

WORLD_WIDTH = len(matrix_map[0]) * TILE
WORLD_HEIGHT = len(matrix_map) * TILE
world_map = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
mini_map = set()
collision_walls = []
for j, row in enumerate(matrix_map):
    for i, char in enumerate(row):
        if char:
            mini_map.add((i * MAP_TILE, j * MAP_TILE))
            collision_walls.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
            if char == 1:
                world_map[(i * TILE, j * TILE)] = 1
            elif char == 2:
                world_map[(i * TILE, j * TILE)] = 2
            elif char == 3:
                world_map[(i * TILE, j * TILE)] = 3
            elif char == 4:
                world_map[(i * TILE, j * TILE)] = 4
            elif char == 5:
                world_map[(i * TILE, j * TILE)] = 5
            elif char == 6:
                world_map[(i * TILE, j * TILE)] = 6
            elif char == 7:
                world_map[(i * TILE, j * TILE)] = 7
            elif char == 8:
                world_map[(i * TILE, j * TILE)] = 8