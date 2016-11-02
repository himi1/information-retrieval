INSRTUCTIONS FOR COMPILING CODE:

1. To create the Inverted index:
********************************

RUN: indexer.py "corpus_file.txt" "index_output_file"
For instance: python indexer.py tccorpus.txt index.out

-> indexer.py:		python script to generate inverted index
-> tccorpus.txt:	input corpus for inverted index
-> index.out:		output file containing inverted index dictionary

Note: tccorpus.txt should be present in the same folder as indexer.py

Output: Returns the inverted index dictionary saved into index.out file, which is created in the same folder as indexer.py

2. To implement BM25 ranking algorithm:
***************************************

RUN: python bm25.py "inverted_index_file.txt" "query_file.txt" "Max_Number_of_document_results(int)" > "result_file"
For instance: python bm25.py index.out queries.txt 100 > results.eval
-> bm25.py:			python script to generate a ranked list of documents for input query file with one or more queries
-> index.out:		index file containing inverted index from part 1 stated above
-> queries.txt:		query file containing one or more queries
-> 100:				maximum number of document results
-> result.eval:		output file containing a ranked list of documents for the given query file

Note: index.out and queries.txt should be present in the folder as bm25.py

Output: Returns the ranked list of documents saved into index.out file, which is created in the same folder as bm25.py
