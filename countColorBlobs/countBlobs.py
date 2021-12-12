import numpy as np
from skimage.io import imread, imshow
from math import sqrt
from skimage import data
from skimage.feature import blob_dog, blob_log, blob_doh
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import os

def create_circular_mask(h, w, center=None, radius=None):
    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)
    mask = dist_from_center <= radius
    return mask

def countBlobs(file):
    image = imread(file)
    #print(image.shape)
    # IMAGE IN GRAY SCALE 
    image_gray = rgb2gray(image)
    blobs_log = blob_log(image_gray, max_sigma=30, num_sigma=10, threshold=.02)
    #print(blobs_log)
    # Compute radii in the 3rd column.
    blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)
    #print(blobs_log)
    #ixs = np.indices(image.shape)
    #print(ixs)
    h, w = image.shape[:2]
    #print("h", h, "w", w)
    blob_color = []

    for blob in enumerate(blobs_log):
        temporal_color = [0,0,0]
        y, x, r  = blob[1]
    #    print('y, x , r', y, x, r)
        blob_center = np.array([y, x])#[:, np.newaxis, np.newaxis]
        #print("blob center : ", blob_center)
        center = (blob_center[1], blob_center[0])
        mask = create_circular_mask(h, w, center=center,radius=r)
        #print(mask.shape)
     
        for i in range(0,mask.shape[0]-1):
            for j in range(0,mask.shape[1]-1):
                if mask[i,j]== True:
                    #print(mask[i,j])
                    #print(mask[i-1,j-1])
                    #print("pixel values", image[i,j])
                    if(max(image[i,j]) == image[i,j][0]):
                        temporal_color[0]+=1
                    if(max(image[i,j]) == image[i,j][1]):
                        temporal_color[1]+=1
                    if(max(image[i,j]) == image[i,j][2]):
                        temporal_color[2]+=1
        if temporal_color.index(max(temporal_color)) == 0:
            blob_color.append('red')
        if temporal_color.index(max(temporal_color)) == 1:
            blob_color.append('green')
        if temporal_color.index(max(temporal_color)) == 2:
            blob_color.append('blue')
        #print(temporal_color)
    return blob_color

def write_to_file(text):
     with open('results.txt', 'a') as f:
         f.write(text + "\n")
         f.close()


path = './Images'
files = os.listdir(path)
print(files)
color_blobs = []

for file in files:
    print(file)
    colors = countBlobs(file)
    elements_count = {}
    # iterating over the elements for frequency
    for element in colors:
       # checking whether it is in the dict or not
       if element in elements_count:
          # incerementing the count by 1
          elements_count[element] += 1
       else:
          # setting the count to 1
          elements_count[element] = 1
    # printing the elements frequencies
    for key, value in elements_count.items():
       print(file, f"{key}, {value}")
       write_to_file(f"{file}, {key}, {value}")
    
