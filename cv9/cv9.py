from __future__ import division
from PIL import Image
import numpy


def to_greyscale(pix):
    for i, row in enumerate(pix):
        for j, column in enumerate(row):
            grey = (pix[i][j][0] * 0.299) + (pix[i][j][1] * 0.587) + (pix[i][j][2] * 0.114)
            pix[i][j][0] = grey
            pix[i][j][1] = grey
            pix[i][j][2] = grey
    return pix


if __name__ == "__main__":
    image = Image.open('input.jpeg')
    pixels = numpy.array(image)
    pixels = to_greyscale(pixels)
    output = Image.fromarray(pixels)
    output.save('output.jpg')
