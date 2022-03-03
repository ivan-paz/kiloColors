import os
import shutil
from multiprocessing import Pool
import count_blobs_methods as methods
from tqdm import tqdm
import argparse
import os


parser = argparse.ArgumentParser(
    description='Kilocounter tracks R, G, B colors from kilobots video frames')
parser.add_argument('kilobots', type=int, metavar='n_kilobots',
                    help='the number of kilobots to expect in the images')
parser.add_argument('-i', '--input', type=str, metavar='',
                    help='folder coneining the images to process, default is ./Images', default='Images')
parser.add_argument('-o', '--output', type=str, metavar='',
                    help='name of the output file, default is results.txt', default='results.txt')
parser.add_argument('-e', '--evil_dir', type=str, metavar='',
                    help='folder to copy the evil images, default is None', default=None)
parser.add_argument('-n', '--n_processors', type=int, metavar='',
                    help='the number of threads to parallelize the computation, default is os.cpu_count()', default=os.cpu_count())
parser.add_argument('-v', '--verbose', help='activate on_the_fly feedback',
                    action='store_true', default=False)

args = parser.parse_args()
kilobots = args.kilobots
n_procs = args.n_processors
input = args.input
output = args.output
evil = args.evil_dir
verbose = args.verbose

files = next(os.walk(input), (None, None, []))[2]
n_images = len(files)

print(f'\n\tComputing all {n_images} files from directory \"{input}\".')
print(
    f'\tExpecting {kilobots} kilobots. Parallelyzing with {n_procs} processors.')
print(f'\tWith verbose {verbose}. \tWriting output to \"{output}\".')
print(f'\tCopying evil images to \"{evil}\".\n\t\t\t\tHERE WE GO!\n')


def parallel_computing(file):
    path = os.path.join(input, file)

    RGB = methods.single_sigma_search(path, kilobots, 2.7)
    detected_blobs = sum(RGB)
    valid = (detected_blobs == kilobots or
             detected_blobs == (kilobots + 1))

    if valid:
        method = 'DoG'
    else:

        RGB = methods.LoG_countBlobs(path)
        detected_blobs = sum(RGB)
        valid = (detected_blobs == kilobots or
                 detected_blobs == (kilobots + 1))

        if valid:
            method = 'LoG'
        else:
            method = 'evil'

    return file, *RGB, method


def main():

    with open(output, 'w') as f:
        f.write(" file, R, G, B, method\n")

    evil_images = []
    n_evil = 0
    n_LoG = 0
    n_DoG = 0
    with Pool(n_procs) as pool:

        for im_out in tqdm(pool.imap_unordered(parallel_computing, files), total=n_images, mininterval=1):
            file, R, G, B, method = im_out

            if method == 'evil':
                evil_images.append(file)
                n_evil += 1
                if verbose:
                    tqdm.write(
                        f"Image {file} failed with DoG and LoG, it's an evil image")
            elif method == 'LoG':
                n_LoG += 1
                if verbose:
                    tqdm.write(
                        f"Image {file} failed with DoG, but succeded with LoG")
            else:
                n_DoG += 1

            with open(output, 'a') as f:
                f.write(f"{file},{R:3},{G:3},{B:3},{method:>4}\n")

    if len(evil_images) and evil:
        os.makedirs(evil, exist_ok=True)
        for file in os.listdir(evil):
            path = os.path.join(evil, file)
            os.unlink(path)

        for file in evil_images:
            src = os.path.join(input, file)
            dst = os.path.join(evil, file)
            shutil.copyfile(src, dst)

    print(f'\n\t{n_DoG} images ({100*n_DoG/n_images:.1f}%) succeded with DoG')
    print(f'\t{n_LoG} images ({100*n_LoG/n_images:.1f}%) succeded with LoG')
    print(f'\t{n_evil} images ({100*n_evil/n_images:.1f}%) are evil images\n')

    print("\tThanks for using kilocounter! Have a nice day!")


if __name__ == '__main__':
    main()
