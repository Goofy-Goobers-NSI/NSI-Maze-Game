import pygame
from cell import Cellule
from random import randint

# Directions
N, E, S, W = 0, 1, 2, 3
DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}
OPPOSITE = {E: W, W: E, N: S, S: N}

class Maze:
    def __init__(self, largeur=15, hauteur=15, cell_size=40, offset_x=340, offset_y=60):
        self.largeur = largeur
        self.hauteur = hauteur
        self.cell_size = cell_size
        self.offset_x = offset_x
        self.offset_y = offset_y

        # Create grid of cell objects
        self.grille = [[Cellule(x, y) for x in range(largeur)] for y in range(hauteur)]
        self.in_maze = set()  # for Wilson's algorithm

        # start and end placeholders
        self.start = None
        self.end = None

    def choose_start(self):
        # Pick a random border cell as starting point
        while True:
            x = randint(0, self.largeur - 1)
            y = randint(0, self.hauteur - 1)
            if x in (0, self.largeur - 1) or y in (0, self.hauteur - 1):
                self.start = self.grille[y][x]
                return self.start

    def choose_end(self):
         # Pick the cell opposite to the start on the other side
        if not self.start:
            return None

        x, y = self.start.x, self.start.y
        end_x = (self.largeur - 1) - x
        end_y = (self.hauteur - 1) - y
        self.end = self.grille[end_y][end_x]
        return self.end

    def draw_maze(self, screen):
        # Draw the maze grid and highlight start/end
        for y in range(self.hauteur):
            for x in range(self.largeur):
                cell = self.grille[y][x]
                self.draw_cell(screen, cell)

    def draw_cell(self, screen, cell):
        """Draw one cell and its walls"""
        x = self.offset_x + cell.x * self.cell_size
        y = self.offset_y + cell.y * self.cell_size
        s = self.cell_size

        # If start or end, color red
        if cell == self.start or cell == self.end:
            pygame.draw.rect(screen, "red", [x, y, s, s], 4)
        else:
            pygame.draw.rect(screen, "black", [x, y, s, s], 1)

        # Later: draw lines only where walls = True
