class ChaosGame:
    """
    The Chaos Game as termed by Michael F. Barnsley is a game in which the starting position is chosen at random
    inside a polygon. A vertex is then chosen at random and the midpoint between the starting position and the
    vertex is drawn. This new point then acts as the new starting position and the process is repeated.

    Rules:
        1 - Draw a polygon.
        2 - Pic a point at random from inside the polygon, this will become the current point.
        3 - Choose at random a vertex of the polygon.
        4 - Draw the midpoint between the chosen vertex and the current point.
        5 - Repeat step 3 where the midpoint becomes the new current point.

    In some cases extra restrictions can be put in place to varying effects. For example in the case of using
    a square as the starting geometry it is necessary to restrict the randomly chosen vertex such that the chosen
    must not be equal to its predecessor.

    The list of restrictions implemented are as follows:

        r0 - apply no restrictions.
        r1 - prevent chosen vertex being equal to its predecessor.
        r2 - prevent chosen vertex being one step away anti-clockwise and previous vertex.
        r3 - prevent chosen vertex being one step away clockwise from previous vertex.
        r4 - prevent chosen vertex being neighbours with the previous if the previous two vertices match.

    The ratio of the distance to travel before marking a point can be controlled with the ratio parameter. This
    is defaulted to 1/2.

    There are other restrictions that can be put in place to create differing results. In addition, other ratios
    other than the midpoint can be used to find new points. More information can be found at...

    https://en.wikipedia.org/wiki/Chaos_game
    """

    def __init__(self, shape=3, rule="r0", ratio=1 / 2, *args, **kwargs):

        self.random = __import__("random")
        self.math = __import__("math")

        self.rule = rule
        self.ratio = ratio
        self.vertices = self._generate_polygon(shape)

        self.shape = shape
        self.start = self._random_start_point()
        self.points = []

    def _generate_polygon(self, no_of_vertices):
        """
        Method used to generate regular polygons based on the number of vertices. Accomplishes this by
        rotating the point (0, 1) around at intervals determined by the number of vertices.

        :param no_of_vertices: The number of vertices needed to generate polygon.
        
        :return vertices: The vertices of the boundary.
        """
        radians = 2 * self.math.pi / no_of_vertices

        x0, y0 = 0, 1
        vertices = [(x0, y0)]

        for vertex in range(1, no_of_vertices):
            x = x0 * self.math.cos(vertex * radians) - y0 * self.math.sin(vertex * radians)
            y = y0 * self.math.cos(vertex * radians) - x0 * self.math.sin(vertex * radians)

            vertices.append((round(x, 2), round(y, 2)))

        return vertices

    def _get_mid_point(self, point_a, point_b):
        """
        Method to get the midpoint between two points.

        :param point_a: The first point x1, y1.
        :param point_b: The second point x2, y2.

        :return: the midpoint xm, ym.
        """
        x_mid = (point_a[0] + point_b[0]) * self.ratio
        y_mid = (point_a[1] + point_b[1]) * self.ratio

        return x_mid, y_mid

    def _random_start_point(self):
        """
        Method that generates a random starting position inside the bounds of the shape.

        ### Currently is not properly implemented as it does not implement functionality to generate point within
        bounds of shape. It just generates a point within a small square situated in the center of the polygon. This
        has no dramatic effect on the end result except to not properly demonstrate the validity that any point may
        have the same effect ###

        :return: x, y coordinates.
        """
        x = y = self.random.random() * (0.5 - -0.5) + -0.5

        return x, y

    def _r0_play(self, iterations):
        """
        Will pick a random vertex of the triangle and draw the midpoint between the current point and the vertex.
        Midpoints are added to the list of points.

        :param iterations: The number of rounds to play the game.
        """
        new_point = self.start

        for _ in range(iterations):
            random_index = self.random.randint(0, self.shape - 1)
            bound_point = self.vertices[random_index]

            new_point = self._get_mid_point(new_point, bound_point)
            self.points.append(new_point)

    def _r1_play(self, iterations):
        """
        Will pick a random vertex and draw the midpoint between the current point and the vertex.
        The additional constraint is added as such that the next vertex picked may not be the same as the previous.
        Midpoints are added to the list of points.

        :param iterations: The number of rounds to play the game.
        """
        new_point = self.start
        random_index, prev_index = self.random.randint(0, self.shape - 1), -2

        for _ in range(iterations):

            random_index = self.random.randint(0, self.shape - 1)
            while random_index == prev_index:
                random_index = self.random.randint(0, self.shape - 1)

            bound_point = self.vertices[random_index]

            new_point = self._get_mid_point(new_point, bound_point)
            prev_index = random_index

            self.points.append(new_point)

    def _r2_play(self, iterations, clockwise=False):
        """
        Will pick a random vertex and draw the midpoint between the current point and the vertex.
        The additional constraint is added as such that the next vertex picked may not one step away from the previous.
        Midpoints are added to the list of points.

        :param iterations: The number of rounds to play the game.
        :param clockwise: Whether the clockwise neighbor is to be prevented or not.
        """
        new_point = self.start
        random_index, prev_index = self.random.randint(0, self.shape - 1), -2

        for _ in range(iterations):

            random_index = self.random.randint(0, self.shape - 1)
            if clockwise:
                while random_index == (prev_index + 1) % self.shape:
                    random_index = self.random.randint(0, self.shape - 1)
            else:
                while random_index == (prev_index - 1) % self.shape:
                    random_index = self.random.randint(0, self.shape - 1)

            bound_point = self.vertices[random_index]

            new_point = self._get_mid_point(new_point, bound_point)
            prev_index = random_index

            self.points.append(new_point)

    def _r4_play(self, iterations):
        """
        Will pick a random vertex and draw the midpoint between the current point and the vertex.
        The additional constraint is added as such that the next vertex picked may not one step away from the previous
        if the two previous vertices match. Midpoints are added to the list of points.

        :param iterations: The number of rounds to play the game.
        """
        new_point = self.start
        prev = [-2, -1]
        for _ in range(iterations):
            random_index = self.random.randint(0, self.shape - 1)

            if prev[-1] == prev[-2]:
                while random_index == (prev[-1] - 1) % self.shape or random_index == (prev[-1] + 1) % self.shape:
                    random_index = self.random.randint(0, self.shape - 1)

            bound_point = self.vertices[random_index]

            new_point = self._get_mid_point(new_point, bound_point)
            prev[-2], prev[-1] = prev[-1], random_index

            self.points.append(new_point)

    def play(self, iterations=1000):
        """
        Method to begin playing the Chaos Game. The game will be played by different rules based on the starting
        geometry of the boundary.

        :param iterations: The number of rounds to play the game.
        """
        if self.rule == "r0":
            self._r0_play(iterations)

        elif self.rule == "r1":
            self._r1_play(iterations)

        elif self.rule == "r2":
            self._r2_play(iterations)

        elif self.rule == "r3":
            self._r2_play(iterations, clockwise=True)

        elif self.rule == "r4":
            self._r4_play(iterations)


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # from tqdm import tqdm
    # from matplotlib import animation
    #
    # def get_next_game():
    #
    #     for i in tqdm(range(30, 71)):
    #         game = ChaosGame(shape=5, rule="r4", ratio=1 - i/100)
    #         game.play(100_000)
    #
    #         yield game
    #
    # def update(i):
    #     game = next(games)
    #     ax.clear()
    #     ax.axis("off")
    #     ax.grid(b=None)
    #
    #     ax.scatter([x for x, _ in game.points],
    #                [y for _, y in game.points],
    #                0.01,
    #                color="black")
    #
    #
    # fig, ax = plt.subplots(figsize=(5, 5))
    # ax.set_aspect('equal', adjustable='box')
    # games = get_next_game()
    #
    # ani = animation.FuncAnimation(fig, update, frames=101, interval=50)
    # ani.save("make_a_wish.gif", writer="pillow")

    game = ChaosGame(shape=5, rule="r4", ratio=.5)
    game.play(100_000)

    plt.scatter([x for x, _ in game.points],
                [y for _, y in game.points],
                0.01,
                color="black")
    plt.plot([x for x, _ in game.vertices] + [game.vertices[0][0]],
             [y for _, y in game.vertices] + [game.vertices[0][1]], color="red")
    plt.scatter(game.start[0], game.start[1], 24, color="green")
    plt.gca().set_aspect('equal', adjustable='box')

    plt.show()
