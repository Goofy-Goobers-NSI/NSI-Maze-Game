# Ce fichier sera une sorte de librairie de fonctions pour créer le menu principal du jeu
import random
class Background:
    def __init__(self,x,y,image):
        self.x = x
        self.y = y
        self.cooldown = 1000
        self.speed = 2
        self.image = image
        self.x_movement = 0
        self.y_movement = 0 
    def move_background(self,screen,current_time):
        if self.x < -3560 or self.x > 0:
            self.x_movement *= -1
        if self.y < -4100 or self.y > 0:
            self.y_movement *= -1
        self.x += self.x_movement * self.speed
        self.y += self.y_movement * self.speed
        if self.cooldown < current_time:
            self.cooldown = current_time + 3000
            self.x_movement = random.randint(-1,1) #-1,0,1
            self.y_movement = random.randint(-1,1)
        screen.blit(self.image,(self.x,self.y))