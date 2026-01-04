import pygame
from maze import Maze
from player import Player
from solver import Solver
from menu import Background,Button

# Pygame setup
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1440,900))
clock = pygame.time.Clock()
pygame.display.set_caption("Maze racers")
running = True
game_state = "menu"

# Timer
timer = 0

# Initializing variables for images 
background_image = pygame.image.load("assets\images\maze_menu_background.jpg").convert_alpha()
menu_background = Background(-1780,-2050,background_image)
play_button_image = pygame.image.load("assets\images\play.png").convert_alpha()
play_button_image = pygame.transform.scale(play_button_image,(130,130))
settings_image = pygame.image.load("assets\images\cog.png").convert_alpha()
settings_image = pygame.transform.scale(settings_image,(130,130))
leaderboard_image = pygame.image.load("assets\images\_trophy.png").convert_alpha()
leaderboard_image = pygame.transform.scale(leaderboard_image,(110,95))
CAT = pygame.image.load("assets\images\cat.png").convert_alpha()
CAT = pygame.transform.scale(CAT,(110,82))
# Initializing variables for sound
wall_hitting_sound = pygame.mixer.Sound("assets\sounds\wall_hit_sound.wav")
movement_woosh_sound = pygame.mixer.Sound("assets\sounds\woosh_movement.wav")

# Initializing variables for text
game_font = pygame.font.Font("assets\_fonts\Racing.otf",150)
game_font2 = pygame.font.Font("assets\_fonts\Racing.otf",100)
victory_text1 = game_font.render("Congrats, you win",True,(220,220,30))
victory_text11 = game_font.render("Congrats, you win",True,(0,0,0))
game_title1 = game_font.render("MAZE",True,(177, 18, 38))
game_title11 = game_font.render("RACERS",True,(177, 18, 38))
timer_text = game_font2.render(f"Time : {timer}",True,(50,50,50))

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
        has_won = False
        screen.fill("white")

        # Background doing it's thing
        menu_background.move_background(screen,current_time)

        # Logo
        pygame.draw.rect(screen,(250,200,135),[375,70,650,350])
        pygame.draw.rect(screen,(43,43,43),[375,70,650,350],7)
        screen.blit(game_title1,(475,85))
        screen.blit(game_title11,(400,205))

        # Play button (Don't forget to subscribe so i get the 10M platinum one)
        play_button = Button(250,480,900,150)
        play_button.render_button(screen)
        screen.blit(play_button_image,(650,490))
        if play_button.is_clicked():
            game_state = "game"
            maze.generate_maze()
            player.x = maze.start.x
            player.y = maze.start.y
            timer = 0
        
        # Settings button
        settings_button = Button(250,650,900,150)
        settings_button.render_button(screen)
        screen.blit(settings_image,(635,660))
        
        # Leaderboard button
        leaderboard_button = Button(20,320,130,130)
        leaderboard_button.render_button(screen)
        screen.blit(leaderboard_image,(30,337))

        # Cat button :3
        cat_button = Button(1290,320,130,130)
        cat_button.render_button(screen)
        screen.blit(CAT,(1300,344))

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
            screen.blit(victory_text11,(21,346))
            screen.blit(victory_text1,(25,350))
            timer_text = game_font2.render(f"Time : {round(timer/60,2)}",True,(220,220,30)) 
            has_won = True
        else:
            timer += 1
            if timer % 60 < 5 or 10 < timer % 60 < 15:
                timer_text = game_font2.render(f"Time : {round(timer/60,2)}",True,(177,18,38))
            else:
                timer_text = game_font2.render(f"Time : {round(timer/60,2)}",True,(50,50,50)) 
        screen.blit(timer_text,(450,30))
        
    pygame.display.flip()
    if has_won:
            pygame.time.wait(3000)
            game_state = "menu"
    clock.tick(60)

pygame.quit()
