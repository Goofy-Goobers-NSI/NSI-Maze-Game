import pygame
from cell import Cellule
from random import randint

# Directions
N, E, S, W = 0, 1, 2, 3
DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}
OPPOSITE = {E: W, W: E, N: S, S: N}
COORD_LIGNE_MURS = {0 : [(0, 0), (40, 0)], 1 : [(40, 0), (40, 40)], 2 : [(40, 40), (0, 40)], 3 : [(0, 40), (0, 0)]}

class Maze:
    def __init__(self, largeur=15, hauteur=15, cell_size=40, offset_x=340, offset_y=60):
        self.largeur = largeur
        self.hauteur = hauteur
        self.cell_size = cell_size
        self.offset_x = offset_x
        self.offset_y = offset_y

        # Create grid of cell objects
        self.grille = [[Cellule(x, y) for y in range(hauteur)] for x in range(largeur)]
        self.in_maze = {self.choose_random_cell()}

        # placeholders
        self.start = None
        self.end = None

    # Super goated helper method :) 
    def choose_random_cell(self): 
        return self.grille[randint(0, self.largeur - 1)][randint(0, self.hauteur - 1)] 

    def choose_start(self):
        # Pick a random border cell as starting point
        while True:
            x = randint(0, self.largeur - 1)
            y = randint(0, self.hauteur - 1)
            if x in (0, self.largeur - 1) or y in (0, self.hauteur - 1):
                self.start = self.grille[x][y]
                return self.start

    def choose_end(self):
         # Pick the cell opposite to the start on the other side
        if not self.start:
            return None

        x, y = self.start.x, self.start.y
        end_x = (self.largeur - 1) - x
        end_y = (self.hauteur - 1) - y
        self.end = self.grille[end_x][end_y]
        return self.end

    def draw_maze(self, screen):
        # Draw the maze grid and highlight start/end
        for y in range(self.hauteur):
            for x in range(self.largeur):
                cell = self.grille[x][y]
                self.draw_start_end_cell(screen, cell)

    def draw_start_end_cell(self, screen, cell):
        """Draw one cell and its walls"""
        x = self.offset_x + cell.x * self.cell_size
        y = self.offset_y + cell.y * self.cell_size
        s = self.cell_size

        # If start or end, color red
        if cell == self.start or cell == self.end:
            pygame.draw.rect(screen, "red", [x, y, s, s], 4)
        #elif cell in self.in_maze:
         #   pygame.draw.rect(screen, "green", [x, y, s, s], 2)
        else:
            pygame.draw.rect(screen, "black", [x, y, s, s], 1)
    
    def draw_walls(self,screen):
        for cell in self.in_maze:
            for wall in cell.walls:
                if not(wall):
                    start_pos =  (self.offset_x + cell.x * self.cell_size + COORD_LIGNE_MURS[cell.walls.index(wall)][0][0]-1,self.offset_y + cell.y * self.cell_size + COORD_LIGNE_MURS[cell.walls.index(wall)][0][1]-1)
                    end_pos = (self.offset_x + cell.x * self.cell_size + COORD_LIGNE_MURS[cell.walls.index(wall)][1][0]-1,self.offset_y + cell.y * self.cell_size + COORD_LIGNE_MURS[cell.walls.index(wall)][1][1]-1)
                    pygame.draw.line(screen,"white",start_pos,end_pos,2)

    def random_walk(self, start_cell):
        '''
        Creates a path that starts from a cell not in the maze
        to a cell in the maze, while removing any loops, this where the term
        "loop erased walk" comes from.
        '''

        path = [start_cell]
        current = start_cell


        while True:
            direction = randint(0, 3)
            nx = current.x + DX[direction]  # next x
            ny = current.y + DY[direction]  # next y

            if nx < 0 or nx >= self.largeur or ny < 0 or ny >= self.hauteur:
                # skips if the next cell would be outside of the grid
                continue

            next_cell = self.grille[nx][ny]

            if next_cell in self.in_maze:  # if cell in maze => exit
                path.append(next_cell)
                break

            if next_cell in path:
                first_occ = path.index(next_cell)
                path = path[:first_occ + 1]
            else:
                path.append(next_cell)
            
            current = next_cell

        self.in_maze.update(path) # merges the path into the maze, .update() is ∪ for sets (les ensembles)
        print(self.in_maze)
        return path

    def carve_path(self, path):
        '''
        Removes walls between cells (set walls to False) in the path,
        The path is a list of Cellule objects from the random_walk() method
        '''
        for i in range(len(path)-1):
            direction  = [path [i+1].x - path[i].x, path [i+1].y - path[i].y]
            for j in range(2):
                direction[j] *= -1
            path[i+1].add_walls(direction)
    
    def generate_maze(self):
        """
        Generates the maze with Wilson's Algorithm,
        keeps looping until every cell is in the maze, if 
        """
        #while len(self.in_maze) < len(self.grille)**2:
        random_cell = Maze.choose_random_cell(self)
        while random_cell in self.in_maze:
            random_cell = Maze.choose_random_cell(self)
        path = Maze.random_walk(self,random_cell)
        Maze.carve_path(self,path)