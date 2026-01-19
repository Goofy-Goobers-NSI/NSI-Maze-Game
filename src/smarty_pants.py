import pygame
import random
from maze import N, E, S, W, DX, DY, OPPOSITE

class Smartypants:
    def __init__(self, maze, solver):
        self.maze = maze
        self.solver = solver
        self.current_i = 0
        self.solution_path = solver.solution_path
        self.current_cell = self.solution_path[0]
        self.speed = 175  # milliseconds per move
        self.last_move_time = pygame.time.get_ticks()

    def update(self, current_time):
        if not self.solution_path:
            return None
        
        if current_time - self.last_move_time < self.speed:
            return None
        
        self.last_move_time = current_time

        self.follow_solution_path(current_time)

    def follow_solution_path(self, current_time):
        if self.current_i >= len(self.solution_path) - 1:
            self.current_cell = self.solution_path[-1]
            return None
        
        self.current_i += 1
        self.current_cell = self.solution_path[self.current_i]

    def draw(self, screen, offset_x, offset_y):
        if not self.current_cell:
            return
        
        cell_size = self.maze.cell_size
        
        center_x = offset_x + self.current_cell.x * cell_size + cell_size // 2
        center_y = offset_y + self.current_cell.y * cell_size + cell_size // 2
        
        # Blue normally
        color = (100, 100, 255)
        radius = cell_size // 3
        
        pygame.draw.circle(screen, color, (center_x, center_y), radius)
        pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), radius, 2)
        
        # Draw arrow to next cell in solution path
        if self.current_i < len(self.solution_path) - 1:
            next_cell = self.solution_path[self.current_i + 1]
            next_x = offset_x + next_cell.x * cell_size + cell_size // 2
            next_y = offset_y + next_cell.y * cell_size + cell_size // 2
            pygame.draw.line(screen, (255, 255, 0), (center_x, center_y), (next_x, next_y), 2)
    
    def is_finished(self):
        if not self.solution_path:
            return False
        return self.current_i >= len(self.solution_path) - 1