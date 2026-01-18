# Ce fichier sera une sorte de librairie de fonctions pour créer les menus du jeu
import random
import pygame
import os, json
leaderboard_file = "assets\leaderboard.json"
screen = pygame.display.set_mode((1440,900))
# Images 
background_image = pygame.image.load("assets\images\maze_menu_background.jpg").convert_alpha()
play_button_image = pygame.image.load("assets\images\play.png").convert_alpha()
play_button_image = pygame.transform.scale(play_button_image,(130,130))
settings_image = pygame.image.load("assets\images\cog.png").convert_alpha()
settings_image = pygame.transform.scale(settings_image,(130,130))
leaderboard_image = pygame.image.load("assets\images\_trophy.png").convert_alpha()
leaderboard_image = pygame.transform.scale(leaderboard_image,(110,95))
CAT = pygame.image.load("assets\images\cat.png").convert_alpha()
CAT = pygame.transform.scale(CAT,(110,82))
cross_image = pygame.image.load("assets\images\cross.png").convert_alpha()
cross_image = pygame.transform.scale(cross_image,(100,100))
light_overlay = pygame.Surface(screen.get_size(),pygame.SRCALPHA) # Permet d'avoir un effet de transparence
light_overlay.fill((200,200,200,50))
dark_overlay = pygame.Surface(screen.get_size(),pygame.SRCALPHA) # Permet d'avoir un effet de transparence
dark_overlay.fill((200,200,200,200))
# Text


class Background:
    def __init__(self,x,y,image):
        self.x = x
        self.y = y
        self.cooldown = 1000
        self.speed = 1
        self.image = image
        self.x_movement = 0
        self.y_movement = 0 
    def move_background(self,screen,current_time):
        # Changing directions every 3 seconds
        if self.cooldown < current_time:
            self.cooldown = current_time + 5000
            self.x_movement = random.randint(-1,1) #-1,0,1
            self.y_movement = random.randint(-1,1)
            while self.x_movement == 0 and self.y_movement == 0:
                self.x_movement = random.randint(-1,1) #-1,0,1
                self.y_movement = random.randint(-1,1)
        # Turning around if we hit the image border so we don't have a white background
        if self.x < -3560 or self.x > 0:
            self.x_movement *= -1
        if self.y < -4100 or self.y > 0:
            self.y_movement *= -1
        # If we move diagonnaly, lower the speed so we have constant speed between straight and diagonal
        if self.x_movement != 0 and self.y_movement != 0:
            self.x += self.x_movement * self.speed * 0.75
            self.y += self.y_movement * self.speed * 0.75
        else:
            self.x += self.x_movement * self.speed
            self.y += self.y_movement * self.speed
        # Actually rendering the image
        screen.blit(self.image,(self.x,self.y))

class Button:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def is_hovered(self):
        mouse_x,mouse_y = pygame.mouse.get_pos()
        return self.x <= mouse_x <=self.x + self.width and self.y <= mouse_y <= self.y + self.height
    
    def render_button(self,screen,base_color):
        if self.is_hovered():
            pygame.draw.rect(screen,(169,169,169),[self.x,self.y,self.width,self.height])
        else:
            pygame.draw.rect(screen,base_color,[self.x,self.y,self.width,self.height])

def draw_menu(menu_background,current_time,game_title1,game_title11,play_button,settings_button,leaderboard_button,cat_button):
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
    play_button.render_button(screen,(69,69,69))
    screen.blit(play_button_image,(650,490))
    # Settings button
    settings_button.render_button(screen,(69,69,69))
    screen.blit(settings_image,(635,660))
        
    # Leaderboard button
    leaderboard_button.render_button(screen,(69,69,69))
    screen.blit(leaderboard_image,(30,337))

    # Cat button :3
    cat_button.render_button(screen,(69,69,69))
    screen.blit(CAT,(1300,344))

def draw_end_screen(font,menu_button,play_back_button,timer_text,render_buttons):
    pygame.draw.rect(screen,(50,50,50),[300,200,800,425])
    pygame.draw.rect(screen,(250,200,135),[300,200,800,425],15)
    victory_text1 = font.render("Congrats, you won !",True,(220,220,30))
    victory_text11 = font.render("Congrats, you won !",True,(240,240,240))
    screen.blit(victory_text11,(318,228))
    screen.blit(victory_text1,(320,230))
    if render_buttons:
        menu_button.render_button(screen,(50,50,50))
        play_back_button.render_button(screen,(50,50,50))
    for i in range(2):
        pygame.draw.rect(screen,(230,230,230),[350+i*400,475,300,100],5)
    menu_button_text = font.render("MENU",True,(230,230,230))
    play_button_text = font.render("PLAY",True,(230,230,230))
    screen.blit(menu_button_text,(790,475))
    screen.blit(play_button_text,(400,475))
    screen.blit(timer_text,(425,340))

