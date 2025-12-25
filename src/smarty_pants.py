import pygame
import random
from maze import N, E, S, W, DX, DY

class Smartypants:
    def __init__(self, maze, solver):
        self.maze = maze
        self.solver = solver
        self.current_i = 0
        self.solution_path = solver.solution_path
        self.current_cell = self.solution_path[0]
        self.speed = 200 # milliseconds per move
        self.last_move_time = pygame.time.get_ticks()

        self.making_mistake = False
        self.mistake_path = []
        self.mistake_i = 0
        self.error_cooldown = 0

        self.mistakes_made = 0
        self.total_moves = 0

    def update(self,current_time):
        if not self.solution_path:
            return None
        
        if current_time - self.last_move_time < self.speed:
            return None
        
        self.last_move_time = current_time

        if self.making_mistake:
            self.follow_mistake_path()
        else:
            self.follow_solution_path()
        
        self.total_moves += 1

    def follow_solution_path(self, current_time):
        if self.current_i >= len(self.solution_path) - 1:
            self.current_cell = self.solution_path[-1]
            return None
        self.current_i += 1
        self.current_cell = self.solution_path[self.current_i]
        if current_time > self.error_cooldown and random.random() < 0.1 and self.current_i < len(self.solution_path) - 3:
            self.start_mistake()

    def start_mistake(self):
        self.making_mistake = True
        self.mistakes_made += 1

        self.mistake_path = []
        current = self.current_cell
        valid_directions = [N, E, S, W]

        if self.current_i < len(self.solution_path) - 1:
            next_cell = self.solution_path[self.current_ix + 1]
            dx = next_cell.x - current.x
            dy = next_cell.y - current.y
            good_dir = None
            for dir in valid_directions:
                if DX[dir] == dx and DY[dir] == dy:
                    good_dir = dir
                    break

            if good_dir is not None and good_dir in valid_directions:
                valid_directions.remove(good_dir)
            
        random.shuffle(valid_directions)
        mistake_found = False

        for dir in valid_directions:
            if not current.walls[dir]:
                ny = current.y + DY[dir]
                nx = current.x + DX[dir]
                if 0 <= nx < self.maze.largeur and 0 <= ny < self.maze.hauteur:
                    next_cell = self.maze.grille[nx][ny]
                    self.mistake_path.append(next_cell)
                    mistake_length = random.randint(1, 3)
                    # for _ in range(mistake_length - 1):
                    # continue in random valid directions
