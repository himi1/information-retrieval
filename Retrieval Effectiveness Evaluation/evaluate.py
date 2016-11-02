from math import log
import sys

__author__ = 'Himanshi'

# To run: python evaluate.py cacm.rel results.eval > output.txt

Number_of_results_for_each_query = 100


def retrieve_dict_from_file(file):
    f = ""
    dict = {}
    try:
        f = open(file)
    except:
        print "Unable to read", file + ".", "Please try again."
        exit()
    lines = ''.join(f.readlines())
    list = [x.rstrip().split() for x in lines.split('\n')[:]]
    #print list
    for each in list:
        #print each
        if each:
            if each[0] in dict:
                #print each[0]
                dict[each[0]].append(each[1:])
            else:
                #print each[0]
                dict[each[0]] = [each[1:]]
    return dict


# Function to calculate Precision
# Input: r_list = relevance_list, qr_list = query_result_list
# r_list is like: 1 Q0 CACM-2629 1 i.e query_id Q0 doc_id relevance
# qr_list is like: 1 Q0 3127 1 14.4047655861 System_123 i.e. query_id  Q0 doc_id rank score

def precision_calculator(r_list, qr_list, query_id):
    map = 0
    ap = 0
    dcg = 0
    #qr_list = qr_list[:-1] # removing last empty element
    precision_at_k_dict = {}
    precision_at_k_dict_string = []
    final_precision = []
    relevant_count = 0
    results_parsed = 0  
    for each in qr_list:
        relevance_level = "0"
        results_parsed += 1
        #print results_parsed
        count_rel_docs = 0
        for rel in r_list:
            count_rel_docs += 1
            if (each[1] in rel[1]):
                relevant_count += 1
                relevance_level = "1"
        precision = (relevant_count/float(results_parsed))
        precision_at_k_dict[("P@" + str(results_parsed))] = precision
        if relevance_level is "1":
            #print precision
            ap += precision
            if each[2] == "1":  #if rank = 1
                dcg = 1
            else:
                dcg += 1/log(float(each[2]), 2)
            #print "dcg at rank", each[3], dcg
        idcg = calc_idcg(count_rel_docs) 
        #print idcg
        rank = int(each[2])
        ndcg = dcg/idcg[rank - 1]
        #"Query Id", "Rank", "Document id", "Document score", "Relevance level", "Precision","Recall","NDCG"
        precision_at_k_dict_string.append([str(query_id),
                                               str(each[2]),
                                               str(each[1]),
                                               str(each[3]),
                                               relevance_level,
                                               "P@"+ str(results_parsed) + ": "
                                                   + str((relevant_count/float(results_parsed))),
                                               str(relevant_count/float(count_rel_docs)),
                                               ndcg])

    final_precision = ("P@"+ str(results_parsed) + " for query " + str(query_id)
                                   + " is " + str((relevant_count/float(results_parsed))))
    #print(count_rel_docs)
    ap_output = ap/count_rel_docs
    return precision_at_k_dict, final_precision, precision_at_k_dict_string, ap_output

def calc_idcg(rel_doc_count):
    #print "rel_doc_count:", rel_doc_count
    n = Number_of_results_for_each_query
    idcg = [1]
    temp = 1
    i = 2
    while i <= rel_doc_count :
        temp += 1/log(float(i), 2)
        idcg.append(temp)
        i += 1
    while i <= 100:
        idcg.append(temp)
        i += 1
    return idcg


# function to print precision values
def print_job(precision_at_k_dict, final_precision, precision_string, ap, query_id):
    print "Output for Query", query_id + ":"
    print final_precision
    print "P@20 is ", precision_at_k_dict["P@20"]
    print "Ap_count is", ap
    print "Retrieval effectiveness Table:"
    print '{}\t{}\t{}\t{}\t{}\t{}\t\t\t\t\t{}\t\t\t\t{}'.format("Q_Id", "Rank", "Document_id", "Document_score", "Relevance","Precision","Recall","NDCG")
    for each in precision_string:
        print '{}\t\t{}\t\t{:<10}\t{:<15}\t{:<10}\t{:<25}\t{:<18}\t{:<10}'.format(each[0], each[1], each[2], each[3],  each[4], each[5], each[6], each[7])


# Main function
def main():
    relevance_dict = retrieve_dict_from_file(sys.argv[1])           # Retrieve relevant list from cacm.rel
    query_result_dict = retrieve_dict_from_file(sys.argv[2])        # Retrieve query result list from result.txt
    query_count = len(query_result_dict)
    #print relevance_dict
    #print query_result_list
    map = 0
    write_to_file = []
    for k1,v1 in sorted(relevance_dict.items()):
        for k2,v2 in sorted(query_result_dict.items()):
            if k1 == k2:
                relevance_list = v1
                query_result_list = v2
                precision_at_k_dict, final_precision, \
                precision_string, ap_output = precision_calculator(relevance_list, query_result_list, k1)
                print_job(precision_at_k_dict, final_precision, precision_string, ap_output, k1)
                write_to_file.append("Output for Query " + k1 + ":")
                write_to_file.append(str(final_precision))
                write_to_file.append("P@20: " + str(precision_at_k_dict["P@20"]))
                map += ap_output

    print "MAP for all the queries:", map/(float(query_count))
    #print write_to_file
    write_to_file.append("MAP for all the queries: " + str(map/(float(query_count))))
    f = open("evaluation_results.txt", "w+")
    for each in write_to_file:
        f.write(str(each) + "\n")
    f.close()
    return

if __name__=='__main__':
    main()


