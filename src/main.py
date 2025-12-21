import pygame
from maze import Maze
from player import Player

# Pygame setup
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

wall_hitting_sound = pygame.mixer.Sound("wall_hit_sound.wav")
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
            if player.check_wall_collisions(0,maze):
                player.move_player(0)
            else:
                wall_hitting_sound.play()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if player.check_wall_collisions(1,maze):
                player.move_player(1)
            else:
                wall_hitting_sound.play()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            if player.check_wall_collisions(2,maze):
                player.move_player(2)
            else:
                wall_hitting_sound.play()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            if player.check_wall_collisions(3,maze):
                player.move_player(3)
            else:
                wall_hitting_sound.play()
            
            
        

    screen.fill("white")
    player.draw_player(screen,maze)
    maze.draw_maze(screen)
    maze.draw_walls(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
