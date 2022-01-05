class HilbertCurve:
    """
    The hilbert curve first conceptualised by David Hilbert is a curve in which a 1 dimensional curve can occupy a
    2 dimensional plane. In order to achieve a plane is subdivided into 4 sub-planes and the center of each is
    connected. each sub-plane is then broken into four additional sub-planes and the curve is copied into available
    new space. The bottom left and bottom right curves are then rotated clock-wise and anti-clockwise respectively,
    before having there endpoints joined to the start point of the curve in the next quadrant.

    Rules:
        1 - Divide square plane into 4 sub-planes.
        2 - Draw lines such the center of each sub-plane is connected.
        3 - Sub-divide each sub-plane into 4 smaller planes.
        4 - Copy the curve scaled to fit each new sub-plane.
        5 - Rotate the bottom left and bottom right curves.
        6 - Join the relevant points to connect the curves.
        7 - Repeat this process n times, where n is considered to be the order of the Pseudo Hilbert Curve

    In general a true Hilbert Curve can never be generated due to the finite limits placed on computation using a
    computer. A true Hilbert Curve would be the resulting curve as n -> inf. As n -> inf the resulting curve would
    occupy all the relevant space given to it inside a square.

    For our purposes a Pseudo Hilbert Curve may be produced such that n repetitions of the process occur generating
    an n order Pseudo Hilbert Curve. The total number of points mapped is equal to N^2 ; N = 2^n.
    """

    def __init__(self, order=3):

        self.N = 2**order
        self.points = [(0, 0)]

        for i in range(self.N * self.N):
            self.points.append(self._hilbert_curve_x2xy(i))

    @staticmethod
    def _bit_mask(x):
        """
        Static method used to bit mask the final least significant bits.

        :param x: The input bit string

        :return: The masked bit string
        """
        return x & 3

    def _hilbert_curve_x2xy(self, index):
        """
        Method for iteratively generating a coordinates of a Pseudo Hilbert Curve. Takes a 1 dimensional index and
        maps it to a 2 dimensional set of coordinates.

        :param index: The indexed position in 1 dimensional space ranging from 0 to N^2

        :return: a tuple containing the x, y coordinates in 2 dimensional space.
        """

        # initial starting coordinated of order 1 Hilbert curve
        positions = (0, 0), (0, 1), (1, 1), (1, 0)

        # gets initial position by masking index then bit shifts index
        tmp = positions[self._bit_mask(index)]
        index = index >> 2

        x, y = tmp[0], tmp[1]

        # loops to determine x, y coordinates based on next bit shifted index.
        n = 4
        while n <= self.N:
            n2 = n // 2

            i = self._bit_mask(index)
            if i == 0:
                x, y = y, x

            elif i == 1:
                x, y = x, y + n2

            elif i == 2:
                x, y = x + n2, y + n2

            elif i == 3:
                x, y = (2 * n2 - 1) - y, (n2 - 1) - x

            index = index >> 2
            n *= 2

        return x, y


class PeanoCurve:

    def __init__(self, order=3):
        self.N = 9**order
        self.points = [(0, 0)]
        self._generate_peano_curve(0)

    @staticmethod
    def _up(x, y):
        return x, y+1

    @staticmethod
    def _down(x, y):
        return x, y-1

    @staticmethod
    def _left(x, y):
        return x-1, y

    @staticmethod
    def _right(x, y):
        return x+1, y

    def _generate_peano_curve(self, index):

        coords = self.points[index]

        i0 = 0
        i1 = 0
        for index in range(self.N):

            if index == 30:
                return

            index %= 9
            print(index)

            if index == 0 or index == 1 or index == 6 or index == 7:
                if i1 % 2 == 0:
                    coords = self._up(*coords)
                    print("up")
                else:
                    coords = self._down(*coords)
                    print("down")
            elif index == 2 or index == 5:
                if i0 % 2 == 0:
                    coords = self._right(*coords)
                    print("right")
                else:
                    coords = self._left(*coords)
            elif index == 3 or index == 4:
                coords = self._down(*coords)
                print("down")



            elif index == 8:
                i0 += 1
                if i0 % 3 == 0:
                    i1 += 1
                    coords = self._right(*coords)
                else:
                    coords = self._up(*coords)

            self.points.append(coords)





class Dithering:

    def __init__(self, image, Curve):

        log2 = __import__("math").log2
        order = int(log2(image.shape[0]))

        self.curve = Curve(order)
        self.dithering(image)

    def dithering(self, image):

        hilbert_points = self.curve.points

        x_0, y_0 = hilbert_points[0]
        i_0 = image[y_0, x_0]
        o_0 = 0 if i_0 <= 0.5 else 1
        e = i_0 - o_0

        image[y_0, x_0] = o_0

        for x, y in hilbert_points[1:]:
            i = image[y, x]
            o = 0 if i + e <= 0.5 else 1
            e += i - o
            image[y, x] = o


if __name__ == "__main__":

    from matplotlib import image
    from matplotlib import pyplot as plt

    # img = image.imread("lenna.png")[:, :, 0]
    #
    # plt.imshow(img, cmap="gray")
    # plt.show()
    #
    # Dithering(img, HilbertCurve)
    # plt.imshow(img, cmap="gray")
    # plt.show()
    #
    # img.sort()
    # plt.imshow(img, cmap="gray")
    # plt.show()


    hilbert_curve = HilbertCurve(6)
    points = hilbert_curve.points
    #
    # peano_curve = PeanoCurve(2)
    # points = peano_curve.points

    xs = [x for x, _ in points]
    ys = [y for _, y in points]
    c = [i for i in range(len(xs))]

    cm = plt.get_cmap("hsv")
    fig = plt.figure(figsize=(5, 5))
    ax1 = plt.subplot(111)

    no_points = len(c)
    ax1.set_prop_cycle('color', [cm(1. * i / (no_points - 1)) for i in range(no_points - 1)])

    for i in range(no_points - 1):
        bar = ax1.plot(xs[i: i + 2], ys[i: i + 2])



    plt.show()


