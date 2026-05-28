import pygame

class Smartypants:
    def __init__(self, maze, solver, speed):
        self.maze = maze
        self.solver = solver
        self.current_i = 0
        self.solution_path = solver.solution_path
        self.current_cell = self.solution_path[0]
        self.speed = speed  # milliseconds per move
        self.last_move_time = pygame.time.get_ticks()
        self.px = None
        self.py = None
        self.interpolation_speed = 0.25

    def update(self, current_time):
        if not self.solution_path:
            return None
        
        if current_time - self.last_move_time < self.speed:
            return None
        
        self.last_move_time = current_time

        self.follow_solution_path()

    def follow_solution_path(self):
        if self.current_i >= len(self.solution_path) - 1:
            self.current_cell = self.solution_path[-1]
            return None
        
        self.current_i += 1
        self.current_cell = self.solution_path[self.current_i]

    def draw(self, screen, maze):
        if not self.current_cell:
            return
        
        cell_size = self.maze.cell_size
        target_x = maze.second_maze_offset_x + self.current_cell.x * cell_size + cell_size // 2
        target_y = maze.second_maze_offset_y + self.current_cell.y * cell_size + cell_size // 2

        if self.px is None or self.py is None or abs(self.px - target_x) > 100 or abs(self.py - target_y) > 100:
            self.px = target_x
            self.py = target_y

        self.px += (target_x - self.px) * self.interpolation_speed
        self.py += (target_y - self.py) * self.interpolation_speed

        if abs(target_x - self.px) < 0.1:
            self.px = target_x
        if abs(target_y - self.py) < 0.1:
            self.py = target_y

        # Blue normally
        color = (100, 100, 255)
        radius = cell_size // 3
        
        pygame.draw.circle(screen, color, (int(self.px), int(self.py)), radius)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.px), int(self.py)), radius, 2)
    
    def is_finished(self):
        if not self.solution_path:
            return False
        return self.current_i >= len(self.solution_path) - 1

    def smarty_win(self, maze):
        return self.current_cell.x == maze.end.x and self.current_cell.y == maze.end.y