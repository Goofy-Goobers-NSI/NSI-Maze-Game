import pygame
from maze import Maze
from player import Player
from solver import Solver
from menu import Background

# Pygame setup
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1440,900))
clock = pygame.time.Clock()
running = True
game_state = "menu"
# Initializing variables for images 
background_image = pygame.image.load("assets\images\maze_menu_background.jpg").convert_alpha()
menu_background = Background(-1780,-2050,background_image)
# Initializing variables for sound
wall_hitting_sound = pygame.mixer.Sound("assets\sounds\wall_hit_sound.wav")
movement_woosh_sound = pygame.mixer.Sound("assets\sounds\woosh_movement.wav")
# Initializing variables for text
game_font = pygame.font.Font("assets\_fonts\Racing.otf",150)
game_font2 = pygame.font.Font("assets\_fonts\Racing.otf",156)
victory_text1 = game_font.render("Congrats, you",True,(220,220,30))
victory_text2 = game_font2.render("win !",True,(220,220,30))
victory_text11 = game_font.render("Congrats, you",True,(0,0,0))
victory_text21 = game_font2.render("win !",True,(0,0,0))
game_title1 = game_font.render("MAZE",True,(177, 18, 38))
game_title11 = game_font.render("RACERS",True,(177, 18, 38))
game_title2 = game_font.render("MAZE",True,(250,200,135))
game_title22 = game_font.render("RACERS",True,(250,200,135))
game_title3 = game_font2.render("MAZE",True,(43,43,43))
game_title33 = game_font2.render("RACERS",True,(43,43,43))

# Create the Maze
maze = Maze(15, 15)
maze.generate_maze()

player = Player(maze.start.x,maze.start.y)

solver = Solver(maze)
solution_path = solver.solve()

while running:
    if game_state == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        current_time = pygame.time.get_ticks()
        screen.fill("white")
        menu_background.move_background(screen,current_time)
        print(menu_background.cooldown,current_time)
        pygame.draw.rect(screen,(250,200,135),[375,120,650,350])
        pygame.draw.rect(screen,(43,43,43),[375,120,650,350],7)    
        screen.blit(game_title1,(475,135))
        screen.blit(game_title11,(400,255))
              
    else:
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
            screen.blit(victory_text11,(121,346))
            screen.blit(victory_text21,(251,436))
            screen.blit(victory_text1,(125,350))
            screen.blit(victory_text2,(255,440))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
