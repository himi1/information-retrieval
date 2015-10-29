__author__ = 'Himanshi'

import sys
import math
import operator

# Data Structures:
# inlink_dictionary     : dictionary where the doc id is the key and the values are all pages pointing to it
# outlink_dictionary    : dictionary where the doc id is the key and the value is the number of outlinks from that page
# page_ranks            : dictionary where the doc id is the key and the value is the PageRank value for that page
# newPR                 : dictionary which is used as a temporary dictionary to update the PageRank value in page_ranks
# sink_nodes            : the list of sink nodes
# damp_factor           : the damping factor as usual
# all_links             : the list of all the pages(document ID's)
# num_of_links          : total number of links in all_links
# inlinks_textfile      : variable to store the inlinks text file name given by user.

inlink_dictionary = {}
outlink_dictionary = {}
page_ranks = {}
new_page_ranks = {}
sink_nodes = []
damp_factor = 0.85
num_of_links = 0
inlinks_textfile = "wt2g_inlinks.txt"   # Setting default value to "wt2g_inlinks.txt"
six_nodes_textfile = "six_nodes.txt"

# Function to collect links from the inlinks_textfile
def collect_links():
    all_links = []
    f = open(inlinks_textfile,'r')
    line = f.readline()
    while line:
        links = line.split()    # Split it based on blank spaces
        if links[0] not in outlink_dictionary:
            outlink_dictionary[links[0]] = 0
        for link in links[1:]:
            if link not in outlink_dictionary:
                outlink_dictionary[link] = 1
            else:
                outlink_dictionary[link] += 1
        inlink_dictionary[links[0]] = links[1:]
        all_links += links
        line = f.readline()  # Change the value of line to next line in the inlinks_textfile
    all_links = set(all_links)
    return all_links


# Function to Initialize all the links to 1/num_of_links value
def init_rank():
    global num_of_links
    num_of_links = len(all_links)
    probability_of_each_link = 1.0/num_of_links
    for link in all_links:
        page_ranks[link] = probability_of_each_link


# Function to collect sink nodes among all the nodes
def collect_sink_nodes():
    for page in outlink_dictionary:
        if outlink_dictionary[page] == 0:   # If the number of outlinks of page is 0
            sink_nodes.append(page)         # Then add it to the sink_nodes list


# Function to calculate perplexity value
def calculate_perplexity():
    entropy = 0
    for link in all_links:
        pr = page_ranks[link]
        entropy += pr * math.log(1/pr,2)
    return 2**entropy


# Function to check for convergence
def check_for_convergence(old,new):
    old = math.floor(old)
    new = math.floor(new)
    if old == new:
        return 0
    else:
        return 1


# Sort the final values of page ranks and write them to the output text file
def write_pagerank():
    final_list = []
    sorted_page_ranks = sorted(page_ranks.items(), key=operator.itemgetter(1), reverse=True)
    count = 1           # To maintain the count of pages being written in the file
    for page in sorted_page_ranks:
        final_list.append(str(count) + ' ' + str(page[0]) + ' ' + str(page[1]) + '\n')
        count += 1
    # Writing to file
    f = open('page_rank_list.txt', 'w+')
    for item in final_list:
        f.write(item)


# Function which implements the PageRank Algorithm to get the page ranks
def get_page_rank():
    old_perplexity = 0.0
    flag = 1
    i = 0       # Iteration i
    check = 0
    while flag:
        i += 1
        print "Iteration:", i
        sink_pr = 0
        for page in sink_nodes:
            sink_pr += page_ranks[page]
        for page in all_links:
            new_page_ranks[page] = (1-damp_factor)/num_of_links
            new_page_ranks[page] += damp_factor * (sink_pr/num_of_links)
            if page not in inlink_dictionary:
                continue
            for in_link in inlink_dictionary[page]:
                new_page_ranks[page] += damp_factor * (page_ranks[in_link]/outlink_dictionary[in_link])
        for link in all_links:
            page_ranks[link] = new_page_ranks[link]
        new_perplexity = calculate_perplexity()
        print "Perplexity:", new_perplexity
        '''f = open('perplexity_values_until_convergence.txt', 'a+')
        f.write("Iteration: " + str(i) + ", Perplexity: " + str(new_perplexity) + "\n")'''
        flag = check_for_convergence(old_perplexity,new_perplexity)
        if flag == 0:
            check += 1
            if check == 4:
                flag = 0
            else:
                flag = 1
        else:
            check = 0
        old_perplexity = new_perplexity


def main():
    args = sys.argv
    if len(args) == 2:                  # pagerank.py "inlink_textfile.txt"
        global inlinks_textfile
        inlinks_textfile = args[1]
    global all_links
    all_links = collect_links()
    init_rank()
    collect_sink_nodes()
    print "Getting Page Ranks now..."
    get_page_rank()
    print "Convergence is reached."
    print "Writing to file..."
    write_pagerank()


if __name__ == '__main__':
    main()