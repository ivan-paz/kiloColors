import os
import pandas
import shutil
import subprocess

# remove images in the folder
path = os.chdir('./')
if os.path.exists('results_difference_of_gaussian.txt'):
    os.remove('results_difference_of_gaussian.txt')

print('-------------------------------------------')
print(' ')
print("file results_difference_of_gaussian.txt removed!")
print(' ')
print('-------------------------------------------')

os.system("python count_blobs_extract_mean_color_difference_of_Gaussian.py")

os.system("time python countDifferenceOfGaussian.py")

if os.path.exists('results_difference_of_gaussian.txt'):
    os.remove('results_laplace_of_gaussian.txt')
print('-------------------------------------------')

os.system("time python count_blobs_extract_mean_color_Laplacian_of_Gaussian.py")

os.system("time python countLaplaceOfGaussian.py")

print("Thanks for using kilocounter! Have a nice day!")
