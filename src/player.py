import pygame
# Sound for movement of the player
pygame.mixer.init()
wall_hitting_sound = pygame.mixer.Sound("assets\\sounds\\wall_hit_sound.wav")
movement_woosh_sound = pygame.mixer.Sound("assets\\sounds\\woosh_movement.wav")
# Dictionary to simplify the player movement code
move_keybinds = {"ARROWS":[pygame.K_UP,pygame.K_RIGHT,pygame.K_DOWN,pygame.K_LEFT],"ZQSD":[pygame.K_z,pygame.K_d,pygame.K_s,pygame.K_q],"WASD":[pygame.K_w,pygame.K_d,pygame.K_s,pygame.K_a]}

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y 
        self.px = None
        self.py = None
        self.interpolation_speed = 0.25  # 0.1 is slow, 0.4 is kinda snappy, 0.25 is the sweet spot

    def draw_player(self, screen, maze):
        target_px = maze.offset_x + self.x * maze.cell_size + 10
        target_py = maze.offset_y + self.y * maze.cell_size + 10

        if self.px is None or self.py is None or abs(self.px - target_px) > 100 or abs(self.py - target_py) > 100:
            self.px = target_px
            self.py = target_py

        self.px += (target_px - self.px) * self.interpolation_speed
        self.py += (target_py - self.py) * self.interpolation_speed

        if abs(target_px - self.px) < 0.1:
            self.px = target_px
        if abs(target_py - self.py) < 0.1:
            self.py = target_py

        pygame.draw.rect(screen, "purple", [self.px, self.py, 20, 20])
        pygame.draw.rect(screen, "black", [self.px, self.py, 20, 20], 3)

    def player_movement(self, pressed_key, movement_keys, maze, timer):
        if timer > 0:
            if pressed_key == move_keybinds[movement_keys][0]:
                if self.check_wall_collisions(0, maze):
                    self.move_player(0)
                    movement_woosh_sound.play()
                else:
                    wall_hitting_sound.play()
            elif pressed_key == move_keybinds[movement_keys][1]:
                if self.check_wall_collisions(1, maze):
                    self.move_player(1)
                    movement_woosh_sound.play()
                else:
                    wall_hitting_sound.play()
            elif pressed_key == move_keybinds[movement_keys][2]:
                if self.check_wall_collisions(2, maze):
                    self.move_player(2)
                    movement_woosh_sound.play()
                else:
                    wall_hitting_sound.play()
            elif pressed_key == move_keybinds[movement_keys][3]:
                if self.check_wall_collisions(3, maze):
                    self.move_player(3)
                    movement_woosh_sound.play()
                else:
                    wall_hitting_sound.play()

    def move_player(self, direction): # direction is equal to 0, 1, 2 or 3 meaning up,right,down,left
        if direction == 0:
            self.y -= 1
        elif direction == 1:
            self.x += 1
        elif direction == 2:
            self.y += 1
        else:
            self.x -= 1

    def check_wall_collisions(self, direction, maze):
        corresponding_wall = maze.grille[self.x][self.y].walls[direction]
        return not(corresponding_wall)
    
    def check_victoire(self, maze):
        return self.x == maze.end.x and self.y == maze.end.y