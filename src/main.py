import pygame,random
from maze import Maze
from player import Player
from solver import Solver
from smarty_pants import Smartypants
from menu import Background,Button,play_button_image,add_time,draw_menu,draw_leaderboard,draw_end_screen,check_in_leaderboard,draw_name_window,draw_play_solo_duo

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
maze_type = "solo"
player_name = "|"
has_written_name = False
render_buttons = True
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

# Sounds
countdown_sound = pygame.mixer.Sound("assets\sounds\countdown_sound.wav")
go_sound = pygame.mixer.Sound("assets\sounds\Go.wav")
secret_go_sound = pygame.mixer.Sound("assets\sounds\Goon.wav") # Time to goon

# Initializing variables for text
game_font_XXXS = pygame.font.Font("assets\_fonts\Racing.otf",30)
game_font_XXS = pygame.font.Font("assets\_fonts\Racing.otf",40)
game_font_XS = pygame.font.Font("assets\_fonts\Racing.otf",50)
game_font_under_S = pygame.font.Font("assets\_fonts\Racing.otf",65)
game_font_S = pygame.font.Font("assets\_fonts\Racing.otf",75)
game_font_M = pygame.font.Font("assets\_fonts\Racing.otf",100)
game_font_L = pygame.font.Font("assets\_fonts\Racing.otf",150)
game_font_XL = pygame.font.Font("assets\_fonts\Racing.otf",350)
game_font_XXL = pygame.font.Font("assets\_fonts\Racing.otf",375)
game_title1 = game_font_L.render("MAZE",True,(177, 18, 38))
game_title11 = game_font_L.render("RACERS",True,(177, 18, 38))
timer_text = game_font_M.render(f"Time : {timer}",True,(50,50,50))

# AAAAAALLLLLLLL the butttooooooooons
play_button = Button(250,480,900,150)
settings_button = Button(250,650,900,150)
leaderboard_button = Button(20,320,130,130)
cat_button = Button(1290,320,130,130)
fastest_time = Button(250,100,300,50)
endurance_easy = Button(250,262,300,50)
endurance_medium = Button(250,425,300,50)
endurance_hard = Button(250,586,300,50)
endurance_expert = Button(250,748,300,50)
close_button = Button(1175,75,50,50)
back_to_menu = Button(750,475,300,100)
play_again = Button(350,475,300,100)
solo_button = Button(205,400,450,450)
duo_button = Button(795,400,450,450)
return_button = Button(25,25,100,100)

# Create the Maze
maze = Maze(15, 15)
maze.generate_maze()

# Player Racer
player = Player(maze.start.x,maze.start.y)

# Solve Maze
solver = Solver(maze)
solution_path = solver.solve()

# AI Racer
smarty = Smartypants(maze, solver)

