from math import log
from operator import itemgetter
from itertools import groupby
import sys

__author__ = 'Himanshi'

# To run: python bm25.py index.out queries.txt 100 > results.eval

# Defining constants
b = 0.75
k1 = 1.2
k2 = 100
R = 0.0             # Assuming that no relevance information is available

# Data structures:
# index: Dictionary containing the inverted index in format {'word':[('docid',freq),('docid',freq), ....]}
index = {}
doc_ids_to_tf = {}  # 'doc_to_tf' dictionary contains the docid as key and all unique words' term frequency as values.
avdl = 0            # Average document length

# Functions:


# Function to calculate the BM25 score for each word in the query
# Computes BM25 scores for documents in the list
# r         : Relevant documents containing word i
# q         : Frequency of word i in the query
# N         : Total number of documents in the collection
# K, k1, k2 : Fixed parameters for BM25
# n         : Number of docs containing word i
# dl        : Document length
# f         : Frequency of word i in the doc under consideration.
# avdl      : Average document length
# R         : Relevance information
def bm25_score_calculator(n,dl,f):
    r = 0       # Assuming that no relevance information is available
    q = 1       # Since every query is used just once
    N = len(doc_ids_to_tf)
    L = (float(dl)/float(avdl))
    K = k1*(b*L+(1-b))
    mul1 = ((k1+1)*f)/(K+f)
    mul2 = ((k2+1)*q)/(k2+q)
    mul3 = log(((r+0.5)/(R-r+0.5))/((n-r+0.5)/(N-n-R+r+0.5)))
    return mul1*mul2*mul3


# Function to retrieve the inverted index from index_file
def retrieve_inverted_lists(index_file):
    f = open(index_file)
    global index
    index = eval(f.read())


# Function to create doc_ids_to_tf and finally return average document length (avdl)
def cal_avg_length():
    sum = 0
    for key, values in index.items():
        for each in values:
            sum += int(each[1])
            if each[0] in doc_ids_to_tf:
                doc_ids_to_tf[each[0]].append(each[1])
            else:
                doc_ids_to_tf[each[0]] = [each[1]]
    return float(sum)/float(len(doc_ids_to_tf))


# Function to input queries from input query file
def input_query(query_file):
    f = open(query_file)
    lines = ''.join(f.readlines())
    query_list = [x.rstrip().split() for x in lines.split('\n')[:]]
    return query_list


# Function to implement BM25 Algorithm for query list
def bm25_ranker(qlist):
    global avdl
    avdl = cal_avg_length()
    results = []
    for query in qlist:
        results.append(bm25_for_each_query(query))
    return results


# Function to implement BM25 Algorithm for each query in query list
def bm25_for_each_query(query):
    doc_to_score = {}                         # This dictionary contains the docid as key and it's score as values
    N = len(doc_ids_to_tf)
    for each_word in query:
        if each_word in index.keys():
            word_val = index[each_word]       # Word_val is a list of tuples that contain the docid, freq for each word
            word_to_docid_n_freq = dict(word_val) # This dictionary contains the docid and frequency for the given word
            n = len(word_to_docid_n_freq)
            for docid,freq in word_to_docid_n_freq.items():
                score = bm25_score_calculator(n,calculate_dl(docid),freq)
                if docid not in doc_to_score:
                    doc_to_score[docid] = score
                else:
                    doc_to_score[docid] += score
    return doc_to_score


# Function to calculate document length(dl) for the given docid
def calculate_dl(docid):
    dl = 0
    for each_tf in doc_ids_to_tf[docid]:
        dl += each_tf
    return dl


# Main function
def main():
    retrieve_inverted_lists(sys.argv[1])        # Retrieve all inverted lists
    query_list = input_query(sys.argv[2])       # input queries from query file
    # Implement BM25 Algorithm on queries
    result_list = bm25_ranker(query_list)       # result_list of list of document to score dictionaries
    query_id = 1
    for each in result_list:
        # sorted_result sorts each element of dictionary({docid:score}), based on the scores and generates a list of
        # tuples, where each tuple is of form (docid,score)
        sorted_result_list = sorted(each.items(),key = itemgetter(1),reverse = True)
        rank = 1
        for each_list in sorted_result_list[:int(sys.argv[3])]:
            print 'query_id:', query_id, 'Q0: Q0', "doc_id:", each_list[0], "rank:", rank, "BM25_score:", each_list[1],\
                "system_name:", "System_123"
            rank += 1
        query_id += 1

if __name__=='__main__':
    main()
