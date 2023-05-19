class A_star_solver(object):
    def __init__(self, width=15, height=15):
        self.came_from = {}
        self.start_node_char = 3
        self.end_node_char = 2
        self.wall_char = 1
        self.open_list = []
        self.width = width
        self.height = height
        self.maze = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.f_vals = []
        self.g_vals = []
        self.path = []

    def calc_path(self, occupied_squares, move):
        """
        move: [(start row, start col), (end row, end col)]
        occipied squares: [(row, col) ... ] of squares where is chess piece
        return path in cnc coords (x, y)
        """
        move = [[round(move[0][0] * 2), round(move[0][1] * 2)], [round(move[1][0] * 2), round(move[1][1] * 2)]]
        self.__init_astar(occupied_squares, move)
        move = [[move[0][1], move[0][0]], [move[1][1], move[1][0]]]
        path = self.__solve(*move)
        path.append(tuple(move[0]))
        # path = self.solve([move[0][1] * 2, move[0][0] * 2], [move[1][1] *2, move[1][0] * 2])
        path.insert(0, tuple(move[1]))
        path.reverse()
        path = self.group_path(path)
        for i in range(len(path)):
            path[i] = (round(path[i][0] / 2, 1), round((14 - path[i][1]) / 2, 1))
        return path

    def __init_astar(self, occupied_squares, move):
        self.f_vals = [[float("inf") for _ in range(self.width)] for _ in range(self.height)]
        self.g_vals = [[float("inf") for _ in range(self.width)] for _ in range(self.height)]
        for row in range(self.height):
            for col in range(self.width):
                if (row / 2, col / 2) in occupied_squares:
                    self.maze[row][col] = self.wall_char
                else:
                    self.maze[row][col] = 0
                # print(self.maze[row][col], end = " ")
            # print()
        self.open_list = []
        self.came_from = {}
        self.path = []
        self.maze[move[0][0]][move[0][1]] = self.start_node_char
        self.maze[move[1][0]][move[1][1]] = self.end_node_char

        """for row in range(self.height):
            for col in range(self.width):
                print(self.maze[row][col], end=" ")
            print()"""

    def __solve(self, start_node, end_node):
        self.open_list.append(start_node)
        self.g_vals[start_node[1]][start_node[0]] = 0
        self.f_vals[start_node[1]][start_node[0]] = self.__shortest_path(start_node, end_node)

        while len(self.open_list) > 0:
            current = self.__get_lowest_f()
            if current == end_node:
                # return function to backtrack
                # print("found")
                self.path = self.__backtrack(tuple(current), self.came_from, tuple(start_node))
                return self.path
            self.open_list.remove(current)
            neighbours = self.__get_neighbours(current)

            for neighbour in neighbours:
                temp_gVal = self.g_vals[current[1]][current[0]] + self.__disatnce(current, neighbour)

                if temp_gVal < self.g_vals[neighbour[1]][neighbour[0]]:
                    self.came_from.update({tuple(neighbour): tuple(current)})
                    self.g_vals[neighbour[1]][neighbour[0]] = temp_gVal
                    self.f_vals[neighbour[1]][neighbour[0]] = temp_gVal + self.__shortest_path(neighbour, end_node)
                    if neighbour not in self.open_list:
                        self.open_list.append(neighbour)
        return None

    def __disatnce(self, current, neighbour):
        if current[0] != neighbour[0] and current[1] != neighbour[1]:
            return 14
        else:
            return 10

    def __backtrack(self, curr: tuple, came_from: dict, start_node: tuple):
        path = []
        current = came_from[curr]
        while current != start_node:
            path.append(current)
            current = came_from[current]
        return path

    def __shortest_path(self, start_node, end_node):
        path_cost = 0

        dx = abs(end_node[0] - start_node[0])
        dy = abs(end_node[1] - start_node[1])

        diagonal = min(dx, dy)
        horizontal = max(dx, dy) - diagonal
        path_cost += 14 * diagonal
        path_cost += 10 * horizontal
        return path_cost

    def __get_lowest_f(self):
        lowest = float("inf"), []
        for to_eval in self.open_list:
            if self.f_vals[to_eval[1]][to_eval[0]] <= lowest[0]:
                lowest = self.f_vals[to_eval[1]][to_eval[0]], to_eval
        return lowest[1]

    def __get_neighbours(self, node):
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (j == 0) and (i == 0):
                    continue
                x = node[0] + i
                y = node[1] + j
                if (-1 < x < self.width) and (-1 < y < self.height) and self.maze[y][x] != self.wall_char:
                    neighbours.append([x, y])
        return neighbours

    def group_path(self, path):
        new_path = []
        prev_dx, prev_dy = 0, 0
        for i in range(len(path) - 1):
            dx, dy = path[i][0] - path[i + 1][0], path[i][1] - path[i + 1][1]
            if dx == prev_dx and dy == prev_dy:
                continue
            else:
                new_path.append(path[i])
                prev_dx = dx
                prev_dy = dy
        new_path.append(path[-1])
        return new_path

    def draw_path(self, path):
        colors = ["#b2bec3", "#d63031", "#00b894"]
        surf = pygame.Surface((450, 450))
        surf.fill("#2d3436")
        for r in range(self.height):
            for c in range(self.width):
                if self.maze[r][c] != 0:
                    pygame.draw.rect(surf, colors[self.maze[r][c] - 1], (c * 30, r * 30, 30, 30))
        for p in path:
            pygame.draw.rect(surf, "#0984e3", (p[0] * 2 * 30, (7 - p[1])* 2 * 30, 30, 30))
        return surf


if __name__ == "__main__":
    import pygame

    pygame.init()
    win = pygame.display.set_mode((450, 450))

    solver = A_star_solver()
    filled = []
    for row in range(8):
        for col in range(8):
            if row in [6, 7, 0, 1]:
                filled.append((row, col))
    move = [(0, 6), (2, 5)]
    path = solver.calc_path(filled, move)
    print(path)
    path_vis = solver.draw_path(path)

    win.blit(path_vis, (0, 0))    
    pygame.display.flip()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
