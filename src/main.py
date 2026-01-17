import pygame,time
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
# Core game variables
movement_keys = 'ZQSD' # Is gonna be changable in settings : WASD or ZQSD or ARROWS
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
light_overlay = pygame.Surface(screen.get_size(),pygame.SRCALPHA) # Permet d'avoir un effet de transparence
light_overlay.fill((200,200,200,50))
dark_overlay = pygame.Surface(screen.get_size(),pygame.SRCALPHA) # Permet d'avoir un effet de transparence
dark_overlay.fill((200,200,200,200))

# Initializing variables for text
game_font = pygame.font.Font("assets\_fonts\Racing.otf",150)
game_font2 = pygame.font.Font("assets\_fonts\Racing.otf",100)
game_font3 = pygame.font.Font("assets\_fonts\Racing.otf",350)
game_font4 = pygame.font.Font("assets\_fonts\Racing.otf",375)
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
    click = False
    current_time = pygame.time.get_ticks()
    if game_state == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        has_won = [False,False]
        cooldown = 0
        screen.fill("white")

        # Background doing it's thing
        menu_background.move_background(screen,current_time)
        screen.blit(light_overlay,(0,0))

        # Logo
        pygame.draw.rect(screen,(250,200,135),[375,70,650,350])
        pygame.draw.rect(screen,(43,43,43),[375,70,650,350],7)
        screen.blit(game_title1,(475,85))
        screen.blit(game_title11,(400,205))

        # Play button (Don't forget to subscribe so i get the 10M platinum one)
        play_button = Button(250,480,900,150)
        play_button.render_button(screen)
        screen.blit(play_button_image,(650,490))
        if play_button.is_hovered() and click: #  Could be simplified but there are technical issues when I do
            game_state = "game"
            maze = Maze(15,15)
            maze.generate_maze()
            player.x = maze.start.x
            player.y = maze.start.y
            timer = 0
            first_time_cooldown = current_time + 3000
        
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
            elif event.type == pygame.KEYDOWN: # This accounts for movements of the player
                player.player_movement(event.key,movement_keys,maze,first_time_cooldown,current_time,has_won)
            
        screen.fill("white")
        if first_time_cooldown > current_time: # What happens during the 3,2,1 countdown
            screen.blit(dark_overlay,(0,0))
            maze.draw_mazes(screen,(210,210,210))
            player.draw_player(screen,maze)
            timer_text = game_font3.render(f"{(first_time_cooldown-current_time)//1000 + 1}",True,(215,210,15))
            timer_text2 = game_font4.render(f"{(first_time_cooldown-current_time)//1000 + 1}",True,(0,0,0))
            fake_timer = game_font2.render(f"Time : 0",True,(50,50,50))
            screen.blit(fake_timer,(475,30))
            if first_time_cooldown-current_time <= 1000: # Because '1' is thinner than '2' and '3', we push it to the right to make it look like it didn't move
                screen.blit(timer_text2,(590,195))
                screen.blit(timer_text,(600,210))
            else:
                screen.blit(timer_text2,(555,195))
                screen.blit(timer_text,(565,210))
            
        else:
            screen.blit(light_overlay,(0,0))
            if has_won[0] == False:
                timer += 1
            if timer % 60 < 5 or 10 < timer % 60 < 15: # Making timer flicker red every second
                timer_text = game_font2.render(f"Time : {round(timer/60,2)}",True,(177,18,38))
            else:
                timer_text = game_font2.render(f"Time : {round(timer/60,2)}",True,(50,50,50)) 
            screen.blit(timer_text,(450,30))
            maze.draw_mazes(screen,(243,243,243))
            player.draw_player(screen,maze)
            # All that happens when you finish the maze
            if player.check_victoire(maze): # When you reach the end, cool 3D text goes brr.
                screen.blit(victory_text11,(21,346))
                screen.blit(victory_text1,(25,350))
                timer_text = game_font2.render(f"Time : {round(timer/60,2)}",True,(220,220,30)) 
                timer_text2 = game_font2.render(f"Time : {round(timer/60,2)}",True,(50,50,50))
                screen.blit(timer_text2,(448,28))
                screen.blit(timer_text,(450,30))   
                if has_won[0] == False:
                    has_won = [True,True]
        pygame.display.flip()
    pygame.display.flip()
    if has_won == [True,True]:
        cooldown = 180
        has_won[1] = False
    if has_won == [True,False]:
        cooldown -= 1
    if has_won == [True,False] and cooldown <= 0:
        print(round(timer/60,2))
        game_state = "menu"


    clock.tick(60)

pygame.quit()