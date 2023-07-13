import numba as nb
import numpy as np
import timeit

@nb.njit(parallel=True, cache=True)
def update_ranges(arr, rad:int):
    num = len(arr[:, 0])
    for i in nb.prange(num):
        if arr[i, 0] == 0:  # Base
            arr[i, 1] = 100
        else:  # Plane beacon or enemy
            min_dist = 1000000000
            arr[i, 1] = 0
            for j in nb.prange(num):
                dist = np.sqrt((arr[i, 2] - arr[j, 2])**2 + (arr[i, 3] - arr[j, 3])**2)
                if dist < rad and arr[j, 1] > arr[i, 1] and arr[j, 0] < 2.5:
                    arr[i, 1] = arr[j, 1] - 1
                if 0 < dist < min_dist and arr[j, 0] < 2 and arr[j, 1] > 1:
                    arr[i, 4] = arr[j, 2]
                    arr[i, 5] = arr[j, 3]
                    min_dist = dist
    return arr


def update_ranges_stock(arr, rad):
    for i, row in enumerate(arr):
        if row[0] == 0:  # Base
            arr[i, 1] = 3
        else:  # Plane beacon or enemy
            min_index = i
            min_dist = 1000000000
            arr[i, 1] = 0
            for j, row2 in enumerate(arr):
                dist = np.sqrt((arr[i, 2] - arr[j, 2])**2 + (arr[i, 3] - arr[j, 3])**2)
                if dist < rad and arr[j, 1] > arr[i, 1]:
                    arr[i, 1] = arr[j, 1] - 1
                if 0 < dist < min_dist and arr[j, 0] < 2:
                    min_index = j
                    min_dist = dist
            arr[i, 4:6] = arr[min_index, 2:4]

    return arr


if __name__ == '__main__':
    clock = timeit.default_timer
    array = np.array(((0, 90, 0, 0, 500, 500, 0),
                      (1, 0, 60, 100, 500, 500, 0),
                      (1, 0, 40, 50, 500, 500, 0),
                      (1, 0, 100, 30, 500, 500, 0),
                      (1, 0, 20, 100, 500, 500, 0),
                      (1, 0, 100, 140, 500, 500, 0),
                      (1, 0, 150, 100, 500, 500, 0),
                      (1, 0, 100, 200, 500, 500, 0),
                      (2, 0, 300, 100, 500, 500, 0),
                      (2, 0, 400, 100, 500, 500, 0),
                      (2, 0, 500, 100, 500, 500, 0),
                      (2, 0, 100, 600, 500, 500, 0),
                      (2, 0, 700, 100, 500, 500, 0),
                      (2, 0, 100, 700, 500, 500, 0),
                      (2, 0, 100, 700, 500, 500, 0),
                      (2, 0, 100, 700, 500, 500, 0)), dtype=float)
    update_ranges(array, 10)
    start = clock()
    for i in range(500):
        ret = update_ranges(array, 400)
    end = clock()
    for i in range(500):
        ret2 = update_ranges_stock(array, 400)
    end2 = clock()
    print(end-start)
    print(end2 - end)
    print(ret - ret2)
    print(ret2)
