import numpy as np
from skimage.io import imread
from math import sqrt
from skimage.feature import blob_dog
from skimage.color import rgb2gray
import os
import colour
import cv2

#proposed_colors = {
        'red_lower' = np.array([255,0,0]),
        'red_upper' = np.array([255,0,0])
        #'yellow':[255,255,0], 
        #'green':  colour.RGB_to_YCbCr([0,255,0]), 
        #'cyan':   colour.RGB_to_YCbCr([0,255,255]), 
        #'blue':   colour.RGB_to_YCbCr([0,0,255]), 
        #'magenta':colour.RGB_to_YCbCr([255,0,255])
        #'white':  colour.RGB_to_YCbCr([255,255,255])
 
 #} # 'black':[0,0,0]
                  
def colorMSQD(pixelRGB, colorRGB):
    return np.sqrt(sum((pixelRGB-colorRGB)**2))
        
def colorMinDistance(pixelRGB):
    minDist = False
    minDistColor = False
    for k,v in proposed_colors.items():
        d = colorMSQD(pixelRGB,v)
        if not minDist or d < minDist:
            minDist = d
            minDistColor = k
    return minDistColor


def countBlobs(file):
    image = imread(file)
    #print(image.shape)
    # IMAGE IN GRAY SCALE 
    image_gray = rgb2gray(image)
    print("this is accurate but it is a long meoooooooooooooow")
    blobs_dog = blob_dog(image_gray, min_sigma = 5, max_sigma=20, threshold=0.01)
    
    return [image, blobs_dog]

def getColors(image,blobs):
    blob_color = []
    for blob in enumerate(blobs):
        temporal_color = [0,0,0]
        y, x, r  = blob[1]
     #   print('y, x , r', y, x, r)
        
        blob_center = np.array([y, x])#[:, np.newaxis, np.newaxis]
        #print("blob center : ", blob_center)
        center = (blob_center[1], blob_center[0])
        #mask = create_circular_mask(h, w, center=center,radius=r)
        #print(image[int(center[1]),int(center[0])])
   
        central_pixel_rgb = (image[int(center[1]),int(center[0])])
        print("Central pixel RGB : ", central_pixel_rgb) 
        
        colour_in_HSV = RGB_to_HSV(central_pixel_rgb)
        
        print("colour_in_HSV: ", colour_in_HSV)

        
        print("Assigned Color == ",color)


        #central_pixel_rgb.argmax(axis=0)
        if central_pixel_rgb.argmax(axis=0)==0:
            blob_color.append('red')
        if central_pixel_rgb.argmax(axis=0)==1:
            blob_color.append('green')
        if central_pixel_rgb.argmax(axis=0)==2:
            blob_color.append('blue')
    #print(blob_color)
    return blob_color

def write_to_file(text):
     with open('../results_difference_of_gaussian.txt', 'a') as f:
         f.write(text + "\n")
         f.close()

# ------------------------------------------------------------------
#
#  This is the "main" loop
# ------------------------------------------------------------------
path = os.chdir('./Images')
files = os.listdir(path)
#print(len(files))
#image = imread(files[0])
#print(image.shape)
color_blobs = []

write_to_file(f"{'image'},{'color'},{'kilobots'}")

for file in files:
    print(file)
    #print('aqui espero')
    image, blobs = countBlobs(file)
    #print('Yaaaa!') 
    #print(blobs)
    blobColors = getColors(image, blobs)
#    print(blobColors)
    elements_count = {}
    # iterating over the elements for frequency
    for element in blobColors:
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
       write_to_file(f"{file},{key},{value}")
    
