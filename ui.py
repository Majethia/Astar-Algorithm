# TO DO
# Drag to create obstacles
# Input board size
# Bug: with updating best path
# Bug: bottom right to top left does not work



from grid import Grid, Node
import random
import pygame
import sys

BLACK = (0, 0, 0)
GREY = (96, 96, 96)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600

BOARD = int(input("SIZE OF THE GRID: "))

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
        x = self.x * WINDOW_HEIGHT / BOARD
        y = self.y * WINDOW_HEIGHT / BOARD
        rectangle = pygame.Rect(x, y, WINDOW_HEIGHT / BOARD, WINDOW_HEIGHT / BOARD)
        rectangle1 = pygame.Rect(x+2, y+2, WINDOW_HEIGHT / BOARD - 4, WINDOW_HEIGHT / BOARD - 4)

        pygame.draw.rect(SCREEN, BLACK, rectangle)
        pygame.draw.rect(SCREEN, self.color, rectangle1)





def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(WHITE)


    grid = Grid(BOARD, BOARD, (0, 0), (BOARD - 1, BOARD -1), [])
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                x, y = pos[0]//(WINDOW_HEIGHT/BOARD), pos[1]//(WINDOW_HEIGHT/BOARD)
                x = int(x)
                y = int(y)
                if event.button == 1:
                    grid.start = grid.grid[x][y]
                if event.button == 3:
                    grid.goal = grid.grid[x][y]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run = False

        for i in range(BOARD):
            for j in range(BOARD):
                n = UI_Node(grid.grid[i][j])
                if grid.grid[i][j].obstacle:
                    n.color = GREY
                if grid.grid[i][j] == grid.start:
                    n.color = PURPLE
                if grid.grid[i][j] == grid.goal:
                    n.color = BLUE
                elif grid.grid[i][j] in grid.open_list:
                    n.color = GREEN
                elif grid.grid[i][j] in grid.closed_list:
                    n.color = RED
                n.draw(SCREEN)

        pygame.display.update()


    run = True
    while run:
        for i in range(BOARD):
            for j in range(BOARD):
                n = UI_Node(grid.grid[i][j])
                if grid.grid[i][j].obstacle:
                    n.color = GREY
                if grid.grid[i][j] == grid.start:
                    n.color = PURPLE
                if grid.grid[i][j] == grid.goal:
                    n.color = BLUE
                elif grid.grid[i][j] in grid.open_list:
                    n.color = GREEN
                elif grid.grid[i][j] in grid.closed_list:
                    n.color = RED

                n.draw(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run = False
                elif event.key == pygame.K_r:
                    for i in range(random.randint(100, 150)):
                        grid.grid[random.randint(1, BOARD-2)][random.randint(1, BOARD-2)].obstacle = True
                    run = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x, y = pos[0]// (WINDOW_HEIGHT/BOARD), pos[1]// (WINDOW_HEIGHT/BOARD)
                x = int(x)
                y = int(y)
                if grid.grid[x][y].obstacle == True:
                    grid.grid[x][y].obstacle = False
                else:
                    grid.grid[x][y].obstacle = True
                    

        pygame.display.update()
            


    grid.open_list.append(grid.start)


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
                if grid.grid[i][j] == grid.start:
                    n.color = PURPLE
                if grid.grid[i][j] == grid.goal:
                    n.color = BLUE
                elif grid.grid[i][j] in grid.open_list:
                    n.color = GREEN
                elif grid.grid[i][j] in grid.closed_list:
                    n.color = RED

                n.draw(SCREEN)

        # for i in grid.open_list:
        #     print(i)
        # print("------------------------------------------------")
        if not grid.open_list:
            break
        current = min(grid.open_list)
        # print("Chosen: ", current)
        # print("------------------------------------------------")
        grid.open_list.remove(current)
        grid.closed_list.append(current)
        
        if current == grid.goal:
            p = grid.goal.previous
            n = UI_Node(grid.goal, PURPLE)
            n.draw(SCREEN)
            while p:
                n = UI_Node(p, PURPLE)
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
