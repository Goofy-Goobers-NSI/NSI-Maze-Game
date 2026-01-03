# Ce fichier sera une sorte de librairie de fonctions pour créer le menu principal du jeu
import random
import pygame
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
    
    def is_clicked(self):
        for event in pygame.event.get():
            return event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered()
    
    def render_button(self,screen):
        if self.is_hovered():
            pygame.draw.rect(screen,(169,169,169),[self.x,self.y,self.width,self.height])
        else:
            pygame.draw.rect(screen,(69,69,69),[self.x,self.y,self.width,self.height])
