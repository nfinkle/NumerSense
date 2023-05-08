from collections import Counter

# Open the file for reading
filename = 'data/test.new.answers.txt'
counts = {}
with open(filename, 'r') as file:
    # Read one line at a time
    lines = file.read().splitlines()
    # Check if line is not empty
    for line in lines:
        # Print the line
        # print(line)
        # Read the next line
        word = line.split('\t')[-1]
        # if word == "no": word = "zero"
        counts[word] = counts.get(word, 0) + 1
print(list(counts.keys()), list(counts.values()))
