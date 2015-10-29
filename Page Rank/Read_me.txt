To run:
The file can be run in two of the following ways:
1. python pagerank.py
It takes inlink file "wt2g_inlinks.txt" by default
2. python pagerank.py "<inliks imput textfile.txt>"
   For example: python pagerank.py "six_nodes.txt"
Note: The input file should be a file in the in-link format as described in the problem set.

OUTPUT:
The output of pagerank.py is a text file page_rank_list.txt
This textfiles contains the page IDs and their PageRank values, sorted by the PageRank values

I have imported the following libraries:
sys
math
operator