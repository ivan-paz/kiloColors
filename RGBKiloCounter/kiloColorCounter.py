import os
import pandas
import shutil
import subprocess
import sys

try:
    kilobots = sys.argv[1]
    print(' ')
    print("kilocounter is tracking colors expecting "+str(kilobots)+" kilobots!")
    print("Hi I am kiloRGBcounter, I am capable of tracking R, G or B colors. For further extensions please hold in the line")
    print('')
except IndexError:
    print('Please provide the number of kilobots you expect to track!')
    sys.exit(1)

# remove images in the folder
path = os.chdir('./')
if os.path.exists('results_difference_of_gaussian.txt'):
    os.remove('results_difference_of_gaussian.txt')

print('-------------------------------------------')
print(' ')
print("file results_difference_of_gaussian.txt removed!")
print(' ')
print('-------------------------------------------')

# 
path = os.chdir('./')
if os.path.exists('results.txt'):
    os.remove('results.txt')
print('file results.txt removed!; writing a new one')

print(' ')
print('Running difference of gaussian algorithm  m^..^m /  (short meows)')
os.system("time python count_blobs_extract_mean_color_difference_of_Gaussian.py")

os.system("time python countDifferenceOfGaussian.py "+str(kilobots)+" ")

path = os.chdir('./')
if os.path.exists('results_laplace_of_gaussian.txt'):
    os.remove('results_laplace_of_gaussian.txt')
    print('file results_laplace_of_gaussian.txt has been deleted!')
print('-------------------------------------------')

print('Running Laplacian of gaussian algorithm  m ^..^ m   (long mwoooooooooows)')
os.system("time python count_blobs_extract_mean_color_Laplacian_of_Gaussian.py")

os.system("time python countLaplaceOfGaussian.py " +str(kilobots)+" ")

print("Thanks for using kilocounter! Have a nice day!")
