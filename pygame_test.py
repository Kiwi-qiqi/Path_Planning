import os
import pygame

# Define color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (64, 64, 64)
BLUE = (0, 0, 255)

# Set the size of each grid cell in pixels
cell_size = 25

# Set the dimensions of the screen
screen_width = 1000
screen_height = 800

# Set the dimensions of the grid
grid_width = screen_width // cell_size
grid_height = screen_height // cell_size

# Initialize Pygame
pygame.init()

# Set the screen size
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# Set the background color to white
background_color = WHITE

# Set the grid color to black
grid_color = BLACK

# Initialize the start and end cells
start_point = (5, 5)
end_point = (grid_width - 6, grid_height - 6)

start_color = GREEN
end_color = RED

# Initialize variables for dragging the start and end cells
dragging_start = False
dragging_end = False

# Update the display
pygame.display.update()

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen_width = event.w
            screen_height = event.h
            grid_width = screen_width // cell_size
            grid_height = screen_height // cell_size
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            screen.fill(background_color)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if left mouse button was pressed
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check if the mouse is on the start point
                if (mouse_pos[0] >= start_point[0] * cell_size and mouse_pos[0] < (start_point[0] + 1) * cell_size
                    and mouse_pos[1] >= start_point[1] * cell_size and mouse_pos[1] < (start_point[1] + 1) * cell_size):
                    # Start dragging the start point
                    dragging_start = True
                
                # Check if the mouse is on the end point
                elif (mouse_pos[0] >= end_point[0] * cell_size and mouse_pos[0] < (end_point[0] + 1) * cell_size
                      and mouse_pos[1] >= end_point[1] * cell_size and mouse_pos[1] < (end_point[1] + 1) * cell_size):
                    # Start dragging the end point
                    dragging_end = True


        elif event.type == pygame.MOUSEBUTTONUP:
            # Check if left mouse button was released
            if event.button == 1:
                # Stop dragging the start point
                dragging_start = False
                
                # Stop dragging the end point
                dragging_end = False


        elif event.type == pygame.MOUSEMOTION:
            # Check if the mouse is being dragged
            if dragging_start:
                # Get the position of the mouse
                mouse_pos = pygame.mouse.get_pos()
                
                # Update the position of the start point
                start_point = (mouse_pos[0] // cell_size, mouse_pos[1] // cell_size)
            
            elif dragging_end:
                # Get the position of the mouse
                mouse_pos = pygame.mouse.get_pos()
                
                # Update the position of the end point
                end_point = (mouse_pos[0] // cell_size, mouse_pos[1] // cell_size)


        # Draw the grid
        for i in range(grid_width):
            for j in range(grid_height):
                rect = pygame.Rect(i * cell_size, j * cell_size, cell_size - 1, cell_size - 1)
                if i == 0 or j == 0 or i == grid_width - 1 or j == grid_height - 1:
                    pygame.draw.rect(screen, GRAY, rect, 0)

                elif (i, j) == start_point:
                    start_rect = pygame.Rect(start_point[0] * cell_size, start_point[1] * cell_size, cell_size - 1, cell_size - 1)
                    pygame.draw.rect(screen, start_color, start_rect, 0)

                elif (i, j) == end_point:
                    start_rect = pygame.Rect(end_point[0] * cell_size, end_point[1] * cell_size, cell_size - 1, cell_size - 1)
                    pygame.draw.rect(screen, end_color, start_rect, 0)
                else:
                    pygame.draw.rect(screen, (220, 220, 220), rect, 0)


        # Update the display
        pygame.display.update()

# Quit Pygame
pygame.quit()