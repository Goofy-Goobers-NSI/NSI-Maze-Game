import pygame
from maze import Maze
from player import Player
from solver import Solver
from menu import Background,Button,play_button_image,add_time,draw_menu,draw_leaderboard,draw_end_screen,check_in_leaderboard,draw_name_window
leaderboard_file = "leaderboard.json"
# Pygame setup
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1440,900))
clock = pygame.time.Clock()
pygame.display.set_caption("Maze racers")
running = True
# Core game variables
movement_keys = 'ARROWS' # Is gonna be changable in settings : WASD or ZQSD or ARROWS
game_state = "menu"
menu_state = "main"
player_name = "|"
has_written_name = False
category = "casual"
# Timer
timer = 0

# Initializing variables for images 
background_image = pygame.image.load("assets\images\maze_menu_background.jpg").convert_alpha()
menu_background = Background(-1780,-2050,background_image)
light_overlay = pygame.Surface(screen.get_size(),pygame.SRCALPHA) # Permet d'avoir un effet de transparence
light_overlay.fill((200,200,200,50))
dark_overlay = pygame.Surface(screen.get_size(),pygame.SRCALPHA) # Permet d'avoir un effet de transparence
dark_overlay.fill((200,200,200,200))

# Initializing variables for text
game_font_XXXS = pygame.font.Font("assets\_fonts\Racing.otf",30)
game_font_XXS = pygame.font.Font("assets\_fonts\Racing.otf",40)
game_font_XS = pygame.font.Font("assets\_fonts\Racing.otf",50)
game_font_S = pygame.font.Font("assets\_fonts\Racing.otf",75)
game_font_M = pygame.font.Font("assets\_fonts\Racing.otf",100)
game_font_L = pygame.font.Font("assets\_fonts\Racing.otf",150)
game_font_XL = pygame.font.Font("assets\_fonts\Racing.otf",350)
game_font_XXL = pygame.font.Font("assets\_fonts\Racing.otf",375)
game_title1 = game_font_L.render("MAZE",True,(177, 18, 38))
game_title11 = game_font_L.render("RACERS",True,(177, 18, 38))
timer_text = game_font_M.render(f"Time : {timer}",True,(50,50,50))

# Create the Maze
maze = Maze(15, 15)
maze.generate_maze()

player = Player(maze.start.x,maze.start.y)

solver = Solver(maze)
solution_path = solver.solve()

while running:
    click = False
    key_pressed = False
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click = True
        elif event.type == pygame.KEYDOWN:
            key_pressed = True
            key = event.key
            event_key = event
    if game_state == "menu":
        has_won = [False,False]
        cooldown = 0
        play_button = Button(250,480,900,150)
        settings_button = Button(250,650,900,150)
        leaderboard_button = Button(20,320,130,130)
        cat_button = Button(1290,320,130,130)
        draw_menu(menu_background,current_time,game_title1,game_title11,play_button,settings_button,leaderboard_button,cat_button)
        
        fastest_time = Button(250,100,300,50)
        endurance_easy = Button(250,262,300,50)
        endurance_medium = Button(250,425,300,50)
        endurance_hard = Button(250,586,300,50)
        endurance_expert = Button(250,748,300,50)
        close_button = Button(1175,75,50,50)
        if leaderboard_button.is_hovered() and click:
            if menu_state == "leaderboard":
                menu_state = None
            else:
                menu_state = "leaderboard"
        if close_button.is_hovered() and click:
            menu_state = None

        if play_button.is_hovered() and click: #  Could be simplified but there are technical issues when I do
            game_state = "game"
            maze = Maze(15,15)
            maze.generate_maze()
            player.x = maze.start.x
            player.y = maze.start.y
            timer = 0
            first_time_cooldown = current_time + 3000
            category = "casual"
            player_name = "|"
            has_written_name = False

        if menu_state == "leaderboard":
            draw_leaderboard(game_font_XXXS,game_font_XXS,category,fastest_time,endurance_easy,endurance_medium,endurance_hard,endurance_expert,close_button)
    elif game_state == "finished":
        screen.fill("white")
        screen.blit(dark_overlay,(0,0))
        maze.draw_mazes(screen,(210,210,210))
        player.draw_player(screen,maze)
        back_to_menu = Button(750,475,300,100)
        play_again = Button(350,475,300,100)
        draw_end_screen(game_font_S,back_to_menu,play_again,timer_text,has_written_name)
        if check_in_leaderboard(category,round(timer/60,2)) and not(has_written_name): # If player is in leaderboard, ask for his name
            draw_name_window(game_font_XS,player_name)
            if key_pressed:
                if key == pygame.K_RETURN:
                    if 1 < len(player_name) < 21:
                        add_time(category,player_name[:-1],round(timer/60,2))
                        has_written_name = True
                elif key == pygame.K_BACKSPACE:  
                    player_name = player_name[:-2] + "|"
                else:
                    player_name = player_name[:-1] + event_key.unicode + "|"
        if play_again.is_hovered() and click and has_written_name:
            game_state = "game"
            maze = Maze(15,15)
            maze.generate_maze()
            player.x = maze.start.x
            player.y = maze.start.y
            timer = 0
            first_time_cooldown = current_time + 3000
            category = "casual"
            has_written_name = False

        elif back_to_menu.is_hovered() and click and has_written_name:
            game_state = "menu"
    else:
        if key_pressed: # This accounts for movements of the player
            player.player_movement(key,movement_keys,maze,first_time_cooldown,current_time,has_won)
                
        screen.fill("white")
        if first_time_cooldown > current_time: # What happens during the 3,2,1 countdown
            screen.blit(dark_overlay,(0,0))
            maze.draw_mazes(screen,(210,210,210))
            player.draw_player(screen,maze)
            timer_text = game_font_XL.render(f"{(first_time_cooldown-current_time)//1000 + 1}",True,(215,210,15))
            timer_text2 = game_font_XXL.render(f"{(first_time_cooldown-current_time)//1000 + 1}",True,(0,0,0))
            fake_timer = game_font_M.render(f"Time : 0",True,(50,50,50))
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
                timer_text = game_font_M.render(f"Time : {round(timer/60,2)}",True,(177,18,38))
            else:
                timer_text = game_font_M.render(f"Time : {round(timer/60,2)}",True,(50,50,50)) 
            screen.blit(timer_text,(450,30))
            maze.draw_mazes(screen,(243,243,243))
            player.draw_player(screen,maze)
            # All that happens when you finish the maze
            if player.check_victoire(maze): # When you reach the end, cool 3D text goes brr.
                timer_text = game_font_M.render(f"Time : {round(timer/60,2)}",True,(220,220,30))
                timer_text2 = game_font_M.render(f"Time : {round(timer/60,2)}",True,(50,50,50))
                screen.blit(timer_text2,(448,28))
                screen.blit(timer_text,(450,30))   
                game_state = "finished"
            
    pygame.display.flip()

    clock.tick(60)

pygame.quit()