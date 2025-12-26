import pygame
import random
from maze import N, E, S, W, DX, DY

class Smartypants:
    def __init__(self, maze, solver, mistake_chance=0.5):
        self.maze = maze
        self.solver = solver
        self.current_i = 0
        self.solution_path = solver.solution_path
        self.current_cell = self.solution_path[0]
        self.speed = 400  # milliseconds per move
        self.last_move_time = pygame.time.get_ticks()

        self.mistake_chance = mistake_chance
        self.making_mistake = False
        self.mistake_path = [] 
        # I want mistake path to be an actual path, not a random direction for smarty to follow...
        self.mistake_i = 0
        self.error_cooldown = 0
        self.mistake_start_index = 0

    def update(self, current_time):
        if not self.solution_path:
            return None
        
        if current_time - self.last_move_time < self.speed:
            return None
        
        self.last_move_time = current_time

        if self.making_mistake:
            self.follow_mistake_path()
        else:
            self.follow_solution_path(current_time)

    def follow_solution_path(self, current_time):
        if self.current_i >= len(self.solution_path) - 1:
            self.current_cell = self.solution_path[-1]
            return None
        
        self.current_i += 1
        self.current_cell = self.solution_path[self.current_i]
        
        if current_time > self.error_cooldown and random.random() <= self.mistake_chance and self.current_i < len(self.solution_path) - 3:
            self.start_mistake()


    def start_mistake(self):
        self.making_mistake = True
        self.mistake_start_index = self.current_i
        self.mistake_path = []
        current = self.current_cell
        valid_directions = [N, E, S, W]

        if self.current_i < len(self.solution_path) - 1:
            next_cell = self.solution_path[self.current_i + 1]
            dx = next_cell.x - current.x
            dy = next_cell.y - current.y
            good_dir = None
            for dir in valid_directions:
                if DX[dir] == dx and DY[dir] == dy:
                    good_dir = dir
                    break

            if good_dir is not None and good_dir in valid_directions:
                valid_directions.remove(good_dir)
            
        random.shuffle(valid_directions) # I hate this
        mistake_found = False

        for dir in valid_directions:
            # most of the time a valid direction is just backwards so the algorithm ends up walking backwards
            # fuh naw lobotomy
            if not current.walls[dir]:
                ny = current.y + DY[dir]
                nx = current.x + DX[dir]

                if 0 <= nx < self.maze.largeur and 0 <= ny < self.maze.hauteur:
                    next_cell = self.maze.grille[nx][ny]
                    self.mistake_path.append(next_cell)
                    mistake_length = random.randint(2, 8)

                    for i in range(mistake_length - 1):
                        current_mistake = self.mistake_path[-1]
                        if not current_mistake.walls[dir]:
                            mistake_nx = current_mistake.x + DX[dir]
                            mistake_ny = current_mistake.y + DY[dir]
                            if 0 <= mistake_nx < self.maze.largeur and 0 <= mistake_ny < self.maze.hauteur:
                                self.mistake_path.append(self.maze.grille[mistake_nx][mistake_ny])
                    
                    mistake_found = True
                    break

        if mistake_found:
            self.mistake_i = 0
            self.error_cooldown = pygame.time.get_ticks() + 2000  # 2 seconds
        else:
            self.making_mistake = False

    def follow_mistake_path(self):
        if self.mistake_i >= len(self.mistake_path):
            # Mistake is over, return to the solution path
            self.making_mistake = False
            # This is dumb because it teleports smarty back to where he was before making the mistake
            # What needs to be done is: smarty walks back to his last position before a mistake 
            # Don't advance current_i, smarty needs to continue from where he left off
            self.current_cell = self.solution_path[self.mistake_start_index]
            self.current_i = self.mistake_start_index
            return
        
        # Follow the mistake path
        self.current_cell = self.mistake_path[self.mistake_i]
        self.mistake_i += 1

    def draw(self, screen, offset_x, offset_y):
        if not self.current_cell:
            return
        
        cell_size = self.maze.cell_size
        
        center_x = offset_x + self.current_cell.x * cell_size + cell_size // 2
        center_y = offset_y + self.current_cell.y * cell_size + cell_size // 2
        
        if self.making_mistake:
            # Red if making mistake
            color = (255, 100, 100)
            radius = cell_size // 2
        else:
            # Blue normally
            color = (100, 100, 255)
            radius = cell_size // 3
        
        pygame.draw.circle(screen, color, (center_x, center_y), radius)
        pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), radius, 2)
        
        # Draw arrow to next cell in solution path
        if not self.making_mistake and self.current_i < len(self.solution_path) - 1:
            next_cell = self.solution_path[self.current_i + 1]
            next_x = offset_x + next_cell.x * cell_size + cell_size // 2
            next_y = offset_y + next_cell.y * cell_size + cell_size // 2
            pygame.draw.line(screen, (255, 255, 0), (center_x, center_y), (next_x, next_y), 2)
    
    def is_finished(self):
        if not self.solution_path:
            return False
        return self.current_i >= len(self.solution_path) - 1