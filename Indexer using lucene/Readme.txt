Containing files:
*****************
1. IndexerAndRet folder:
	Contains source code for indexing and retrieval
2. IndexerAndRet.jar:
	Runnable jar file
3. termToTfFile:
	A sorted (by frequency) list of (term, term_freq pairs)
4. Zipf Law Graph and Queries comparisions.xls:
	->Sheet1: Contains a plot of the resulting Zipfian curve
	->Sheet2: Contains a table comparing the total number of documents retrieved per query using Lucene’s scoring function vs. using search engine (index with BM25) from the previous assignment
5. Score lists:
	Four lists (one per query) each containing at MOST 100 docIDs ranked by score with a text snippet of 200 chars along the DocID
6. external_jars: 
	Contains external jars of lucene

To run:
*******
The Project can be run using two methods:
1. Run java -jar IndexerAndRet.jar
And then follow the prompt

2. 	->Create a new project in Eclipse or NetBeans
	->Add the IndexerAndRet.java file to it
	->Add these external jars from the external_jars folder:
		lucene-analyzers-common-4.7.2.jar, 
		lucene-core-4.7.2.jar,
		lucene-queryparser-4.7.2.jar
	->Run IndexerAndRet.java file using Eclipse/NetBeans
	->Follow the prompt

Please note: In order to write TermToTF list and Score_results to file, the Path/folder should already exist.



