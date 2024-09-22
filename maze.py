class Maze:
    def __init__(self, matrix):
        self.matrix = matrix
        # self.graph = self._generate_graph()
        # self.route_map = self._get_route_map()
        # self.get_available_points(1, 1, 5)

    def _generate_graph(self):
        n = len(self.matrix)
        m = len(self.matrix[0])
        result = [[0 for j in range(m)] for i in range(n)]
        for i in range(n):
            for j in range(m):
                if self.matrix[i][j] == 0:
                    continue

                if j > 0 and self.matrix[i][j - 1] == 1:
                    result[i * m + j][i * m + j - 1] = 1
                if j == 0 and self.matrix[i][m - 1] == 1:
                    result[i * m + j][i * m + m - 1] = 1
                if j < m - 1 and self.matrix[i][j + 1] == 1:
                    result[i * m + j][i * m + j + 1] = 1
                if j == m - 1 and self.matrix[i][0] == 1:
                    result[i * m + j][i * m] = 1

                if i > 0 and self.matrix[i - 1][j] == 1:
                    result[i * m + j][(i - 1) * m + j] = 1
                if i == 0 and self.matrix[n - 1][j] == 1:
                    result[i * m + j][(n - 1) * m + j] = 1
                if i < n - 1 and self.matrix[i + 1][j] == 1:
                    result[i * m + j][(i + 1) * m + j] = 1
                if i == n - 1 and self.matrix[0][j] == 1:
                    result[i * m + j][j] = 1

    def _get_route_map(self):
        n = len(self.matrix)
        m = len(self.matrix[0])
        result = [[[] for _ in range(n * m)] for _ in range(n * m)]
        for i_start in range(n):
            for j_start in range(m):
                print(i_start, j_start)
                for i_end in range(n):
                    for j_end in range(m):
                        if (self.matrix[i_start][j_start] == 1 and self.matrix[i_end][j_end] == 1
                                and not result[self.code_point(i_start, j_start)][self.code_point(i_end, j_end)]):
                            r_fwd = self._calc_route(i_start, j_start, i_end, j_end)
                            r_bwd = list(reversed(r_fwd))[1:].append(self.code_point(i_end, j_end)) if r_fwd else None
                            result[self.code_point(i_start, j_start)][self.code_point(i_end, j_end)] = r_fwd
                            result[self.code_point(i_end, j_end)][self.code_point(i_start, j_start)] = r_bwd
        return result

    def _calc_route(self, i_start, j_start, i_end, j_end):
        n = len(self.matrix)
        m = len(self.matrix[0])

        route = []
        steps = [[0 for j in range(m)] for i in range(n)]

        def _depth_search(i, j, optimal_route):
            if len(route) + 1 >= len(optimal_route) and len(optimal_route) != 0:
                return optimal_route
            if not (i == i_start and j == j_start):
                route.append(self.code_point(i, j))
            if i == i_end and j == j_end and (len(route) < len(optimal_route) or len(optimal_route) == 0):
                optimal_route.clear()
                optimal_route.extend(route)
                if route:
                    del route[-1]
                return optimal_route
            steps[i][j] = 1

            if j > 0 and self.matrix[i][j - 1] == 1 and steps[i][j - 1] != 1:
                _depth_search(i, j - 1, optimal_route)
            if j == 0 and self.matrix[i][m - 1] == 1 and steps[i][m - 1] != 1:
                _depth_search(i, m - 1, optimal_route)
            if j < m - 1 and self.matrix[i][j + 1] == 1 and steps[i][j + 1] != 1:
                _depth_search(i, j + 1, optimal_route)
            if j == m - 1 and self.matrix[i][0] == 1 and steps[i][0] != 1:
                _depth_search(i, 0, optimal_route)

            if i > 0 and self.matrix[i - 1][j] == 1 and steps[i - 1][j] != 1:
                _depth_search(i - 1, j, optimal_route)
            if i == 0 and self.matrix[n - 1][j] == 1 and steps[n - 1][j] != 1:
                _depth_search(n - 1, j, optimal_route)
            if i < n - 1 and self.matrix[i + 1][j] == 1 and steps[i + 1][j] != 1:
                _depth_search(i + 1, j, optimal_route)
            if i == n - 1 and self.matrix[0][j] == 1 and steps[0][j] != 1:
                _depth_search(0, j, optimal_route)
            steps[i][j] = 0
            if route:
                del route[-1]

            return optimal_route

        def _breadth_search():
            queue = [self.code_point(i_start, j_start)]
            routes = {self.code_point(i_start, j_start): []}
            steps[i_start][j_start] = 1
            while queue:
                for point in queue[:]:
                    i, j = self.decode_point(point)
                    if i == i_end and j == j_end:
                        queue = []
                        break
                    new_points = []
                    if j > 0 and self.matrix[i][j - 1] == 1 and steps[i][j - 1] != 1:
                        steps[i][j - 1] = 1
                        encoded_point = self.code_point(i, j - 1)
                        new_points.append(encoded_point)
                    if j == 0 and self.matrix[i][m - 1] == 1 and steps[i][m - 1] != 1:
                        steps[i][m - 1] = 1
                        encoded_point = self.code_point(i, m - 1)
                        new_points.append(encoded_point)
                        # queue.append(encoded_point)
                    if j < m - 1 and self.matrix[i][j + 1] == 1 and steps[i][j + 1] != 1:
                        steps[i][j + 1] = 1
                        encoded_point = self.code_point(i, j + 1)
                        new_points.append(encoded_point)
                    if j == m - 1 and self.matrix[i][0] == 1 and steps[i][0] != 1:
                        steps[i][0] = 1
                        encoded_point = self.code_point(i, 0)
                        new_points.append(encoded_point)

                    if i > 0 and self.matrix[i - 1][j] == 1 and steps[i - 1][j] != 1:
                        steps[i - 1][j] = 1
                        encoded_point = self.code_point(i - 1, j)
                        new_points.append(encoded_point)
                    if i == 0 and self.matrix[n - 1][j] == 1 and steps[n - 1][j] != 1:
                        steps[n - 1][j] = 1
                        encoded_point = self.code_point(n - 1, j)
                        new_points.append(encoded_point)
                    if i < n - 1 and self.matrix[i + 1][j] == 1 and steps[i + 1][j] != 1:
                        steps[i + 1][j] = 1
                        encoded_point = self.code_point(i + 1, j)
                        new_points.append(encoded_point)
                    if i == n - 1 and self.matrix[0][j] == 1 and steps[0][j] != 1:
                        steps[0][j] = 1
                        encoded_point = self.code_point(0, j)
                        new_points.append(encoded_point)

                    queue.extend(new_points)
                    queue.remove(point)
                    for np in new_points:
                        routes[np] = routes.get(point) + [np]
                    del routes[point]
            return routes[self.code_point(i_end, j_end)]

        # return _depth_search(i_start, j_start, [])
        return _breadth_search()

    def get_available_points(self, i_start, j_start, block_point_i, block_point_j, depth, skip_depth):
        result = []
        n = len(self.matrix)
        m = len(self.matrix[0])
        steps = [[0 for j in range(m)] for i in range(n)]
        steps[i_start][j_start] = 1
        if block_point_i >= 0 and block_point_j >= 0 and block_point_i < n and block_point_j < m:
            steps[block_point_i][block_point_j] = 1
        queue = [self.code_point(i_start, j_start)]
        for d in range(depth):
            for p in queue[:]:
                i, j = self.decode_point(p)
                new_points = []
                if j > 0 and self.matrix[i][j - 1] == 1 and steps[i][j - 1] != 1:
                    steps[i][j - 1] = 1
                    encoded_point = self.code_point(i, j - 1)
                    new_points.append(encoded_point)
                if j == 0 and self.matrix[i][m - 1] == 1 and steps[i][m - 1] != 1:
                    steps[i][m - 1] = 1
                    encoded_point = self.code_point(i, m - 1)
                    new_points.append(encoded_point)
                    # queue.append(encoded_point)
                if j < m - 1 and self.matrix[i][j + 1] == 1 and steps[i][j + 1] != 1:
                    steps[i][j + 1] = 1
                    encoded_point = self.code_point(i, j + 1)
                    new_points.append(encoded_point)
                if j == m - 1 and self.matrix[i][0] == 1 and steps[i][0] != 1:
                    steps[i][0] = 1
                    encoded_point = self.code_point(i, 0)
                    new_points.append(encoded_point)

                if i > 0 and self.matrix[i - 1][j] == 1 and steps[i - 1][j] != 1:
                    steps[i - 1][j] = 1
                    encoded_point = self.code_point(i - 1, j)
                    new_points.append(encoded_point)
                if i == 0 and self.matrix[n - 1][j] == 1 and steps[n - 1][j] != 1:
                    steps[n - 1][j] = 1
                    encoded_point = self.code_point(n - 1, j)
                    new_points.append(encoded_point)
                if i < n - 1 and self.matrix[i + 1][j] == 1 and steps[i + 1][j] != 1:
                    steps[i + 1][j] = 1
                    encoded_point = self.code_point(i + 1, j)
                    new_points.append(encoded_point)
                if i == n - 1 and self.matrix[0][j] == 1 and steps[0][j] != 1:
                    steps[0][j] = 1
                    encoded_point = self.code_point(0, j)
                    new_points.append(encoded_point)

                queue.extend(new_points)
                queue.remove(p)
                if d >= skip_depth:
                    result.extend(new_points)
        return result

    def code_point(self, i, j):
        return i * len(self.matrix[0]) + j

    def decode_point(self, value):
        return value // len(self.matrix[0]), value % len(self.matrix[0])


if __name__ == '__main__':
    maze = Maze([
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ])
