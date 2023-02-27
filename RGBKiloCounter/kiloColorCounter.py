import os
import shutil
from skimage.io import imread
from multiprocessing import Pool, freeze_support
import count_blobs_methods as methods
from tqdm import tqdm
import argparse
from numpy import bincount
import os
# main script to be executer in terminal

parser = argparse.ArgumentParser(
    description='Kilocounter tracks R, G, B colors from kilobots video frames')
parser.add_argument('kilobots', type=int, metavar='n_kilobots',
                    help='the number of kilobots to expect in the images')
parser.add_argument('-i', '--input', type=str, metavar='',
                    help='folder containing the images to process, default is Images', default='Images')
parser.add_argument('-o', '--output', type=str, metavar='',
                    help='name of the output file, default is results.csv', default='results.csv')
parser.add_argument('-e', '--evil_dir', type=str, metavar='',
                    help='folder to copy the evil images, default is Evil', default='Evil')
parser.add_argument('-n', '--n_processors', type=int, metavar='',
                    help='the number of threads to parallelize the computation, default is os.cpu_count()', default=os.cpu_count())
parser.add_argument('-r', '--results_dir', type=str, metavar='',
                    help='folder to copy all the images, default is None', default=None)


args = parser.parse_args()
kilobots = args.kilobots
n_procs = args.n_processors
input_dir = args.input
output = args.output
evil_dir = args.evil_dir
results_dir = args.results_dir

files = next(os.walk(input_dir), (None, None, []))[2]
n_images = len(files)

print(f'\n\tComputing {n_images} images from \"{input_dir}\".')
print(
    f'\tExpecting {kilobots} kilobots. Parallelyzing with {n_procs} processors.')
print(f'\tPrinting output to \"{output}\".')
print(f'\tPrinting evil processed images to \"{evil_dir}\"')
print(f'\tPrinting  all processed images to \"{results_dir}\"')
print('\t\t\t\tHERE WE GO!\n')


def parallel_computing(file):
    '''
    THIS SIGMA=2.7 HAS TO BE COMPUTED WITH DoG OR LoG BEFORE
    THE MAIN COLOR COUNTING BUT, SO FAR, ALL BLOBS ARE ARROUND SIGMA=2.7

    WE NEED SOME TYPE OF DOUBLE-CHECK TO VERIFY THE CORRECT BLOB DETECTION
    CHECK ONE: LOOK FOR n_blobs+1 AND SEE IF THE LEAST BRIGHT BLOB IS BACKGROUND
    WHAT HAPPENS WHEN SOME KILOBOT IS OF IN THIS FRAME?

    min_bright = peak_bright(gaus, coord[-1], int(sigma) + 1)
    for point in coord:
        # print(peak_bright(gaus, point, int(sigma) + 1), end=' ')
        print(gaus[point[0], point[1]], end=' ')
    print()
    '''

    ok = True
    im = imread(os.path.join(input_dir, file))

    coords = methods.single_sigma_search(im, n_blobs=kilobots, sigma=2.7)
    colors = methods.getColors(im, coords)

    if len(coords) != kilobots:
        ok = False
        dst = os.path.join(evil_dir, file)
        methods.print_image_with_blobs(dst, im, coords, colors)

    if results_dir:
        methods.print_image_with_blobs(os.path.join(
            results_dir, file), im, coords, colors)

    # Return the counts of each color (number of Red blobs, Greens and Blues)
    RGB = bincount(colors, minlength=3)

    return file, *RGB, ok


def main():

    with open(output, 'w') as f:
        f.write(" file, R, G, B, correct\n")

    n_ok = 0
    if results_dir:
        os.makedirs(results_dir, exist_ok=True)
    os.makedirs(evil_dir, exist_ok=True)
    for file in os.listdir(evil_dir):
        path = os.path.join(evil_dir, file)
        os.unlink(path)

    with Pool(n_procs) as pool:

        for im_out in tqdm(pool.imap_unordered(parallel_computing, files), total=n_images, mininterval=1):
            file, R, G, B, ok = im_out
            n_ok += ok

            with open(output, 'a') as f:
                f.write(f"{file},{R:3},{G:3},{B:3},{ok}\n")

    print(f'\n\t{n_ok} images ({100*n_ok/n_images:.1f}%) succeded')
    print(
        f'\tthe rest ({n_images-n_ok}, {100*(n_images-n_ok)/n_images:.1f}%) were copied to \"{evil_dir}\"')

    if n_ok == n_images:
        os.rmdir(evil_dir)

    print("\n\tThanks for using kilocounter! Have a nice day!")


if __name__ == '__main__':
    freeze_support()
    main()
