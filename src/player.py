import pygame

class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y 

    def draw_player(self,screen,maze):
        x = maze.offset_x + self.x*maze.cell_size + 10
        y = maze.offset_y + self.y*maze.cell_size + 10
        pygame.draw.rect(screen,"purple",[x,y,20,20])
        pygame.draw.rect(screen,"black",[x,y,20,20],3)

    def move_player(self,direction): # direction is equal to 1,2,3 or 4 meaning up,right,down,left
        if direction == 0:
            self.y -= 1
        elif direction == 1:
            self.x += 1
        elif direction == 2:
            self.y += 1
        else:
            self.x -= 1

    def check_wall_collisions(self,direction,maze):
        corresponding_wall = maze.grille[self.x][self.y].walls[direction]
        return not(corresponding_wall)
    
    def check_victoire(self,maze):
        return self.x == maze.end.x and self.y == maze.end.y