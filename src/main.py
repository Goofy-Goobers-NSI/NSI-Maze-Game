import pygame
from maze import Maze
from player import Player

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Create the Maze
maze = Maze(15, 15)
maze.choose_start()
maze.choose_end()
maze.generate_maze()
player = Player(maze.start.x,maze.start.y)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            player.move_player(0)
            print(player.x,player.y)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            player.move_player(1)
            print(player.x,player.y)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            player.move_player(2)
            print(player.x,player.y)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            player.move_player(3)
            print(player.x,player.y)
            
            
        

    screen.fill("white")
    player.draw_player(screen)
    maze.draw_maze(screen)
    maze.draw_walls(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
