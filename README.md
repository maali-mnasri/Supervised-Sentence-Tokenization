# Supervised-Sentence-Tokenization
A supervised tool to detect sentence boundaries.

This sentence tokenizer is trained on labelled data consistong of raw text where we know where sentence boundaries are.
For research and test purpose, the model has been trained on a sample of the PennTreebank.

# Feature engineering and Training setting

The training data consists of trigrams formed of two words separated by a separator (e.g. point). Each trigram has a additional binary label:
  - 0 means the point in this trigram is not a sentence boundary
  - 1 means the point in this trigram is a sentence boundary
  
The training model uses multiple features such as the lengths of the previous/next words, if next/previous is in capital letters, etc.
  
The machine learning algorithm is SVM with linear kernel.
  
# Evaluation

The extracted trigrams were about 6376 trigrams divided into 80% for training and 20% for test.
The model reached 98% of F-measure (precision+recall).

# How to train the model
While you can use the pretrained model in /data, you can train your own model on your own data.
To this end, you should create a csv training file that holds in each line a tab separated trigram and the label indicating if it is a sentence boundary.
You can follow the sample trigrams file in /data.
The script I used to create the training file from a PennTreeBank formatted data is in /src : CreateTrainTest.py
In /data you can also find a sample of the initial tagged text data from the PennTreeBank : see raw_data_sample.json but you can find the sample I used here : https://github.com/nlp-compromise/penn-treebank/blob/master/penn-data.json

Now, to train the SVM model you just need to run:

python3 TrainSBModel.py --tf trainingfile-path --testsize test-size-percentage

where trainingfile-path is the path to your training file and size-percentage is the percentage of the data you want to keep for test? it should be between 0.1 and 0.9

The trained model is persisted in the /data folder

# Run the sentence tokenizer

python3 SentenceTokenizer.py --text "the text you want to segment into sentence"

The output is printed one sentence per line and you can also import the SentenceTokenizer script as a module and get the sentences into a list:

from SentenceTokenizer import sentence_tokenizer
sentences = sentence_tokenizer(text)

# TO DO

Train the model using additional separators such as '!' and '?'

# References
This work is highly inspired by (Agarwal et al.,2005) and (Gillick,2009) works.

AGARWAL, Neha, FORD, Kelley Herndon, et SHNEIDER, Max. Sentence boundary detection using a maxEnt classifier. In : Proceedings of MISC. 2005. p. 1-6.

GILLICK, Dan. Sentence boundary detection and the problem with the US. In : Proceedings of Human Language Technologies: The 2009 Annual Conference of the North American Chapter of the Association for Computational Linguistics, Companion Volume: Short Papers. 2009. p. 241-244.

