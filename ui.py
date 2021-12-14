from grid import Grid, Node

import pygame
import sys

BLACK = (0, 0, 0)
GREY = (96, 96, 96)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400

BOARD = 20

class UI_Node():
    def __init__(self, n: Node, color = (255, 255, 255)):
        self.x = n.x
        self.y = n.y
        self.g = n.g
        self.h = n.h
        self.obstacle = n.obstacle
        self.previous = n.previous
        self.color = color

    def draw(self, SCREEN):
        x = self.x * 20
        y = self.y * 20
        rectangle = pygame.Rect(x, y, 20, 20)
        rectangle1 = pygame.Rect(x+2, y+2, 16, 16)

        pygame.draw.rect(SCREEN, BLACK, rectangle)
        pygame.draw.rect(SCREEN, self.color, rectangle1)





def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(WHITE)

    obs = []
    for i in range(18):
        obs.append((8, i+2))
    grid = Grid(BOARD, BOARD, (0, 0), (BOARD - 1, BOARD -1), obs)
    while True:
        CLOCK.tick(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for i in range(BOARD):
            for j in range(BOARD):
                n = UI_Node(grid.grid[i][j])
                if grid.grid[i][j].obstacle:
                    n.color = GREY
                elif grid.grid[i][j] in grid.open_list:
                    n.color = GREEN
                elif grid.grid[i][j] in grid.closed_list:
                    n.color = RED

                n.draw(SCREEN)

        # for i in grid.open_list:
        #     print(i)
        # print("------------------------------------------------")
        current = min(grid.open_list)
        # print("Chosen: ", current)
        # print("------------------------------------------------")
        grid.open_list.remove(current)
        grid.closed_list.append(current)
        
        if current == grid.goal:
            p = grid.goal.previous
            n = UI_Node(grid.goal, YELLOW)
            n.draw(SCREEN)
            while p:
                n = UI_Node(p, YELLOW)
                n.draw(SCREEN)
                p = p.previous
            pygame.display.update()
            break

        neighbours = grid.find_surroundings(current)
        for i in neighbours:
            i.previous = current
            i.calc_h(grid.goal)
            i.calc_g()
            i.calc_f()
            if i not in grid.open_list:
                grid.open_list.append(i)


        pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


main()


# p = grid.goal
# while p:
#     print(p)
#     p = p.previous
