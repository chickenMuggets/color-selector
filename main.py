import pygame

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)  # Define the color orange

# Change if you want fullscreen
fullscreen = False

# Function to get user input for grid size
def get_grid_size():
    while True:
        try:
            size = int(input("Enter the grid size (e.g., 5 for a 5x5 grid): "))
            if size > 0:
                return size
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

# Get grid size from user
GRID_SIZE = get_grid_size()

# Create the window
if fullscreen:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((500, 500))

# Function to draw the grid
def draw_grid(selected_cells, color_mapping, cell_size):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            if (row, col) in selected_cells:
                cell_color = color_mapping.get((row, col), RED)  # Default to red if no color is set
                pygame.draw.rect(screen, cell_color, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

# Main loop
running = True
selected_cells = set()
color_mapping = {}  # To store colors of selected cells
dragging = False
dragged_cells = set()  # Keep track of cells already toggled during drag
current_color = RED  # Default color

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            dragging = True
            x, y = event.pos
            col = x // CELL_SIZE
            row = y // CELL_SIZE
            if (row, col) in selected_cells:
                selected_cells.remove((row, col))
                color_mapping.pop((row, col), None)  # Remove color when deselected
            else:
                selected_cells.add((row, col))
                color_mapping[(row, col)] = current_color  # Use the currently selected color
            dragged_cells.add((row, col))  # Mark this cell as toggled
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            dragged_cells.clear()  # Clear the set when drag ends
        elif event.type == pygame.MOUSEMOTION and dragging:
            x, y = event.pos
            col = x // CELL_SIZE
            row = y // CELL_SIZE
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                if (row, col) not in dragged_cells:  # Only toggle if not already toggled
                    if (row, col) in selected_cells:
                        selected_cells.remove((row, col))
                        color_mapping.pop((row, col), None)  # Remove color when deselected
                    else:
                        selected_cells.add((row, col))
                        color_mapping[(row, col)] = current_color  # Use the currently selected color
                    dragged_cells.add((row, col))  # Mark this cell as toggled

        # Check for key presses to change the current color
        keys = pygame.key.get_pressed()
        if keys[pygame.K_b]:  # Set current color to black
            current_color = BLACK
        elif keys[pygame.K_g]:  # Set current color to green
            current_color = GREEN
        elif keys[pygame.K_l]:  # Set current color to blue
            current_color = BLUE
        elif keys[pygame.K_r]:  # Set current color to red
            current_color = RED
        elif keys[pygame.K_o]:  # Set current color to orange
            current_color = ORANGE

    # Update CELL_SIZE based on current screen size
    screen_width, screen_height = screen.get_size()
    CELL_SIZE = min(screen_width, screen_height) // GRID_SIZE

    screen.fill(BLACK)
    draw_grid(selected_cells, color_mapping, CELL_SIZE)
    pygame.display.flip()

    if keys[pygame.K_p]:
        # Function to print the grid in the desired format
        display = 'display = Image(\n'
        for row in range(GRID_SIZE):
            line = ':'
            for col in range(GRID_SIZE):
                if (row, col) in selected_cells:
                    line += '9'
                else:
                    line += '0'
            display += f'    "{line}"\n'
        display += ')'
        print(display)

pygame.quit()

# Function to print the grid in the desired format
def print_grid(selected_cells):
    display = 'display = Image(\n'
    for row in range(GRID_SIZE):
        line = ':'
        for col in range(GRID_SIZE):
            if (row, col) in selected_cells:
                line += '9'
            else:
                line += '0'
        display += f'    "{line}"\n'
    display += ')'
    print(display)

# Print the grid when the program ends
print_grid(selected_cells)
