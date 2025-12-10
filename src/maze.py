import pygame
from cell import Cellule
from random import random


N, E, S, W = 0, 1, 2, 3  # wall index, example: walls[N] is top wall
DX = {E: 1, W: -1, N: 0, S: 0}  # EAST/WEST move by (x+0,y+1) or (x+0, y-1), basically move right/left
DY = {E: 0, W: 0, N: -1, S: 1}  # NORTH/SOUTH move by (x+1, y+0) or (x-1, y+0), move up/down
OPPOSITE = {E: W, W: E, N: S, S: N}
# OPPOSITE is for removing walls when carving through a maze
# The OPPOSITE map will allow for the removal of both walls of adjacent cells

class Maze():
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.grille = [[Cellule(x, y) for x in range(largeur)] for y in range(hauteur)]
        self.in_maze = set()

    def draw_maze(self):
        for y in range(self.hauteur):
            for x in range(self.largeur):
                cell = self.grille[y][x]
                