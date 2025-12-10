# -*- coding: utf-8 -*-
class Cellule:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.walls = [True] * 4 
        
    def add_walls(self,wall_directions): # wall_direction will take the form of a list : [1,0,1,0] will be one wall on top and one on bottom.
        for indice in range(4):
            if not(wall_directions[indice]):
                self.walls[indice] = False
                
    def __repr__(self):
        return " [ " + str(self.x) + ", " + str(self.y) + ", " + str(self.walls) + " ] "
    
    def __eq__(self,cell):
        return self.x == cell.x and self.y == cell.y
