class Node:
    def __init__(self, x = 0, y = 0, g = float('inf'), h = 0, obstacle = False, previous = None):
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.f = self.g + self.h
        self.obstacle = obstacle
        self.previous = previous

    def calc_g(self):
        if self.previous == None:
            self.g = float('inf')
            return
        elif self.previous.x == self.x or self.previous.y == self.y:
            g = 10
        else:
            g = 14
        self.g = g + self.previous.g

    def calc_h(self, goal):
        x = abs(goal.x - self.x)
        y = abs(goal.y - self.y)
        m = (min(x, y), max(x, y))
        self.h = (m[0] * 14) + ((m[1] - m[0]) * 10)

    def calc_f(self):
        self.f = self.g + self.h
        return self.f

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
        self.start.g = 0
        self.start.f = 0
        self.goal = self.grid[goal[0]][goal[1]]
        

    def find_surroundings(self, current: Node):
        sr = []
        closed_set = set(self.closed_list)
        deltas = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        
        for dx, dy in deltas:
            new_x, new_y = current.x + dx, current.y + dy
            if 0 <= new_x < self.rows and 0 <= new_y < self.cols:
                neighbor = self.grid[new_x][new_y]
                if neighbor.obstacle:
                    continue
                if neighbor in closed_set:
                    continue
                sr.append(neighbor)
        
        return sr


    def __str__(self) -> str:
        res = ""
        for i in range(self.rows):
            for j in range(self.cols):
                res += f"{self.grid[i][j].__str__()}\n"
        return res
