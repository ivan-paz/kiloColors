import pandas as pd

#data = pd.read_csv("/home/ivan/documents/kilobots/colour_tracking/tests/8_08_2021_4mm_vivora_subexpuesto/verbose.csv", sep = " ",header=None)
data = "/home/ivan/documents/kilobots/colour_tracking/tests/8_08_2021_4mm_vivora_subexpuesto/verbose.csv"

output = []
with open(data, 'r') as f:
    lines = f.readlines()
    colors = set(['red', 'green', 'blue'])
    for line in lines:
        for color in colors:
            if color in line:
                print(color)
                output.append(color + '\n')
        else:
            output.append(line)
for i in output:
    print(i)
