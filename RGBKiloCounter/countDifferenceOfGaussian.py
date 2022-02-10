import os
import pandas
import shutil
import sys

try:
    kilobots = sys.argv[1]
    kilobots = int(kilobots)
except IndexError:
    print('Please provide the number of kilobots (an integer) you expect to track!')
    sys.exit(1)

# remove images in the folder
path = os.chdir('./problematicImages')
files = os.listdir(path)
for file in files:
    os.remove(file)
print('-------------------------------------------')
print("images in folder problematicImages removed!")
print('-------------------------------------------')

# find problematic images
path = os.chdir('../')

# reading the CSV file
df = pandas.read_csv('results_difference_of_gaussian.txt')
# create a column with the sum of kilobots grouping by "image"
df['total_kilobots'] = df.groupby('image')['kilobots'].transform('sum')
# displaying the contents of the CSV file
print(df.to_string())
print('original data base')

df_kilobots = df[df['total_kilobots'] != kilobots].dropna()
df_kilobots_1 = df_kilobots[df_kilobots['total_kilobots'] != kilobots+1].dropna()
#problematic = df[df['total_kilobots'] == kilobots & df['total_kilobots'] == kilobots + 1]#.dropna()
problematic = df_kilobots_1
print('problematic images: ')
print(problematic.to_string())
print('---------------------------------------------------------')

for i in problematic['image'].unique():
    print(i)
    src = r'./Images/'+ str(i)
    dst =  r'./problematicImages/' + str(i)
    shutil.copyfile(src, dst)
    print("Image " + str(i) + " has been copied to problematicImages")

k1 = df[df['total_kilobots'] == kilobots ].dropna()  
k2 = df[df['total_kilobots'] == kilobots+1 ].dropna()
correctly_counted = pandas.concat([k1,k2],axis=0)

with open('results.txt', 'a') as f:
    dfAsString = correctly_counted.to_string(header=False, index=False)
    f.write(dfAsString)
    f.write('\n')
print("corectly counted")
print(correctly_counted)

