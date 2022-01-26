import os
import pandas
import shutil

kilobots = 37

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
evil = df[df['total_kilobots'] != kilobots ].dropna()
print(evil)

for i in evil['image'].unique():
    print(i)
    src = r'./Images/'+ str(i)
    dst =  r'./evil_images/' + str(i)
    shutil.copyfile(src, dst)
    print("Image " + str(i) + " has been copied to evil_images")

correctly_counted = df[df['total_kilobots'] == kilobots ].dropna()
with open('results.txt', 'a') as f:
    dfAsString = correctly_counted.to_string(header=False, index=False)
    f.write(dfAsString)

print("corectly counted")
print(correctly_counted)

