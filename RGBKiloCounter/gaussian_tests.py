# %%
from cv2 import threshold
import skimage as sk
import scipy as sp
import numpy as np
from skimage.feature import blob_dog, blob_log
from matplotlib import pyplot as plt
from tqdm import tqdm
import os

# %%

# im = sk.data.camera()

# print(image.shape)
# IMAGE IN GRAY SCALE


# im = sk.color.rgb2gray(sk.io.imread('Images/output0062.jpg'))
im = np.sum(sk.io.imread('Images/output0062.jpg'), axis=-1)
im = im - np.min(im)
im = im / np.max(im)

# %%

ths = np.linspace(0.001, 0.25, 10)
fig, ax = plt.subplots()
files = next(os.walk('Images/'), (None, None, []))[2]
for file in tqdm(files[:10]):

    im = np.sum(sk.io.imread('Images/' + file), axis=-1)
    im = im - np.min(im)
    im = im / np.max(im)

    n_blobs = []
    for th in ths:
        blobs = blob_dog(im, min_sigma=1, max_sigma=4, threshold=th)
        n_blobs.append(len(blobs))
    ax.plot(ths, n_blobs)

ax.set(ylim=(0, 50))


# %%
max_sigma = 4
min_sigma = 1
sigma_ratio = 1.6


k = int(np.log(max_sigma / min_sigma) / np.log(sigma_ratio) + 1)
sigma_list = np.array([min_sigma * (sigma_ratio ** i)
                       for i in range(k + 1)])
print(sigma_list)
# %%

im = np.sum(sk.io.imread('Images/output0062.jpg'), axis=-1)
im = im - np.min(im)
im = im / np.max(im)


print(f' we have {len(blobs)} blobs')


# %%

im = sk.io.imread('Images/output0062.jpg')
im_gray = np.sum(im, axis=-1)
previous = blob_log(sk.color.rgb2gray(im), min_sigma=1,
                    max_sigma=5, num_sigma=30, threshold=0.03)

sigma = np.mean(previous[:, 2])


min_distance = 10
sp_gaus = sp.ndimage.gaussian_filter(im_gray, sigma=sigma, truncate=2)
coord = sk.feature.peak_local_max(
    sp_gaus, min_distance=min_distance, num_peaks=37, threshold_rel=0.2)


dpi = 300
fig, ax = plt.subplots(figsize=(im.shape[1] / dpi, im.shape[0] / dpi), dpi=dpi)
ax.set(xticks=(), yticks=())
ax.imshow(sk.io.imread('Images/output0062.jpg'))
for point in coord:
    ax.add_patch(plt.Circle(
        point[::-1], 20, color='w', fill=False, lw=0.5))
# ax[1, 1].plot(*coord[:, [1, 0]].T, 'ro', fillstyle='none', ms=10)
plt.tight_layout(pad=0)
fig.patch.set_facecolor('k')
fig.savefig('filter_test.png')
plt.close(fig)


# %%
# im_ = np.fft.fft2(im)
# sp_gaus = sp.ndimage.fourier_gaussian(
#     im_, sigma=sigma, n=- 1, axis=- 1, output=None)
# sp_gaus = np.fft.ifft2(sp_gaus).real.astype(np.uint8)


# %%
# %Blur Kernel
# ksize = 31
# kernel = zeros(ksize)

# %Gaussian Blur
# s = 3
# m = ksize / 2
# [X, Y] = meshgrid(1: ksize)
# kernel = (1 / (2 * pi * s ^ 2)) * exp(-((X - m). ^ 2 + (Y - m). ^ 2) / (2 * s ^ 2))

# %Display Kernel
# figure, imagesc(kernel)
# axis square
# title('Blur Kernel')
# colormap gray

# %Embed kernel in image that is size of original image
# [h, w] = size(origimage)
# kernelimage = zeros(h, w)
# kernelimage(1: ksize, 1: ksize) = kernel

# %Perform 2D FFTs
# fftimage = fft2(double(origimage))
# fftkernel = fft2(kernelimage)

# %Set all zero values to minimum value
# fftkernel(abs(fftkernel) < 1e-6) = 1e-6

# %Multiply FFTs
# fftblurimage = fftimage.*fftkernel

# %Perform Inverse 2D FFT
# blurimage = ifft2(fftblurimage)

# %Display Blurred Image
# figure, imagesc(blurimage)
# axis square
# title('Blurred Image')
# colormap gray
# set(gca, 'XTick', [], 'YTick', [])
