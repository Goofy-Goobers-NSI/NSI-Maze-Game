import pygame
from maze import Maze
from player import Player

# Pygame setup
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1440,900))
clock = pygame.time.Clock()
running = True

wall_hitting_sound = pygame.mixer.Sound("assets\sounds\wall_hit_sound.wav")
movement_woosh_sound = pygame.mixer.Sound("assets\sounds\woosh_movement.wav")
game_font = pygame.font.Font("assets\_fonts\Star Crush.ttf",90)
game_font2 = pygame.font.Font("assets\_fonts\Star Crush.ttf",96)
victory_text1 = game_font.render("Congratulations",True,(220,220,30))
victory_text2 = game_font.render("you win",True,(220,220,30))
victory_text11 = game_font.render("Congratulations",True,(0,0,0))
victory_text21 = game_font.render("you win",True,(0,0,0))
# Create the Maze
maze = Maze(15, 15)
maze.generate_maze()
player = Player(maze.start.x,maze.start.y)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            if player.check_wall_collisions(0,maze):
                player.move_player(0)
                movement_woosh_sound.play()
            else:
                wall_hitting_sound.play()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if player.check_wall_collisions(1,maze):
                player.move_player(1)
                movement_woosh_sound.play()
            else:
                wall_hitting_sound.play()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            if player.check_wall_collisions(2,maze):
                player.move_player(2)
                movement_woosh_sound.play()
            else:
                wall_hitting_sound.play()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            if player.check_wall_collisions(3,maze):
                player.move_player(3)
                movement_woosh_sound.play()
            else:
                wall_hitting_sound.play()
            
    screen.fill("white")

    maze.draw_mazes(screen)
    player.draw_player(screen,maze)
    if player.check_victoire(maze): # When you reach the end, cool 3D text goes brr.
        screen.blit(victory_text11,(76,346))
        screen.blit(victory_text21,(231,446))
        screen.blit(victory_text1,(81,350))
        screen.blit(victory_text2,(235,450))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
