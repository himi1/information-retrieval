Running Guidelines:

For nbtrain.py:
python nbtrain.py --pos "textcat\train\pos" --neg "textcat\train\neg" --model "model.txt"  > Output.txt

For nbtest.py:
python nbtest.py model.txt "NaiveBaye's\textcat\test" > Output.txt

Excuting nbtrain.y generates two dictionaries containing positive and negative probabilities for each word from
the training data, stored in model.txt

Executing nbtest.py use model.txt and test data to give results for positive and negative reviews for the test data.

For Extra Credit:
1. Jelinek-Mercer smoothing technique: Uncomment the code for function prob_calc() and its calling in nbtrain.py
   and main() respectively.

2. Dirischlet smoothing technique: Uncomment the code for function prob_calc() and its calling in nbtrain.py
   and main() respectively.

For 1 and 2:

   Uncomment the following code in main():

   # Pos_Prob = prob_calc(Pos, Neg)
   # Neg_Prob = prob_calc(Neg, Pos)

   Comment out the following code in main():
   
   Pos_Prob = prob_calc(Pos)
   Neg_Prob = prob_calc(Neg)

3. Removed special characters while reading the training data and applied Dirihlet smoothing technique with it.
   For this uncomment the code in function read_train():

   #to_remove = re.compile('[' + re.escape(r'@/\[]:,.!?#;$%^&<>*-_') + ']+')   
   #j = re.sub(to_remove, '', i)
   term = i.rstrip().split()  -- change i to j

   
The ouput doesnot varies mcuh using these three techniques, output for 1,2,3 provided in JilenekMercer.txt, Dirischlet.txt,
SpecialCharacters.txt files respectively.