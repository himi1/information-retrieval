import operator
import sys
import glob
import os
import math

# to run:
# python nbtest.py model.txt "C:\Users\Patricia\Documents\IR_CS6200\Asignments\NaiveBaye's\textcat\test" > Output.txt

# def find_bigrams(input_list):
#     bigram_list = []
#     for i in range(len(input_list)-1):
#         bigram_list.append((input_list[i], input_list[i+1]))
#     return bigram_list


def read_from_model_file(model_file):
    f = open(model_file, 'r')
    text = ''.join(f.readlines())
    d1, d2 = text.split("\n")
    Pos_prob_read = eval(d1)
    Neg_prob_read = eval(d2)
    return Pos_prob_read, Neg_prob_read
    f.close()

# reading the test file:
def read_test(path):
    doc_list = []
    filename_list = []
    # Reading all files from train-pos
    for filename in glob.glob(os.path.join(path, '*.txt')):
        filename_list.append(filename)
        with open(filename) as f:
            text = ''.join(f.readlines())
            doc_word_list = []
            for i in text.split('\n'):
                term = i.rstrip().split()
                # term = find_bigrams(term)
                # doc_word_list.append(term)
                doc_word_list.extend(term)

            doc_list.append(doc_word_list)
    return doc_list, filename_list


# calculating pos or neg probability for each document in test data:
def cal_prob(doc_list, dict):
    prob_sum = []
    for doc in doc_list:
        temp_prob = 0
        for term in doc:
            if term in dict:
                temp_prob += math.log(dict[term])
        prob_sum.append(temp_prob)
    return prob_sum

# calculating pos-neg and neg-pos ratios for top 20 items:
def top_20_ratio(pos, neg):
    pos_to_neg_ratio = {}
    neg_to_pos_ratio = {}
    for kp in pos.keys():
        pos_to_neg_ratio[kp] = math.log(pos[kp]) - math.log(neg[kp])
        neg_to_pos_ratio[kp] = math.log(neg[kp]) - math.log(pos[kp])
    top_20_pos_to_neg_ratio = sorted(pos_to_neg_ratio.items(), key=operator.itemgetter(1), reverse = True)[:20]
    top_20_neg_to_pos_ratio = sorted(neg_to_pos_ratio.items(), key=operator.itemgetter(1), reverse =True)[:20]


    print "top_20_neg_to_pos_ratio:", top_20_neg_to_pos_ratio
    print "top_20_pos_to_neg_ratio:", top_20_pos_to_neg_ratio


def main():
    Pos_prob, Neg_prob = read_from_model_file(sys.argv[1])
    top_20_ratio(Pos_prob,Neg_prob)
    docs_list, filename_list = read_test(sys.argv[2])

    pos_probability = cal_prob(docs_list, Pos_prob)
    neg_probability = cal_prob(docs_list, Neg_prob)

    i = 0
    neg_count = 0
    pos_count = 0
    while i < len(pos_probability):
        if pos_probability[i] <= neg_probability[i]:
            neg_count += 1
        else:
            pos_count += 1
        i += 1
    print "neg_count: " + str(neg_count), "pos_count: " + str(pos_count)

    j = 0
    # printing Scores of each file
    print "No.", "Filename", "Pos_probability", "Neg_probability"
    while j < len(filename_list):
        print (j+1), filename_list[j].split('\\')[-1:][0], pos_probability[j], neg_probability[j]
        j += 1


if __name__ == "__main__":
    main()