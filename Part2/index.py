# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 07:15:02 2020

@author: R Ramachandran
"""

import os
import sys
import pickle
from collections import Counter
from bs4 import BeautifulSoup
from utils import textprocessing, helpers

file = "C:/Users/Ramji/BITS/SEMESTER_2/Information Retrieval (SSZG537)/Assignment/AI/wiki_00"

"""
Read content from the file
@parameter the file name
@return the content of the file
"""
def read_file(file):
    f = open(file, "r", encoding="utf8")
    content = f.read()
    return content

"""
Extract content from doc tag, it also extracts words from the link tag
like "a" and "href" tag
@parameter the file content
@return the list with doc content in it
"""
def extract_doc(content):
    doc_list = []
    doc_content = BeautifulSoup(content, 'html.parser')
    find_result = doc_content.findAll("doc")
    for doc in find_result:
        doc_list.append(doc.text)
    return doc_list

"""
Write extracted data from wiki_00 file as seperate documents for easy processing
The files are stored as doc_num.txt file ex. 1.txt
@parameter the document list extracted from wiki_00 file and path in which docs should be stored
"""
def write_doc_to_files(doc_list, doc_path):
    doc_num = 1
    for doc in doc_list:
        with open(doc_path + '\\' + str(doc_num), "w", encoding="utf-8") as f:
            f.write(doc)
            f.close()
            doc_num = doc_num + 1 

"""
Indexing process starts here
__main__ method
"""
print('Indexing....')

dataset_path = os.path.join(os.getcwd(), 'docs')
data_path = os.path.join(os.getcwd(), 'data')

if not os.path.exists(data_path):
    os.mkdir(data_path)

if not os.path.exists(dataset_path):
    os.mkdir(dataset_path)

wiki_file_path = os.path.join(os.getcwd(), 'wikifiles')

if not os.path.exists(wiki_file_path):
    sys.exit(1)
    
# Extract the wiki_00 file content and convert it to doc files
files = helpers.get_docs(wiki_file_path)
file_content = ""
for file in files:
    file_content = file_content + read_file(file)
doc_content_list = extract_doc(file_content)
write_doc_to_files(doc_content_list, dataset_path)

# Read the documents list
docs = helpers.get_docs(dataset_path)

# For each documents convert the doc content to words. Also remove the non words from corpus
corpus = []
for doc in docs:
    with open(doc, mode='r', encoding="utf-8") as f:
        text = f.read()
        words = textprocessing.preprocess_text(text)
        bag_of_words = Counter(words)
        corpus.append(bag_of_words)

# Compute the idf of the corpus
idf = helpers.compute_idf(corpus)

# Find the tf-idf of the words and save it in the dict
for doc in corpus:
    helpers.compute_weights(idf, doc)
    helpers.normalize(doc)

# Create the inverted index with tf-idf and posting list
inverted_index = helpers.build_inverted_index(idf, corpus)

# Save the doc file name, inverted index and dictionary words in respective files
docs_file = os.path.join(data_path, 'docs.pickle')
inverted_index_file = os.path.join(data_path, 'inverted_index.pickle')
dictionary_file = os.path.join(data_path, 'dictionary.txt')

# Serialize data
with open(docs_file, 'wb') as f:
    pickle.dump(docs, f)

with open(inverted_index_file, 'wb') as f:
    pickle.dump(inverted_index, f)

with open(dictionary_file, 'w') as f:
    for word in idf.keys():
        f.write(word + '\n')

print('Index done.')
