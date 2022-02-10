# 

Execute python kiloColorCounter.py

How this works.

Images contains the images to analize.

The script applies blob detection using the Difference of Gaussian and the Laplace of Gaussian, see the documentation here: 

https://scikit-image.org/docs/dev/auto_examples/features_detection/plot_blob.html?highlight=dog

Each blob detection is performed by the corresponding script:

count_blobs_extract_mean_color_difference_of_Gaussian.py

count_blobs_extract_mean_color_Laplacian_of_Gaussian.py

After the Difference of gausian the script countDifferenceOfGaussian.py checks if the number of detected blobs is less than the expected.

If that is the case, the respective images are copied to problematicImages

Images in problematicImages folder are analized with the Laplace of Gausian blob detection.

the results are writen in results_laplace_of_gaussian.txt


The script countLaplaceOfGaussian.py checks if the number of detected blobs is less than the expected, the images that do not satisfy this condition are copied to evil_images folder. 


