from __future__ import division
import math
from PIL import Image
import numpy
import copy
from numba import cuda
import time


def to_greyscale(pix):
    for i, row in enumerate(pix):
        for j, column in enumerate(row):
            grey = (pix[i][j][0] * 0.299) + (pix[i][j][1] * 0.587) + (pix[i][j][2] * 0.114)
            pix[i][j][0] = grey
            pix[i][j][1] = grey
            pix[i][j][2] = grey
    return pix


@cuda.jit
def to_greyscale_cuda(pix, grey):
    x, y = cuda.grid(2)
    if x < pix.shape[0] and y < pix.shape[1]:
        grey_pixel = (pix[x, y, 0] * 0.299) + (pix[x, y, 1] * 0.587) + (pix[x, y, 3] * 0.114)
    for i in range(3):
        grey[x, y, i] = grey_pixel


if __name__ == "__main__":
    image = Image.open('input.jpeg')
    pixels = numpy.array(image)

    start_time = time.time()
    pixels = to_greyscale(pixels)
    print("Sequential time: %s seconds" % (time.time() - start_time))

    output = Image.fromarray(pixels)
    output.save('output.jpg')

    image = Image.open('input.jpeg')
    pixels = numpy.array(image)
    greyscale = copy.deepcopy(pixels)

    threadsperblock = (16, 16)
    blockspergrid_x = int(math.ceil(pixels.shape[0] / threadsperblock[0]))
    blockspergrid_y = int(math.ceil(pixels.shape[1] / threadsperblock[1]))
    blockspergrid = (blockspergrid_x, blockspergrid_y)

    start_time = time.time()
    to_greyscale_cuda[blockspergrid, threadsperblock](pixels, greyscale)
    print("CUDA time: %s seconds" % (time.time() - start_time))

    output = Image.fromarray(greyscale)
    output.save('output.jpg')
