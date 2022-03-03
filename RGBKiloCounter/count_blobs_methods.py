from skimage.io import imread
from skimage.feature import blob_dog, blob_log, peak_local_max
from skimage.color import rgb2gray
from scipy.ndimage import gaussian_filter
from numpy import sum
import matplotlib.pyplot as plt
import os


def single_sigma_search(file, n_blobs, sigma):
    image = imread(file)

    image_gray = sum(image, axis=-1)

    min_distance = 10
    sp_gaus = gaussian_filter(image_gray, sigma=sigma, truncate=2)
    coord = peak_local_max(sp_gaus, min_distance=min_distance,
                           num_peaks=n_blobs, threshold_rel=0.2)


    if len(coord)!=n_blobs:
        dpi = 300
        fig, ax = plt.subplots(
            figsize=(image.shape[1] / dpi, image.shape[0] / dpi), dpi=dpi)
        ax.set(xticks=(), yticks=())
        ax.imshow(imread(file))
        for point in coord:
            ax.add_patch(plt.Circle(
                point[::-1], 20, color='w', fill=False, lw=0.5))
        plt.tight_layout(pad=0)
        fig.patch.set_facecolor('k')

        fig.savefig(f'checks/{len(coord)}'+os.path.basename(file))

    return getColors(image, coord)


def DoG_countBlobs(file):
    image = imread(file)
    # print(image.shape)
    # IMAGE IN GRAY SCALE
    image_gray = rgb2gray(image)
    # image_gray = sum(image, axis=-1)
#    print("this algorithm is not so accurate but it is a short meow")
    blobs_dog = blob_dog(image_gray, min_sigma=5, max_sigma=20, threshold=0.01)
    # Compute radii in the 3rd column.
    #blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)
#    print(type(blobs_log))
    return getColors(image, blobs_dog[:, :2])


def LoG_countBlobs(file):
    image = imread(file)
    # print(image.shape)
    # IMAGE IN GRAY SCALE
    image_gray = rgb2gray(image)
    #print("this is accurate but it is a long meoooooooooooooow")
    blobs_log = blob_log(image_gray, max_sigma=20,
                         num_sigma=10, threshold=.016)
#    print('meow ends!')
    # Compute radii in the 3rd column.
    #blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)
#    print(type(blobs_log))
    return getColors(image, blobs_log[:, :2])


def getColors(image, blobs):
    RGB = [0, 0, 0]
    for blob in blobs:
        # temporal_color = [0, 0, 0]
        y, x = blob
        #print('y, x , r', y, x, r)

        # blob_center = np.array([y, x])  # [:, np.newaxis, np.newaxis]
        #print("blob center : ", blob_center)
        # center = (y, x)
        # print(center)
        #mask = create_circular_mask(h, w, center=center,radius=r)
        # print(image[int(center[1]),int(center[0])])
        central_pixel_rgb = image[int(y), int(x)]
        # print(central_pixel_rgb)
        # central_pixel_rgb.argmax(axis=0)
        max_channel = central_pixel_rgb.argmax(axis=0)
        RGB[central_pixel_rgb.argmax(axis=0)] += 1

    # print(blob_color)
    return RGB
