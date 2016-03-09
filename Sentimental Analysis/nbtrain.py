import re
import glob
import os
import argparse

# to run:
# python nbtrain.py --pos "textcat\train\pos" --neg "textcat\train\neg" --model "model.txt"  > Output.txt


def read_train(path):
    dict = {}
    dict_list = []

    #to_remove = re.compile('[' + re.escape(r'@/\[]:,.!?#;$%^&<>*-_') + ']+')

    # Reading all files from train-pos
    for filename in glob.glob(os.path.join(path, '*.txt')):
        with open(filename) as f:
            text = ''.join(f.readlines())
            for i in text.split('\n'):
                #j = re.sub(to_remove, '', i)
                term = i.rstrip().split()
                dict_list.append(term)

    # Creating dictionary for words:
    for terms in dict_list:
        for term in terms:
            if term not in dict:
                dict[term] = 1
            else:
                dict[term] += 1
    return dict


def change_dict(dict1, dict2):
    # check if key not in dict, add key
    for kp,vp in dict1.iteritems():
        if kp not in dict2:
            dict2[kp] = 0
    print "after pos.iter", len(dict1), len(dict2)
    return dict2


def remove_words_freq_less_than_five(Pos, Neg):
    # removing words with freq less than 5
    for kp in Pos.keys():
        if Pos[kp] + Neg[kp] < 5:
            del Pos[kp]
            del Neg[kp]
    print "after del iter", len(Pos), len(Neg)
    return Pos, Neg

# 1. Jelinek-Mercer smoothing:

# def prob_calc(dict1, dict2):
#     prob_dict = {}
#     V = len(dict1)
#     count = sum(dict1.values()) + sum(dict2.values())
#     # print "count of pos", sum(dict1.values())
#     for kp in dict1.keys():
#         P = ((1-0.4)*(float(dict1[kp])/sum(dict1.values()))) + (0.4)*(float(dict1[kp]+dict2[kp])/count)
#         prob_dict[kp] = P
#     return prob_dict

# 2. Dirischlet smoothing:

# def prob_calc(dict1, dict2):
#     prob_dict = {}
#     V = len(dict1)
#     count = sum(dict1.values()) + sum(dict2.values())
#     for kp in dict1.keys():
#         P = (float(dict1[kp]) + (0.2*(float(dict1[kp])+dict2[kp]))/count) / (sum(dict1.values()) + 0.2)
#         prob_dict[kp] = P
#     return prob_dict


# calculating probabilities of all terms:
def prob_calc(dict):
    prob_dict = {}
    V = len(dict)
    count = sum(dict.values())
    #print V, count
    for k,v in dict.items():
        P = (float(v) + 1)/(count + V)
        prob_dict[k] = P
    return prob_dict

# Main Function
def main():
    parser = argparse.ArgumentParser(description = 'HW6')
    parser.add_argument('--pos', dest='pos1', action = 'store', default='pos', help= 'Enter path for Pos')
    parser.add_argument('--neg', dest='neg1', action = 'store', default='neg', help= 'Enter path for Neg')
    parser.add_argument('--model', dest='model', action = 'store', default='model', help= 'Enter path for output')
    args = parser.parse_args()

    pos_path = args.pos1
    neg_path = args.neg1
    filepath = args.model

    Pos = read_train(pos_path)
    Neg = read_train(neg_path)

    Neg = change_dict(Pos, Neg)
    Pos = change_dict(Neg, Pos)

    Pos, Neg = remove_words_freq_less_than_five(Pos, Neg)

    Pos_Prob = prob_calc(Pos)
    Neg_Prob = prob_calc(Neg)

    # calculating probabilities using J-M smoothing:
    # Pos_Prob = prob_calc(Pos, Neg)
    # Neg_Prob = prob_calc(Neg, Pos)

    f = open(filepath, 'w')
    f.write(str(Pos_Prob))
    f.write("\n")
    f.write(str(Neg_Prob))
    f.close()





if __name__ == "__main__":
    main()