# Functions for the leaderboard 
def draw_leaderboard(small_font,big_font,category,fastest_time,endurance_e,endurance_m,endurance_h,endurance_ex,close_button):
    pygame.draw.rect(screen,(50,50,50),[200,50,1050,800])
    pygame.draw.rect(screen,(250,200,135),[200,50,1050,800],15)
    fastest_time.render_button(screen,(50,50,50))
    endurance_e.render_button(screen,(50,50,50))
    endurance_m.render_button(screen,(50,50,50))
    endurance_h.render_button(screen,(50,50,50))
    endurance_ex.render_button(screen,(50,50,50))
    close_button.render_button(screen,(50,50,50))
    for i in range(5):
        pygame.draw.rect(screen,(230,230,230),[250,100+i*162,300,50],5)
    fastest_completion = small_font.render("Fastest time",True,(230,230,230))
    endurance_easy = small_font.render("Endurance easy",True,(230,230,230))
    endurance_medium = small_font.render("Endurance medium",True,(230,230,230))
    endurance_hard = small_font.render("Endurance hard",True,(230,230,230))
    endurance_expert = small_font.render("Endurance expert",True,(230,230,230))
    screen.blit(fastest_completion,(300,105))
    screen.blit(endurance_easy,(280,267))
    screen.blit(endurance_medium,(257,430))
    screen.blit(endurance_hard,(275,591))
    screen.blit(endurance_expert,(260,753))
    screen.blit(cross_image,(1150,50))
    leaderboard = load_leaderboard()
    for i in range(1,len(leaderboard[category])+1):
        if i == 1:
            place_text = big_font.render(f"#{i} {leaderboard[category][0]["name"]}",True,(220,220,30))
            time_text = big_font.render(f"{leaderboard[category][0]["time"]}",True,(220,220,30))
        elif i == 2:
            place_text = big_font.render(f"#{i} {leaderboard[category][1]["name"]}",True,(192,192,192))
            time_text = big_font.render(f"{leaderboard[category][1]["time"]}",True,(192,192,192))
        elif i == 3:
            place_text = big_font.render(f"#{i} {leaderboard[category][2]["name"]}",True,(205,127,50))
            time_text = big_font.render(f"{leaderboard[category][2]["time"]}",True,(205,127,50))
        else:
            place_text = big_font.render(f"#{i} {leaderboard[category][i-1]["name"]}",True,(230,230,230))
            time_text = big_font.render(f"{leaderboard[category][i-1]["time"]}",True,(230,230,230))
        screen.blit(place_text,(600,60+70*i))
        screen.blit(time_text,(1100,60+70*i))

# I used chatgpt for the next three functions but I can fully explain it, I swear I can, please don't burn me alive
def load_leaderboard(): # Opens the leaderboard file
    with open(leaderboard_file, "r") as f:
        return json.load(f)
    
def save_leaderboard(data): # Will be called to save the changes made to the leaderboard
    with open(leaderboard_file, "w") as f:
        json.dump(data, f, indent=4)

def add_time(category,player_name,new_time):
    leaderboard = load_leaderboard()
    # Adds the new time, A NEW CHALLENGER HAS ARRIVED !!!!!!
    leaderboard[category].append({
        "name": player_name,
        "time": new_time
    })
    # Sorts the times from lowest to highest
    leaderboard[category].sort(key=lambda entry: entry["time"])
    # Keeps only the ten first entries
    leaderboard[category] = leaderboard[category][:10]
    # Saves changes made, because duh
    save_leaderboard(leaderboard)

def check_in_leaderboard(category,time): # Returns True if time is in leaderboard, used for asking name
    leaderboard = load_leaderboard()
    if len(leaderboard[category]) < 10:
        return True
    else:
        return time < leaderboard[category][9]["time"]

def draw_name_window(font,player_name):
    pygame.draw.rect(screen,(50,50,50),[150,250,1100,275])
    pygame.draw.rect(screen,(250,200,135),[150,250,1100,275],15)
    congratulating_text = font.render("Wow ! You made it to leaderboards !",True,(230,230,230))
    name_text = font.render("Give us your name :",True,(230,230,230))
    restrictions_text1 = font.render("Between 1 and",True,(200,35,25))
    restrictions_text2 = font.render("20 characters",True,(200,35,25))
    screen.blit(congratulating_text,(175,260))
    screen.blit(name_text,(175,310))
    screen.blit(restrictions_text1,(175,375))
    screen.blit(restrictions_text2,(175,425))
    pygame.draw.rect(screen,(230,230,230),[600,380,600,100],3)
    player_name_text = font.render(player_name,True,(230,230,230))
    screen.blit(player_name_text,(620,400))