while running:
    click = False
    key_pressed = False
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
        cooldown = 0
        draw_menu(menu_background,pygame.time.get_ticks(),game_title1,game_title11,play_button,settings_button,leaderboard_button,cat_button)
        
        if menu_state == "leaderboard":
            draw_leaderboard(game_font_XXXS,game_font_XXS,category,fastest_time,endurance_easy,endurance_medium,endurance_hard,endurance_expert,close_button)

        elif menu_state == "gamemode_soloduo":
            draw_play_solo_duo(game_font_XXS,game_font_S,solo_button,duo_button,return_button,game_title1,game_title11,menu_background,pygame.time.get_ticks())

            if solo_button.is_hovered() and click:
                game_state = "game"
                gamemode = "time_trial"
                maze = Maze(15,15)
                maze.generate_maze()
                player.x = maze.start.x
                player.y = maze.start.y
                timer = -300 # Starts at '-5 seconds' for the cooldown
                player_name = "|"
                has_written_name = False
                maze_type = "solo"

            elif duo_button.is_hovered() and click:
                game_state = "game"
                gamemode = "versus_ai"
                maze = Maze(15,15)
                maze.generate_maze()
                solver = Solver(maze)
                solution_path = solver.solve()
                smarty = Smartypants(maze, solver)
                player.x = maze.start.x
                player.y = maze.start.y
                

                timer = -300 # Starts at '-5 seconds' for the cooldown
                category = "casual"
                player_name = "|"
                has_written_name = False
                maze_type = "versus"

            elif return_button.is_hovered() and click:
                menu_state = None

        if leaderboard_button.is_hovered() and click:
            if menu_state == "leaderboard":
                menu_state = None
            else:
                menu_state = "leaderboard"

        if close_button.is_hovered() and click:
            menu_state = None

        if play_button.is_hovered() and click: #  Could be simplified but there are technical issues when I do
            menu_state = "gamemode_soloduo"
    
    elif game_state == "finished":
        screen.fill("white")
        screen.blit(dark_overlay,(0,0))
        maze.draw_mazes(screen,(210,210,210),maze_type)
        player.draw_player(screen,maze)
        if gamemode == "versus_ai":
            smarty.draw(screen,maze)
        draw_end_screen(game_font_S,back_to_menu,play_again,timer_text,render_buttons,who_won)

        if check_in_leaderboard(category,round(timer/60,2)) and not(has_written_name) and who_won == "player": # If player is in leaderboard, ask for his name
            draw_name_window(game_font_XS,player_name)
            render_buttons = False
            if key_pressed:
                if key == pygame.K_RETURN:
                    if 1 < len(player_name) < 21:
                        add_time(category,player_name[:-1],round(timer/60,2))
                        has_written_name = True
                        render_buttons = True
                elif key == pygame.K_BACKSPACE:  
                    player_name = player_name[:-2] + "|"
                else:
                    player_name = player_name[:-1] + event_key.unicode + "|"


        if play_again.is_hovered() and click and render_buttons:
            game_state = "game"
            maze = Maze(15,15)
            maze.generate_maze()
            player.x = maze.start.x
            player.y = maze.start.y
            solver = Solver(maze)
            solution_path = solver.solve()
            smarty = Smartypants(maze, solver)
            timer = -300
            category = "casual"
            has_written_name = False

        elif back_to_menu.is_hovered() and click and render_buttons:
            game_state = "menu"
            menu_state = None
    else:
        timer += 1
        if key_pressed: # This accounts for movements of the player
            player.player_movement(key,movement_keys,maze,timer)
                
        screen.fill("white")
        if timer <= 0: # What happens during the 5,4,3,2,1 countdown
            remaining_time = -timer
            screen.blit(dark_overlay,(0,0))
            maze.draw_mazes(screen,(210,210,210),maze_type)
            player.draw_player(screen,maze)
            if gamemode == "versus_ai":
                smarty.draw(screen,maze)
            timer_text = game_font_L.render(f"{(remaining_time)//60 + 1}",True,(215,210,15))
            timer_text2 = game_font_L.render(f"{(remaining_time)//60 + 1}",True,(0,0,0))

            if remaining_time == 0:
                if random.random() < 0.95:
                    go_sound.play()
                else:
                    secret_go_sound.play()

            if remaining_time <= 180:
                screen.blit(timer_text2,(655,-10))
                screen.blit(timer_text,(660,-5))
                if (remaining_time % 60) == 0 and remaining_time > 0: # Because '1' is thinner than '2' and '3', we push it to the right to make it look like it didn't move
                    countdown_sound.play()

            else:
                timer_text = game_font_XL.render(f"{(remaining_time)//60 + 1}",True,(215,210,15))
                timer_text2 = game_font_XXL.render(f"{(remaining_time)//60 + 1}",True,(0,0,0))
                screen.blit(timer_text2,(555,195))
                screen.blit(timer_text,(565,210))    

        else:
            screen.blit(light_overlay,(0,0))
            if timer % 60 < 5 or 10 < timer % 60 < 15: # Making timer flicker red every second
                timer_text = game_font_M.render(f"Time : {round(timer/60,2)}",True,(177,18,38))
            else:
                timer_text = game_font_M.render(f"Time : {round(timer/60,2)}",True,(50,50,50)) 

            screen.blit(timer_text,(450,30))
            maze.draw_mazes(screen,(243,243,243),maze_type)
            player.draw_player(screen,maze)
            if gamemode == "versus_ai":
                smarty.update(pygame.time.get_ticks())
                smarty.draw(screen,maze)


            # All that happens when you finish the maze
            if player.check_victoire(maze) or smarty.smarty_win(maze): # When you reach the end, cool 3D text goes brr.
                timer_text = game_font_M.render(f"Time : {round(timer/60,2)}",True,(220,220,30))
                timer_text2 = game_font_M.render(f"Time : {round(timer/60,2)}",True,(50,50,50))
                screen.blit(timer_text2,(448,28))
                screen.blit(timer_text,(450,30))   
                game_state = "finished"
                if player.check_victoire(maze):
                    who_won = "player"
                else:
                    who_won = "AI"
            
    pygame.display.flip()

    clock.tick(60)

pygame.quit()