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
maze.random_walk(maze.grille[randint(0, maze.largeur - 1 )][randint(0, maze.hauteur - 1 )])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")
    maze.draw_maze(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
