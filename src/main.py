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
conversions_pour_choose_end={ 60 : 620 , 620 : 60 , 340 : 900 , 900 : 340 }

for i in range(15):
        for j in range(15):
            new_cell = cell.Cellule(40*i+340,40*j+60)
            cells.append(new_cell)

def choose_start():
    cellule_possible = cells[randint(0,len(cells)-1)]
    while cellule_possible.x != 340 and cellule_possible.x != 900 and cellule_possible.y != 60 and cellule_possible.y != 620: # Trouver une cellule qui est sur le bord pour avoir un départ valide.
        cellule_possible = cells[randint(0,len(cells)-1)]
    return cellule_possible
    
def choose_end(start_cell):
    for cellule in cells:
        if start_cell.y == 60 or start_cell.y == 620:
            if cellule.x == 560 + 2*340 - start_cell.x and cellule.y == conversions_pour_choose_end[start_cell.y]:
                return cellule
        elif start_cell.x == 340 or start_cell.x == 900:
            if cellule.x == conversions_pour_choose_end[start_cell.x] and cellule.y == 560 + 2*60 - start_cell.y:
                return cellule

cellule_depart = choose_start()
print(cellule_depart)
cellule_fin = choose_end(cellule_depart)
print(cellule_fin)


while running:
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for cellule in cells:  
        if cellule == cellule_depart or cellule == cellule_fin:
            pygame.draw.rect(screen,"red",[cellule.x,cellule.y,40,40],5)
        else:
            pygame.draw.rect(screen,"black",[cellule.x,cellule.y,40,40],1)
            
        
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()


