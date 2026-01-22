import pygame
import random
from maze import N, E, S, W, DX, DY

class Solver:
    def __init__(self, maze, difficulty="hard"):
        self.maze = maze
        self.solution_path = []
        self.visited = set()
        
        '''
        Difficulty Configuration
        m = max mistakes
        d = depth for mistakes
        gap = minimum steps between mistakes (cooldown essentially between mistakes)
        '''
        
        configs = {
            "easy":   {"m": (6, 8), "d": (5, 9), "gap": 5},
            "normal": {"m": (3, 5), "d": (3, 5), "gap": 12},
            "hard":   {"m": (0, 3), "d": (1, 5), "gap": 25}
        }
        
        conf = configs.get(difficulty.lower(), configs["normal"])
        self.max_mistakes = random.randint(conf["m"][0], conf["m"][1])
        self.depth_range = conf["d"]
        self.min_gap = conf["gap"]
        
        self.mistakes_made = 0
        self.steps_since_last_mistake = 0

    def solve(self):
        start = self.maze.start
        target = self.maze.end
        self.dfs(start, target)
        return self.solution_path
    
    def dfs(self, current, target):
        '''
        Docstring for dfs
        Depth-First Search with intentional mistake-making to simulate an imperfect solver.
        This method explores the maze recursively, making wrong turns based on the
        configured difficulty level.
        Args:
            current (Cell): The current cell being explored.
            target (Cell): The target cell to reach.
        Returns:
            bool: True if the target is reached, False otherwise.
        '''

        self.visited.add(current)
        self.solution_path.append(current)

        if current == target:
            return True

        directions = [N, E, S, W]
        random.shuffle(directions)

        for d in directions:
            # Prevents moving through walls
            if current.walls[d]:
                continue
            
            # Calculate neighbor coordinates
            nx = current.x + DX[d]
            ny = current.y + DY[d]

            # Also prevent moving through walls bounds but even more
            if not (0 <= nx < self.maze.largeur and 0 <= ny < self.maze.hauteur):
                continue
            
            # Get the neighbor cell
            neighbour = self.maze.grille[nx][ny]
            
            if neighbour not in self.visited:
                # Check if this neighbor is a mistake path
                if not self.can_reach_target(neighbour, target, self.visited.copy()):
                    
                    # Can a mistake be made now?
                    # if mistakes made < max mistakes AND steps since last mistake >= min gap
                    if self.mistakes_made < self.max_mistakes and self.steps_since_last_mistake >= self.min_gap:
                        self.mistakes_made += 1
                        self.steps_since_last_mistake = 0 # Reset spacing
                        
                        depth = random.randint(self.depth_range[0], self.depth_range[1])
                        self.make_mistake_trip(neighbour, depth)
                        
                        self.solution_path.append(current) # Backtrack to junction
                    continue 
                else:
                    # On the correct path, increment 
                    self.steps_since_last_mistake += 1
                    
                    if self.dfs(neighbour, target):
                        return True
        return False

    def make_mistake_trip(self, current, depth):
        """Standard depth-limited wander into a dead end."""
        # Limits depth of mistake
        if depth <= 0: 
            return None

        self.visited.add(current)
        self.solution_path.append(current)

        directions = [N, E, S, W]
        random.shuffle(directions)

        for d in directions:
            if current.walls[d]:
                continue
            nx = current.x + DX[d]
            ny = current.y + DY[d]
            if not (0 <= nx < self.maze.largeur and 0 <= ny < self.maze.hauteur):
                continue
            
            neighbour = self.maze.grille[nx][ny]
            if neighbour not in self.visited:
                self.make_mistake_trip(neighbour, depth - 1)
                self.solution_path.append(current) # Backtrack
                return None
    
    def can_reach_target(self, start_cell, target_cell, visited_cells):
        """
        Identifies dead ends by checking if the target cell is reachable from the start cell using DFS.
        params:
            start_cell (Cell): Cell to start search from
            target_cell (Cell): Cell to reach
            visited_cells (set): Cells already visited in the main DFS
        """

        # NSI class applies right here, I can't believe I actually found a use case for a stack in the maze game

        stack = [start_cell]
        while stack:
            current = stack.pop()
            if current == target_cell:
                return True
            visited_cells.add(current)

            for d in [N, E, S, W]:
                if not current.walls[d]:
                    nx = current.x + DX[d]
                    ny = current.y + DY[d]

                    if 0 <= nx < self.maze.largeur and 0 <= ny < self.maze.hauteur:
                        neighbor = self.maze.grille[nx][ny]
                        if neighbor not in visited_cells:
                            stack.append(neighbor)

        return False

    def draw_solution(self, screen, offset_x, offset_y):
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