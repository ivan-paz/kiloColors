from skimage.io import imread
from skimage.feature import blob_dog, blob_log, peak_local_max
from skimage.color import rgb2gray
from scipy.ndimage import gaussian_filter
from numpy import sum
import numpy as np
import matplotlib.pyplot as plt
import os


def print_image_with_blobs(file, im, coord, colors):

    color_names = ['r', 'g', 'b']

    dpi = 300

    fig, ax = plt.subplots(
        figsize=(im.shape[1] / dpi, im.shape[0] / dpi), dpi=dpi)
    ax.set(xticks=(), yticks=())
    ax.imshow(im)
    for point, color in zip(coord, colors):
        ax.add_patch(
            plt.Circle(point[::-1], 20, color=color_names[color], fill=False, lw=0.5))
    plt.subplots_adjust(0, 0, 1, 1)
    fig.savefig('checks/' + os.path.basename(file))
    plt.close('all')


def single_sigma_search(file, n_blobs, sigma):

    im = imread(file)
    im_gray = sum(im, axis=-1)
    gaus = gaussian_filter(im_gray, sigma=sigma, truncate=2)
    gaus = gaus - np.min(gaus)
    coord = peak_local_max(gaus, min_distance=6,
                           num_peaks=n_blobs, threshold_rel=0.1)
    #

    # WE NEED SOME TYPE OF DOUBLE-CHECK TO VERIFY THE CORRECT BLOB DETECTION
    # CHECK ONE: LOOK FOR n_blobs+1 AND SEE IF THE LEAST BRIGHT BLOB IS BACKGROUND
    # WHAT HAPPENS WHEN SOME KILOBOT IS OF IN THIS FRAME?

    # min_bright = peak_bright(gaus, coord[-1], int(sigma) + 1)
    # for point in coord:
    #     # print(peak_bright(gaus, point, int(sigma) + 1), end=' ')
    #     print(gaus[point[0], point[1]], end=' ')
    # print()

    colors = getColors(im, coord)

    # WE CAN PUT SOME FLAG TO PRINT ALL FRAMES WITH DETECTED BLOBS
    if len(coord) != n_blobs:
        print_image_with_blobs(file, im, coord, colors)

    # Return the counts of each color (number of Red blobs, Greens and Blues)
    return np.bincount(colors, minlength=3)


# def DoG_countBlobs(file):
#     image = imread(file)
#     # print(image.shape)
#     # IMAGE IN GRAY SCALE
#     image_gray = rgb2gray(image)
#     # image_gray = sum(image, axis=-1)
# #    print("this algorithm is not so accurate but it is a short meow")
#     blobs_dog = blob_dog(image_gray, min_sigma=5, max_sigma=20, threshold=0.01)
#     # Compute radii in the 3rd column.
#     #blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)
# #    print(type(blobs_log))
#     return getColors(image, blobs_dog[:, :2])


# def LoG_countBlobs(file):
#     image = imread(file)
#     # print(image.shape)
#     # IMAGE IN GRAY SCALE
#     image_gray = rgb2gray(image)
#     #print("this is accurate but it is a long meoooooooooooooow")
#     blobs_log = blob_log(image_gray, max_sigma=20,
#                          num_sigma=10, threshold=.016)
# #    print('meow ends!')
#     # Compute radii in the 3rd column.
#     #blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)
# #    print(type(blobs_log))
#     return getColors(image, blobs_log[:, :2])


def getColors(image, blobs_coords):
    '''
    Returns the strongest channnel of each blob (R=0, G=1, B=2)
    This is a fast and vectorized color detector method bot only works with RGB
    '''
    return np.argmax(image[blobs_coords[:, 0], blobs_coords[:, 1]], axis=1)
