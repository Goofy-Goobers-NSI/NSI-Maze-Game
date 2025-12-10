import pygame
import cell
from random import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
screen.fill("white")
cells = []

def choose_start():
    cellule_possible = cells[randint(0,len(cells))]
    while cellule_possible[0] != 340 or cellule_possible[0] != 905 or cellule_possible[1] != 60 or cellule_possible[1] != 620: # Trouver une cellule qui est sur le bord pour avoir un départ valide.
        cellule_possible = cells[randint(0,len(cells))]
    return cellule_possible
    
def choose_end(start_cell):
    for cellule in cells:
        if cellule.x == 600 + 2*340 - start_cell.x and cellule.y == 600 + 2*65 - start_cell.y:
            return cellule

cellule_depart = choose_start()
cellule_fin = choose_end(cellule_depart)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    
    for i in range(15):
        for j in range(15):
            new_cell = cell.Cellule(40*i+340,40*j+60)
            cells.append(new_cell)
            pygame.draw.rect(screen,"black",[new_cell.x,new_cell.y,40,40],1)
            
        # while on trouve pas une cell, on en prend une random dans cells et on check ses coordonnées
        
    
    print(cells)
        
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()


