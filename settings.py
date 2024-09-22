import numpy as np
import random


def generate_maze(width, height):
    maze = np.ones((height, width), dtype=int)
    maze[1, 1: height - 1] = 0
    maze[height - 2, 1: height - 1] = 0
    maze[1: width - 1, 1] = 0
    maze[1: width - 1, width - 2] = 0
    stack = []

    start_x, start_y = random.randrange(1, width - 1), random.randrange(1, height - 1)
    maze[start_y, start_x] = 0
    stack.append((start_x, start_y))

    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    while stack:
        x, y = stack[-1]
        neighbors = []
        # neighbors_in_case_deadend = []

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < width - 1 and 0 < ny < height - 1 and maze[ny, nx] == 1:
                neighbors.append((nx, ny))
        # for dx, dy in directions:
        #     nx, ny = x + dx, y + dy
        #     if 0 < nx < width - 1 and 0 < ny < height - 1 and maze[(y + ny) // 2, (x + nx) // 2] == 1:
        #         neighbors_in_case_deadend.append((nx, ny))
        # if not neighbors:
        #     neighbors = neighbors_in_case_deadend

        if neighbors:
            nx, ny = neighbors[np.random.randint(0, len(neighbors))]
            maze[(y + ny) // 2, (x + nx) // 2] = 0
            maze[ny, nx] = 0
            stack.append((nx, ny))
        else:
            # if neighbors_in_case_deadend:
            #     nx, ny = neighbors_in_case_deadend[np.random.randint(0, len(neighbors_in_case_deadend))]
            #     maze[(y + ny) // 2, (x + nx) // 2] = 0
            #     maze[ny, nx] = 0
            stack.pop()

    return maze


MAP = [
    ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
    ['1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1'],
    ['1', 'B', '1', '1', ' ', '1', '1', '1', ' ', '1', ' ', '1', '1', '1', ' ', '1', '1', 'B', '1'],
    ['1', ' ', ' ', ' ', ' ', '1', ' ', ' ', ' ', '1', ' ', ' ', ' ', '1', ' ', ' ', ' ', ' ', '1'],
    ['1', '1', ' ', '1', ' ', '1', ' ', '1', ' ', '1', ' ', '1', ' ', '1', ' ', '1', ' ', '1', '1'],
    ['1', ' ', ' ', '1', ' ', ' ', ' ', '1', ' ', ' ', ' ', '1', ' ', ' ', ' ', '1', ' ', ' ', '1'],
    ['1', ' ', '1', '1', '1', '1', ' ', '1', '1', '1', '1', '1', ' ', '1', '1', '1', '1', ' ', '1'],
    ['1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'r', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1'],
    ['1', '1', ' ', '1', '1', '1', ' ', '1', '1', '-', '1', '1', ' ', '1', '1', '1', ' ', '1', '1'],
    [' ', ' ', ' ', ' ', ' ', '1', ' ', '1', 's', 'p', 'o', '1', ' ', '1', ' ', ' ', ' ', ' ', ' '],
    ['1', '1', ' ', '1', ' ', '1', ' ', '1', '1', '1', '1', '1', ' ', '1', ' ', '1', ' ', '1', '1'],
    ['1', ' ', ' ', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', ' ', ' ', '1'],
    ['1', ' ', '1', '1', '1', '1', ' ', '1', '1', '1', '1', '1', ' ', '1', '1', '1', '1', ' ', '1'],
    ['1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1'],
    ['1', '1', '1', ' ', '1', '1', '1', ' ', '1', '1', '1', ' ', '1', '1', '1', ' ', '1', '1', '1'],
    ['1', ' ', ' ', ' ', '1', ' ', ' ', ' ', ' ', 'P', ' ', ' ', ' ', ' ', '1', ' ', ' ', ' ', '1'],
    ['1', 'B', '1', ' ', '1', ' ', '1', ' ', '1', '1', '1', ' ', '1', ' ', '1', ' ', '1', 'B', '1'],
    ['1', ' ', '1', ' ', ' ', ' ', '1', ' ', ' ', ' ', ' ', ' ', '1', ' ', ' ', ' ', '1', ' ', '1'],
    ['1', ' ', '1', '1', '1', ' ', '1', '1', '1', ' ', '1', '1', '1', ' ', '1', '1', '1', ' ', '1'],
    ['1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1'],
    ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']
]

# # Random maze generation
# maze = generate_maze(20, 20)
# MAP = [['1' if j == 1 else ' ' for j in i] for i in maze.tolist()]
# MAP[1][1] = 'r'
# MAP[1][1] = 's'
# MAP[1][18] = 'p'
# MAP[18][1] = 'o'
# MAP[18][18] = 'P'

MAP_BINARY = [list(map(lambda x: 1 if x != '1' else 0, row)) for row in MAP]
BOARD_RATIO = (len(MAP[0]), len(MAP))
CHAR_SIZE = 32
WIDTH, HEIGHT = (BOARD_RATIO[0] * CHAR_SIZE, BOARD_RATIO[1] * CHAR_SIZE)
NAV_HEIGHT = 64
PLAYER_SPEED = CHAR_SIZE // 4
GHOST_SPEED = 8
