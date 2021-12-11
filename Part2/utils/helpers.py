# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 07:15:02 2020

@author: R Ramachandran
"""

import os
from collections import defaultdict
import math

"""
======================Remove====================================
def get_stopwords(stopwords_file):
    with open(stopwords_file, mode='r') as f:
        stopwords = set(f.read().split())
    return stopwords
"""

"""
Get all the doc file names from the mentioned path
@parameter the dataset location
@return list of docs file name
"""
def get_docs(dataset_path):
    docs = []
    for doc_file in os.listdir(dataset_path):
        docs.append(os.path.join(dataset_path, doc_file))
    return docs

"""
Method to calculate the inverse document frequency of the corpus
@parameter the entire corpus
@return the inverse document frequency of each word in as dict
"""
def compute_idf(corpus):
    num_docs = len(corpus)
    idf = defaultdict(lambda: 0)
    for doc in corpus:
        for word in doc.keys():
            idf[word] += 1

    for word, value in idf.items():
        idf[word] = math.log(num_docs / value)
    return idf

"""
Method to conpute the tf-idf value i.e. term frequency - inverse document frequency
@parameter the idf and the doc
@return the doc updated with the tf-idf value
"""
def compute_weights(idf, doc):
    for word, value in doc.items():
        doc[word] = idf[word] * (1 + math.log(value))


"""
To calculate the lenght of each document and also the query
@parameter the doc
@return the doc updated with the lenght
"""
def normalize(doc):
    denominator = math.sqrt(sum([e ** 2 for e in doc.values()]))
    for word, value in doc.items():
        doc[word] = value / denominator

"""
To build the inverted index with idf value and posting values
@parameter idf and the corpus
@return the inverted index dict
"""
def build_inverted_index(idf, corpus):
    inverted_index = {}
    for word, value in idf.items():
        inverted_index[word] = {}
        inverted_index[word]['idf'] = value
        inverted_index[word]['postings_list'] = []

    for index, doc in enumerate(corpus):
        for word, value in doc.items():
            inverted_index[word]['postings_list'].append([index, value])

    return inverted_index
