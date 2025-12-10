import pygame
from maze import Maze

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))

clock = pygame.time.Clock()
running = True
screen.fill("black")

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    maze = Maze(15, 15)
    maze.draw_maze(screen)


    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()

