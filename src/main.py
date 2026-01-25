import pygame,random
from maze import Maze
from player import Player
from solver import Solver
from smarty_pants import Smartypants
from menu import Background,Button,add_time,draw_menu,draw_leaderboard,draw_end_screen,check_in_leaderboard,draw_name_window,draw_play_solo_duo,draw_cat_menu,draw_setting_menu

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
back_to_menu = Button(750,475,300,100)
play_again = Button(350,475,300,100)
solo_button = Button(205,400,450,450)
duo_button = Button(795,400,450,450)
return_button = Button(25,25,100,100)
wasd_button = Button(390,300,180,100)
zqsd_button = Button(610,300,180,100)
arrows_button = Button(830,300,180,100)
ez_ai_button = 4
mid_ai_button = 5
hard_ai_button = 6

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

# Cats Menu
cat_folder = "assets/images/cats"
cat_catalog = []

for i in range(1, 9):
    file_base = f"{cat_folder}/cat{i}"
    ext = ".png"
    surf = pygame.image.load(f"{file_base}{ext}").convert_alpha()
    surf = pygame.transform.scale(surf, (210, 210))
    cat_catalog.append(surf)

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
        draw_menu(menu_background, pygame.time.get_ticks(), game_title1, game_title11, play_button, settings_button, leaderboard_button, cat_button)
        
        if menu_state == "cats":
            draw_cat_menu(game_font_XS, return_button, menu_background, cat_catalog)
            if click and return_button.is_hovered():
                menu_state = "main"
        elif menu_state == "leaderboard":
            draw_leaderboard(game_font_XXXS, game_font_XXS,menu_background, category, fastest_time, endurance_easy, endurance_medium, endurance_hard, endurance_expert, return_button)
            if click and return_button.is_hovered():
                menu_state = "main"
        elif menu_state == "settings":
            draw_setting_menu(game_font_XXS,game_font_XS,game_font_S,menu_background,return_button,wasd_button,zqsd_button,arrows_button,movement_keys,ez_ai_button,mid_ai_button,hard_ai_button)
            if click:
                if return_button.is_hovered():
                    menu_state = "main"
                elif wasd_button.is_hovered():
                    movement_keys = "WASD"
                elif zqsd_button.is_hovered():
                    movement_keys = "ZQSD"
                elif arrows_button.is_hovered():
                    movement_keys = "ARROWS"
        elif menu_state == "gamemode_soloduo":
            draw_play_solo_duo(game_font_XXS, game_font_S, solo_button, duo_button, return_button, game_title1, game_title11, menu_background, pygame.time.get_ticks())
            if click:
                if return_button.is_hovered():
                    menu_state = "main"
                elif solo_button.is_hovered():
                    game_state = "game"
                    gamemode = "time_trial"
                    maze_type = "solo"
                    maze = Maze(15, 15)
                    maze.generate_maze()
                    player.x, player.y = maze.start.x, maze.start.y
                    timer = -300
                    player_name = "|"
                    has_written_name = False
                elif duo_button.is_hovered():
                    game_state = "game"
                    gamemode = "versus_ai"
                    maze_type = "versus"
                    maze = Maze(15, 15)
                    maze.generate_maze()
                    solver = Solver(maze)
                    solution_path = solver.solve()
                    smarty = Smartypants(maze, solver)
                    player.x, player.y = maze.start.x, maze.start.y
                    timer = -300
                    category = "casual"
                    player_name = "|"
                    has_written_name = False
        elif menu_state == "main":
            if click:
                if play_button.is_hovered():
                    menu_state = "gamemode_soloduo"
                elif leaderboard_button.is_hovered():
                    menu_state = "leaderboard"
                elif cat_button.is_hovered():
                    menu_state = "cats"
                elif settings_button.is_hovered():
                    menu_state = "settings"

    elif game_state == "finished":
        screen.fill("white")
        screen.blit(dark_overlay, (0, 0))
        maze.draw_mazes(screen, (210, 210, 210), maze_type)
        player.draw_player(screen, maze)
        if gamemode == "versus_ai":
            smarty.draw(screen, maze)
        
        # Create the final time text surface for the end screen
        final_time_val = round(timer/60, 2)
        display_timer_text = game_font_M.render(f"Time : {final_time_val}", True, (220, 220, 30))
        
        draw_end_screen(game_font_S, back_to_menu, play_again, display_timer_text, render_buttons, who_won)

        if check_in_leaderboard(category, final_time_val) and not has_written_name and who_won == "player":
            draw_name_window(game_font_XS, player_name)
            render_buttons = False
            if key_pressed:
                if key == pygame.K_RETURN:
                    if 1 < len(player_name) < 21:
                        add_time(category, player_name[:-1], final_time_val)
                        has_written_name, render_buttons = True, True
                elif key == pygame.K_BACKSPACE:  
                    player_name = player_name[:-2] + "|"
                else:
                    player_name = player_name[:-1] + event_key.unicode + "|"

        if click and render_buttons:
            if play_again.is_hovered():
                game_state, timer, has_written_name = "game", -300, False
                maze = Maze(15, 15)
                maze.generate_maze()
                player.x, player.y = maze.start.x, maze.start.y
                if gamemode == "versus_ai":
                    solver = Solver(maze)
                    solution_path = solver.solve()
                    smarty = Smartypants(maze, solver)
            elif back_to_menu.is_hovered():
                game_state, menu_state = "menu", "main"

    else:
        timer += 1
        if key_pressed:
            player.player_movement(key, movement_keys, maze, timer)
                
        screen.fill("white")
        if timer <= 0:
            remaining_time = -timer
            screen.blit(dark_overlay, (0, 0))
            maze.draw_mazes(screen, (210, 210, 210), maze_type)
            player.draw_player(screen, maze)
            if gamemode == "versus_ai":
                smarty.draw(screen, maze)
            
            count_val = (remaining_time // 60) + 1
            timer_text_surf = game_font_L.render(f"{count_val}", True, (215, 210, 15))
            timer_shadow = game_font_L.render(f"{count_val}", True, (0, 0, 0))

            if remaining_time == 0:
                go_sound.play() if random.random() < 0.95 else secret_go_sound.play()

            if remaining_time <= 180:
                screen.blit(timer_shadow, (655, -10))
                screen.blit(timer_text_surf, (660, -5))
                if (remaining_time % 60) == 0 and remaining_time > 0:
                    countdown_sound.play()
            else:
                timer_text_surf = game_font_XL.render(f"{count_val}", True, (215, 210, 15))
                timer_shadow = game_font_XXL.render(f"{count_val}", True, (0, 0, 0))
                screen.blit(timer_shadow, (555, 195))
                screen.blit(timer_text_surf, (565, 210))    

        else:
            screen.blit(light_overlay, (0, 0))
            color = (177, 18, 38) if (timer % 60 < 5 or 10 < timer % 60 < 15) else (50, 50, 50)
            running_timer_surf = game_font_M.render(f"Time : {round(timer/60, 2)}", True, color) 

            screen.blit(running_timer_surf, (450, 30))
            maze.draw_mazes(screen, (243, 243, 243), maze_type)
            player.draw_player(screen, maze)
            
            if gamemode == "versus_ai":
                smarty.update(pygame.time.get_ticks())
                smarty.draw(screen, maze)

            if player.check_victoire(maze) or (gamemode == "versus_ai" and smarty.smarty_win(maze)):
                game_state = "finished"
                who_won = "player" if player.check_victoire(maze) else "AI"
            
    pygame.display.flip()
    clock.tick(60)