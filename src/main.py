import pygame
from maze import Maze

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Create the Maze
maze = Maze(15, 15)
maze.choose_start()
maze.choose_end()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")
    maze.draw_maze(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

