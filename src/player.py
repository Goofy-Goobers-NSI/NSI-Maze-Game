import pygame
# Sound for movement of the player
pygame.mixer.init()
wall_hitting_sound = pygame.mixer.Sound("assets\sounds\wall_hit_sound.wav")
movement_woosh_sound = pygame.mixer.Sound("assets\sounds\woosh_movement.wav")
# Dictionary to simplify the player movement code
move_keybinds = {"ARROWS":[pygame.K_UP,pygame.K_RIGHT,pygame.K_DOWN,pygame.K_LEFT],"ZQSD":[pygame.K_z,pygame.K_d,pygame.K_s,pygame.K_q],"WASD":[pygame.K_w,pygame.K_d,pygame.K_s,pygame.K_a]}

class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y 

    def draw_player(self,screen,maze):
        x = maze.offset_x + self.x*maze.cell_size + 10
        y = maze.offset_y + self.y*maze.cell_size + 10
        pygame.draw.rect(screen,"purple",[x,y,20,20])
        pygame.draw.rect(screen,"black",[x,y,20,20],3)

    def player_movement(self,pressed_key,movement_keys,maze,timer):
        if timer > 0:
            if pressed_key == move_keybinds[movement_keys][0]:
                if self.check_wall_collisions(0,maze):
                    self.move_player(0)
                    movement_woosh_sound.play()
                else:
                    wall_hitting_sound.play()
            elif pressed_key == move_keybinds[movement_keys][1]:
                if self.check_wall_collisions(1,maze):
                    self.move_player(1)
                    movement_woosh_sound.play()
                else:
                    wall_hitting_sound.play()
            elif pressed_key == move_keybinds[movement_keys][2]:
                if self.check_wall_collisions(2,maze):
                    self.move_player(2)
                    movement_woosh_sound.play()
                else:
                    wall_hitting_sound.play()
            elif pressed_key == move_keybinds[movement_keys][3]:
                if self.check_wall_collisions(3,maze):
                    self.move_player(3)
                    movement_woosh_sound.play()
                else:
                    wall_hitting_sound.play()

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