# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 07:15:02 2020

@author: R Ramachandran
@id: 2019ht12107
"""

import pickle
import os
import math
from utils import textprocessing
from utils import helpers
from collections import Counter

def get_doc_number(docs, num):
    print(os.path.splitext(os.path.basename(docs[num]))[0])
    

# To read the docs, inverted index and dictionary files
docs_file = os.path.join(os.getcwd(), 'data', 'docs.pickle')
inverted_index_file = os.path.join(os.getcwd(), 'data', 'inverted_index.pickle')

# Read the data from the already saved files inverted index and docs file names
with open(docs_file, 'rb') as f:
    docs = pickle.load(f)
with open(inverted_index_file, 'rb') as f:
    inverted_index = pickle.load(f)

# Get words from the inverted index
dictionary = set(inverted_index.keys())

# Get query from command line
query = input("Enter the query: ")

# Preprocess query
query = textprocessing.preprocess_text(query)
query = [word for word in query if word in dictionary]
query = Counter(query)

# Compute weights for words in query
for word, value in query.items():
    query[word] = inverted_index[word]['idf'] * (1 + math.log(value))

helpers.normalize(query)

# Compute the scores based on word idf and query idf value
scores = [[i, 0] for i in range(len(docs))]
for word, value in query.items():
    for doc in inverted_index[word]['postings_list']:
        index, weight = doc
        scores[index][1] += value * weight

# Sort the score in descending order
scores.sort(key=lambda doc: doc[1], reverse=True)

# Print the top 10 file name and scores
print('----- Results ------ ')
print_count = 1
#print("{}. {} - {}".format("SNo", "Doc#", "Score"))
print("{} - {}".format("Document Title #", "Score"))
for index, score in enumerate(scores):
    if score[1] == 0:
        break
    print('{}\t{}'.format('Document Title ' + os.path.splitext(os.path.basename(docs[score[0]]))[0], score[1]))
    #print('{}'.format('Document Title ' + os.path.splitext(os.path.basename(docs[score[0]]))[0]))
    #print('{}'.format(score[1]))
    if print_count == 10:
        break
    print_count = print_count + 1