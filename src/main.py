import pygame
from maze import Maze
from player import Player
from solver import Solver
from smarty_pants import Smartypants

# Pygame setup
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1440, 900))
clock = pygame.time.Clock()
running = True

# Sounds
wall_hitting_sound = pygame.mixer.Sound("assets\sounds\wall_hit_sound.wav")

# Create Maze
maze = Maze(15, 15)
maze.generate_maze()

# Solve Maze
solver = Solver(maze)
solution_path = solver.solve()

# Player Racer
player = Player(maze.start.x, maze.start.y)

# AI Racer
smarty = Smartypants(maze, solver)

while running:
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if player.check_wall_collisions(0, maze):
                    player.move_player(0)
                else:
                    wall_hitting_sound.play()
            elif event.key == pygame.K_RIGHT:
                if player.check_wall_collisions(1, maze):
                    player.move_player(1)
                else:
                    wall_hitting_sound.play()
            elif event.key == pygame.K_DOWN:
                if player.check_wall_collisions(2, maze):
                    player.move_player(2)
                else:
                    wall_hitting_sound.play()
            elif event.key == pygame.K_LEFT:
                if player.check_wall_collisions(3, maze):
                    player.move_player(3)
                else:
                    wall_hitting_sound.play()
    
    smarty.update(current_time)
    screen.fill("white")
    maze.draw_maze(screen)
    maze.draw_second_maze(screen)    
    solver.draw_solution(screen, maze.second_maze_offset_x, maze.second_maze_offset_y)
    player.draw_player(screen, maze)    
    smarty.draw(screen, maze.second_maze_offset_x, maze.second_maze_offset_y)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()