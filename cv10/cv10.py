from __future__ import division
import math
from PIL import Image
import numpy
import copy
from numba import cuda
import glob
import numpy as np


@cuda.jit()
def to_greyscale_cuda(pix, grey):
    x, y = cuda.grid(2)
    if x < pix.shape[0] and y < pix.shape[1]:
        grey_pixel = (pix[x, y, 0] * 0.299) + (pix[x, y, 1] * 0.587) + (pix[x, y, 3] * 0.114)
    for i in range(3):
        grey[x, y, i] = grey_pixel


if __name__ == "__main__":
    cuda.profile_start()
    streams = []
    pixels_gpu = []
    greyscale_gpu = []
    gpu_out = []
    streams = []
    start_events = []
    end_events = []
    kernel_times = []
    images = []
    threadsperblock = (8, 8)

    # load images
    image_paths = (glob.glob("images/*.jpg"))
    for image_path in image_paths:
        image = Image.open(image_path)
        pixels = numpy.array(image)
        greyscale = copy.deepcopy(pixels)
        images.append({"pixels": pixels, "greyscale": greyscale})
        streams.append(cuda.stream())
        start_events.append(cuda.event())
        end_events.append(cuda.event())

    # copy to GPU
    for k, image in enumerate(images):
        pixels_gpu.append(cuda.to_device(image.get('pixels'), stream=streams[k]))
        greyscale_gpu.append(cuda.to_device(image.get('greyscale'), stream=streams[k]))

    # process arrays.
    for k, image in enumerate(images):
        blockspergrid_x = image.get('pixels').shape[0] // threadsperblock[0]
        blockspergrid_y = image.get('pixels').shape[1] // threadsperblock[1]
        blockspergrid = (blockspergrid_x, blockspergrid_y)
        start_events[k].record(streams[k])
        to_greyscale_cuda[blockspergrid, threadsperblock, streams[k]](pixels_gpu[k], greyscale_gpu[k])

    # record ends
    for k, image in enumerate(images):
        end_events[k].record(streams[k])

    # copy processed arrays to host
    for k, greyscale_gpu_k in enumerate(greyscale_gpu):
        gpu_out.append(greyscale_gpu_k.copy_to_host(stream=streams[k]))

    # print out execution times
    for k, end_event in enumerate(end_events):
        end_event.synchronize()
        kernel_times.append(cuda.event_elapsed_time(start_events[k], end_events[k]))
        print('Kernel execution time in milliseconds: %f ' %
              cuda.event_elapsed_time(start_events[k], end_event))

    print('Mean kernel duration (milliseconds): %f' % np.mean(kernel_times))
    print('Mean kernel standard deviation (milliseconds): %f' % np.std(kernel_times))

    # save processed images
    for k, image_out in enumerate(gpu_out):
        output = Image.fromarray(image_out)
        output.save('output' + str(k) + '.jpg')

