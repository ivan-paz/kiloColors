from skimage.io import imread
from skimage.feature import blob_dog, blob_log
from skimage.color import rgb2gray


def DoG_countBlobs(file):
    image = imread(file)
    #print(image.shape)
    # IMAGE IN GRAY SCALE
    image_gray = rgb2gray(image)
#    print("this algorithm is not so accurate but it is a short meow")
    blobs_dog = blob_dog(image_gray, min_sigma=5, max_sigma=20, threshold=0.01)
    # Compute radii in the 3rd column.
    #blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)
#    print(type(blobs_log))
    return getColors(image, blobs_dog)


def LoG_countBlobs(file):
    image = imread(file)
    #print(image.shape)
    # IMAGE IN GRAY SCALE
    image_gray = rgb2gray(image)
    #print("this is accurate but it is a long meoooooooooooooow")
    blobs_log = blob_log(image_gray, max_sigma=20,
                         num_sigma=10, threshold=.016)
#    print('meow ends!')
    # Compute radii in the 3rd column.
    #blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)
#    print(type(blobs_log))
    return getColors(image, blobs_log)


def getColors(image, blobs):
    RGB = [0, 0, 0]
    for blob in enumerate(blobs):
        # temporal_color = [0, 0, 0]
        y, x, r = blob[1]
        #print('y, x , r', y, x, r)

        # blob_center = np.array([y, x])  # [:, np.newaxis, np.newaxis]
        #print("blob center : ", blob_center)
        # center = (y, x)
        # print(center)
        #mask = create_circular_mask(h, w, center=center,radius=r)
        #print(image[int(center[1]),int(center[0])])
        central_pixel_rgb = image[int(y), int(x)]
        #print(central_pixel_rgb)
        #central_pixel_rgb.argmax(axis=0)
        max_channel = central_pixel_rgb.argmax(axis=0)
        RGB[central_pixel_rgb.argmax(axis=0)] += 1

    #print(blob_color)
    return RGB
