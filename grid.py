class Node:
    def __init__(self, x = 0, y = 0, g = 0, h = 0, obstacle = False, previous = None):
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.f = self.g + self.h
        self.obstacle = obstacle
        self.previous = previous

    def calc_g(self):
        if self.previous == None:
            self.g = 0
            return
        elif self.previous.x == self.x or self.previous.y == self.y:
            g = 10
        else:
            g = 15
        self.g = g + self.previous.g

    def calc_h(self, goal):
        x = goal.x - self.x
        y = goal.y - self.y
        m = (min(x, y), max(x, y))
        self.h = (m[0] * 14) + ((m[1] - m[0]) * 10)

    def calc_f(self):
        self.f = self.g + self.h

    def __str__(self) -> str:
        return f"x pos: {self.x} :: y pos: {self.y} :: g cost: {self.g} :: h cost {self.h} :: f cost {self.f} :: obstacle: {self.obstacle}"

    def __gt__(self, n):
        return self.f > n.f
    
    def __lt__(self, n):
        return self.f < n.f


class Grid:
    def __init__(self, rows: int, cols: int, start, goal, obstacles: list):
        self.rows = rows
        self.cols = cols
        self.obstacles = obstacles
        self.grid = []
        self.open_list = []
        self.closed_list = []
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid.append([])
                if (i, j) in obstacles:
                    o = True
                else:
                    o = False
                n = Node(x = i, y = j, obstacle=o)
                n.calc_g()
                self.grid[i].append(n)
        self.start = self.grid[start[0]][start[1]]
        self.goal = self.grid[goal[0]][goal[1]]
        self.open_list.append(self.start)


    def find_surroundings(self, current: Node):
        sr = []
        if (current.x + 1) < self.rows and (current.y + 1) < self.cols:
            sr.append(self.grid[current.x + 1][current.y + 1])
        if (current.x + 1) < self.rows:
            sr.append(self.grid[current.x + 1][current.y])
        if (current.y + 1) < self.cols:
            sr.append(self.grid[current.x][current.y + 1])
        if (current.x - 1) > 0 and (current.y - 1) > 0:
            sr.append(self.grid[current.x - 1][current.y - 1])
        if (current.x - 1) > 0:
            sr.append(self.grid[current.x - 1][current.y])
        if (current.y - 1) > 0:
            sr.append(self.grid[current.x][current.y - 1])
        if (current.x - 1) > 0 and (current.y + 1) < self.cols:
            sr.append(self.grid[current.x - 1][current.y + 1])
        if (current.y - 1) > 0 and (current.x + 1) < self.rows:
            sr.append(self.grid[current.x + 1][current.y - 1]) 
        res_sr = []
        for i in sr:
            if i.obstacle:
                pass
            elif i in self.closed_list:
                pass
            else:
                res_sr.append(i)
        return res_sr


    def __str__(self) -> str:
        res = ""
        for i in range(self.rows):
            for j in range(self.cols):
                res += f"{self.grid[i][j].__str__()}\n"
        return res
