import os
import pandas
import shutil

kilobots = 37

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
print(df)
problematic = df[df['total_kilobots'] != kilobots ].dropna()
print(problematic)

for i in problematic['image'].unique():
    print(i)
    src = r'./Images/'+ str(i)
    dst =  r'./problematicImages/' + str(i)
    shutil.copyfile(src, dst)
    print("Image " + str(i) + " has been copied to problematicImages")

# write the correctly counted into results.txt 
#def write_to_file(text):
#     with open('./results.txt', 'a') as f:
#         f.write(text + "\n")
#         f.close()

correctly_counted = df[df['total_kilobots'] == kilobots ].dropna()
with open('results.txt', 'a') as f:
    dfAsString = correctly_counted.to_string(header=False, index=False)
    f.write(dfAsString)
    f.write('\n')
print("corectly counted")
print(correctly_counted)

