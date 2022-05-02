import math
from numba import jit
import numpy as np


def convert_coordinates(point, dispY):
    return int(point[0]), int(dispY - point[1])


class FastFunctions():
    def __init__(self):
        # dummy calls to compile
        convert_coordinates((0, 0), 100)
        self.ficks((0, 0), (1, 1), 60, 0.1)
        self.get_concentration_array((5, 5), (1, 1), 5, 0.1)
        self.gray(np.array([[1, 2, 3], [4, 5, 6]]))

    @staticmethod
    @jit(nopython=True)
    def ficks(point, origin, t, D):
        l2 = (point[0] - origin[0]) ** 2 + (point[1] - origin[1]) ** 2
        if t == 0:
            return 255
        else:
            return int((60 / (math.sqrt(12.56 * D * t))) * np.exp(-l2 / (4 * D * t)))

    @jit(nopython=True)
    def get_concentration_array(self, concentration_function, shape, origin, t, D):
        rows, columns = shape
        alphaArr = np.zeros((rows, columns), dtype=np.int32)
        for i in range(rows):
            for j in range(columns):
                point_conc = 255 - concentration_function((i / rows, j / columns), origin, t, D)
                if point_conc < 0:
                    alphaArr[i, j] = 0
                else:
                    alphaArr[i, j] = point_conc
        return alphaArr

    @staticmethod
    @jit(nopython=True)
    def gray(im):
        w, h = im.shape
        ret = np.empty((w, h, 3), dtype=np.uint8)
        ret[:, :, 2] = ret[:, :, 1] = ret[:, :, 0] = im
        return ret
