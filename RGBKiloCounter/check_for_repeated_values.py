# creating variable to store the
# number of words
number_of_words = 0
word_list = []

# Opening our text file in read only
# mode using the open() function
with open("results.txt",'r') as file:

	# Reading the content of the file
	# using the read() function and storing
	# them in a new variable
    data = file.read()

	# Splitting the data into separate lines
	# using the split() function
    lines = data.split()

	# Iterating over every word in
	# lines
    for word in lines:

		# checking if the word is numeric or not
        if not word.isnumeric() and word not in ['blue','red','green']:
            word_list.append(word)
			# Adding the length of the
			# lines in our number_of_words
			# variable
            #print(word)

# Printing total number of words
#print(len(word_list.unique()))
print(word_list)
print(len(set(word_list)))

from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

counts = Counter(word_list)

labels, values = zip(*counts.items())

# sort your values in descending order
indSort = np.argsort(values)[::-1]

# rearrange your data
labels = np.array(labels)[indSort]
values = np.array(values)[indSort]

indexes = np.arange(len(labels))

bar_width = 0.35

plt.bar(indexes, values)

# add labels
plt.xticks(indexes + bar_width, labels,rotation='vertical')
plt.show()
