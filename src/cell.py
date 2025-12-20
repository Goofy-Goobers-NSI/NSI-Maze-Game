class Cellule:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.walls = [True] * 4 
        self.direction = None
        
    def remove_walls(self,list_walls): # wall_direction will take the form of a list : [1,0,1,0] will be one wall on top and one on bottom.
        if list_walls[0] == 0: # If direction is North or South
            if list_walls[1] > 0: # Direction = South
                self.walls[2] = False
            else: # Direction = South
                self.walls[0] = False
        else: # Direction = East or West
            if list_walls[0] > 0: # Direction = East
                self.walls[1] = False
            else: # Direction = West
                self.walls[3] = False
                
    def __repr__(self):
        return " [ " + str(self.x) + ", " + str(self.y) + ", " + str(self.walls) + " ] "
    
    def __eq__(self,cell):
        return self.x == cell.x and self.y == cell.y
    
    def __hash__(self):
        return hash((self.x, self.y))
