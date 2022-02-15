import os
import pandas
import shutil
import sys

#kilobots = 37
kilobots = sys.argv[1]
kilobots = int(kilobots)

# remove images in the folder
path = os.chdir('./evil_images')
files = os.listdir(path)
for file in files:
    os.remove(file)
print('-------------------------------------------')
print("images in folder evil_images removed!")
print('-------------------------------------------')

# find problematic images
path = os.chdir('../')

# reading the CSV file
df = pandas.read_csv('results_laplace_of_gaussian.txt')
# create a column with the sum of kilobots grouping by "image"
df['total_kilobots'] = df.groupby('image')['kilobots'].transform('sum')
# displaying the contents of the CSV file
print(df)
#evil = df[df['total_kilobots'] == mask ].dropna()
df_kilobots = df[df['total_kilobots'] != kilobots].dropna()
df_kilobots_1 = df_kilobots[df_kilobots['total_kilobots'] != kilobots+1].dropna()
evil = df_kilobots_1
#evil = df[ df['total_kilobots'] == kilobots & df['total_kilobots'] == kilobots + 1 ]#.dropna()
print(evil)

for i in evil['image'].unique():
    print(i)
    src = r'./Images/'+ str(i)
    dst =  r'./evil_images/' + str(i)
    shutil.copyfile(src, dst)
    print("Image " + str(i) + " has been copied to evil_images")

#correctly_counted = df[df['total_kilobots'] == kilobots ].dropna()

with open('results.txt', 'a') as f:
    dfAsString = df.to_string(header=False, index=False)
    f.write(dfAsString)

print("result of laplace of gaussian")
print(df)
