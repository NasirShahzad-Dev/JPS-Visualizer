import pygame
import sys

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 30
CELL_SIZE = WIDTH // GRID_SIZE
WHITE, BLACK, RED, BLUE, GREEN, YELLOW = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)

# Pygame Initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("JPS Visual Implementation")
clock = pygame.time.Clock()

# Grid Initialization
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Start/Goal Points
start_point = None
end_point = None
path = []

# Functions to Draw the Grid
def draw_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[y][x] == 1:  # Wall
                pygame.draw.rect(screen, BLACK, rect)
            elif grid[y][x] == 2:  # Path
                pygame.draw.rect(screen, GREEN, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)  # Draw cell borders

    if start_point:
        pygame.draw.rect(screen, BLUE, (start_point[0] * CELL_SIZE, start_point[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    if end_point:
        pygame.draw.rect(screen, RED, (end_point[0] * CELL_SIZE, end_point[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Reset the Path
def clear_path():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] == 2:
                grid[y][x] = 0

# Improved Jump Point Search with Diagonal Movement
def jump_point_search(start, end):
    clear_path()
    queue = [start]
    visited = set()
    came_from = {}  # To track the path

    while queue:
        x, y = queue.pop(0)
        visited.add((x, y))

        if (x, y) == end:
            # Goal is reached
            reconstruct_path(came_from, end)
            return True

        # Explore neighbors (8 directions including diagonals)
        for dx, dy in [
            (0, 1), (1, 0), (0, -1), (-1, 0),  # Cardinal directions
            (1, 1), (-1, -1), (-1, 1), (1, -1)  # Diagonal directions
        ]:
            nx, ny = x + dx, y + dy
            # Check bounds and obstacles
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and (nx, ny) not in visited and grid[ny][nx] != 1:
                # For diagonal moves, ensure no blocking obstacles
                if dx != 0 and dy != 0:  # Diagonal move
                    if grid[y][nx] == 1 or grid[ny][x] == 1:
                        continue  # Skip diagonal if blocked
                queue.append((nx, ny))
                visited.add((nx, ny))
                came_from[(nx, ny)] = (x, y)

    # If we exit the loop, no path was found
    print("No path found!")  # Console notification
    return False

# Reconstruct the Path
def reconstruct_path(came_from, current):
    while current in came_from:
        x, y = current
        grid[y][x] = 2
        path.append(current)
        current = came_from[current]

# Event Handling
def handle_events():
    global start_point, end_point
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
            if pygame.key.get_pressed()[pygame.K_s]:  # Place Start Point
                start_point = (grid_x, grid_y)
            elif pygame.key.get_pressed()[pygame.K_g]:  # Place End Point
                end_point = (grid_x, grid_y)
            elif event.button == 1:  # Left Click to Add Wall
                grid[grid_y][grid_x] = 1
            elif event.button == 3:  # Right Click to Remove Wall
                grid[grid_y][grid_x] = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and start_point and end_point:
                clear_path()
                path_found = jump_point_search(start_point, end_point)
                if not path_found:
                    print("Unable to find a valid path to the goal!")

# Main Loop
while True:
    screen.fill(WHITE)
    handle_events()
    draw_grid()
    pygame.display.flip()
    clock.tick(30)
