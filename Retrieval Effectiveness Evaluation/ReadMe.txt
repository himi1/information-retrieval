# To run: 
python evaluate.py cacm.rel results.eval > output.txt

cacm.rel: contains relevance judgements for the CACM test collections
results.eval: contains the result obtained from hw3 or hw4
(Note: The query ID in result.eval should match the query id of same query in cacm.rel)
output.txt: Contains the final output values for each query, including:
1. P@100
2. P@20
3. Ap_count(Average precision)
4. Retrieval effectiveness Table
And finally the MAP for all queries in last line.

A new file is also created called evaluation_results, which just contains the following:
1. P@100 for each query
2. P@20 for each query
3. MAP for all the queries