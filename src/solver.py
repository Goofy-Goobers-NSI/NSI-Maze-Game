import pygame
from maze import N, E, S, W, DX, DY

class Solver:
    def __init__(self, maze):
        self.maze = maze
        self.solution_path = []
        self.visited = set()

    def solve(self):
        start = self.maze.start
        end = self.maze.end
        self.dfs(start, end, [])
        return self.solution_path
    
    def dfs(self, current_cell, target_cell, current_path):
        # If the cell has already been visited
        if current_cell in self.visited:
            return False
        
        self.visited.add(current_cell)
        current_path.append(current_cell)

        # Check if target reached, record path
        if current_cell == target_cell:
            self.solution_path = current_path.copy()
            return True

        directions = [N, E, S, W]
        # Explore each direction
        for dir in directions:
            # If there's a wall, skip this direction
            if current_cell.walls[dir]:
                continue
            if current_cell.walls[dir] == False:
                ny = current_cell.y + DY[dir]
                nx = current_cell.x + DX[dir]
            
            # Check if the next cell is within bounds
            if nx < 0 or nx >= self.maze.largeur or ny < 0 or ny >= self.maze.hauteur:
                continue
            
            # Get the neighbouring cell
            neighbour = self.maze.grille[nx][ny]
            
            # If the neighbour has not been visited, continue the DFS
            if self.dfs(neighbour, target_cell, current_path):
                return True
            
        # If no path found, backtrack
        current_path.pop()
        return False


    def draw_solution(self, screen, offset_x, offset_y):
        # Gonna remove this method once the evil Ai is created            
        for i in range(len(self.solution_path) - 1):
            current = self.solution_path[i]
            next_cell = self.solution_path[i + 1]
            
            # Offsets of solution path
            x1 = offset_x + current.x * self.maze.cell_size + self.maze.cell_size // 2
            y1 = offset_y + current.y * self.maze.cell_size + self.maze.cell_size // 2
            x2 = offset_x + next_cell.x * self.maze.cell_size + self.maze.cell_size // 2
            y2 = offset_y + next_cell.y * self.maze.cell_size + self.maze.cell_size // 2
            
            pygame.draw.line(screen, (0, 255, 0), (x1, y1), (x2, y2), 3)
            pygame.draw.circle(screen, (0, 200, 0), (x1, y1), 5)