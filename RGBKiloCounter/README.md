# kiloCounter 


Execute python kiloColorCounter.py \<number of kilobots to track\>

Images/ contains the images to analyze.

The kiloColorCounter script applies:

1. blob detection using the Difference of Gaussian algorithm (faster but a bit imprecise).

2. blob detection with the Laplace of Gaussian algorithm (slower but more accurate).

See the documentation here: 

https://scikit-image.org/docs/dev/auto_examples/features_detection/plot_blob.html?highlight=dog


## How it works

Each blob detection algorithm is performed by the corresponding script:

count_blobs_extract_mean_color_difference_of_Gaussian.py

count_blobs_extract_mean_color_Laplacian_of_Gaussian.py


the script count_blobs_extract_mean_color_difference_of_Gaussian.py writes the results in:

results_difference_of_gaussian.txt

the script countDifferenceOfGaussian.py checks if the number of detected blobs is less than the expected.

### Please note that

THE ACTUAL VERSION OF THE SCRIPT COUNTS VALID THE NUMBER-OF-KILOBOTS AND THE NIMBER-OF-KILOBOTS + 1 BECAUSE OF THE CURRENT EXPERIMENTS.

images NOT SATISFYING SUCH CONDITION are copied to problematicImages

images in problematicImages folder are analyzed with the Laplace of Gaussian blob detection.

the results are written in results_laplace_of_gaussian.txt


The script countLaplaceOfGaussian.py checks if the number of detected blobs is less than the expected, the images that do not satisfy this condition are copied to evil_images folder. 

The script 
count_blobs_extract_mean_color_difference_of_Gaussian.py writes the images with number-of-kilobots or number-of-kilobots + 1 in

results.txt 

The script count_blobs_extract_mean_color_Laplacian_of_Gaussian.py writes the number of blobs IN results.txt for all the processed images NO MATTER IF THE NUMBER DOES NOT MATCHES THE EXPECTED.

