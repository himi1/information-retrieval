import sys
from itertools import groupby

__author__ = 'Himanshi'

# To run: python indexer.py tccorpus.txt index.out

# Data structure:
# index: Dictionary containing the inverted index in format {'word':[('docid',freq),('docid',freq), ....]}
index = {}

# Functions:


# Function to input corpus from input_file
def extract_from_input(input_file):
    try:
        f = open(input_file, 'r')
    except:
        print input_file + " could not be opened. Please try again."
        exit()

    input = f.read().split()
    doc_list = []           # List of list of docid with words from each document
    for key, group in groupby(input, lambda x: x == '#'):
        if not key:
            doc_list.append(list(group))
    doc_to_token = {}       # This dictionary contains docid as key and all the words associated with it as values
    for each_list in doc_list:
        tokens = []         # List of token terms in each document
        for each in each_list[1:]:
            if not str.isdigit(each):
                tokens.append(each)
        doc_to_token[each_list[0]] = tokens
    return doc_to_token


# Function to compute the inverted index
def compute_index(doc_to_token):
    for key, values in doc_to_token.iteritems():
        word_to_freq = {}       # word_to_freq is a dictionary containing word as key and its frequency as value
        for each_word in values:
            if each_word not in word_to_freq:
                word_to_freq[each_word] = 1
            else:
                word_to_freq[each_word] += 1
        for k, value in word_to_freq.items():
            index.setdefault(k,[]).append((key,value,))


# Function to write the inverted index to output_file
def write_index_to_file(output_file):
    f = open(output_file, 'w')
    f.write(str(index))
    f.close()


# Main function
def main():
    args = sys.argv
    if len(args) == 3:              # indexer tccorpus.txt index.out
        print "Extracting corpus from file..."
        doc_to_token = extract_from_input(args[1])
        print "Extraction complete. Computing inverted index now"
        compute_index(doc_to_token)
        print "Printing inverted index to " + args[2] + " now"
        write_index_to_file(args[2])
    else:
        print "Wrong input. Please try again. Input format should be of type: indexer tccorpus.txt index.out"

if __name__== '__main__':
    main()