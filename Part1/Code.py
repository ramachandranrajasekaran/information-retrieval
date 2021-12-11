# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 10:24:52 2020

@author: R Ramachandran
"""

'''
Run the below in cmd prompt if getting error when invoking stopwords 
>>> import nltk
>>> nltk.download('stopwords')
Run the below command in the cmd prompt if you are getting error while
tokenazing throws error
>>> import nltk
>>> nltk.download('punkt')
'''

import os
import sys
import nltk
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from string import punctuation
from nltk.corpus import stopwords
from nltk import FreqDist
from nltk.stem import PorterStemmer 
import pandas as pd
import matplotlib.pyplot as plt
import re
import math



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

# Stopword list also included "", `` & '' in the list which was not by default available
# Used nltk.corpus library to get the stopwords and string library for punctuation
stoplist = set(stopwords.words('english') + list(punctuation) + ['""', '``', "''"] + ['href','also','one','first','new','world','two','states','time','th','many','used','would','may'])

# Get wiki file names from the wikifiles location
wiki_file_path = os.path.join(os.getcwd(), 'wikifiles')
if not os.path.exists(wiki_file_path):
    sys.exit(1)
files = get_docs(wiki_file_path)

# check and create "output" directory
output_file_path = os.path.join(os.getcwd(), 'output')
if not os.path.exists(output_file_path):
    os.mkdir(output_file_path)
    
# Read File Content
def read_file_content(files):
    content = ""
    for file in files:
        f = open(file, "r", encoding="utf8")
        content = content + f.read()
    return content

# Extract content from docs in the file using BeautifulSoup Library
# This also removes link tags (i.e. "a" & "href")
def extract_doc(content):
    doc_list = []
    doc_content = BeautifulSoup(content, 'html.parser')
    find_result = doc_content.findAll("doc")
    for doc in find_result:
        doc_list.append(doc.text)
    return doc_list

# To tokenize the text in each document. Used the nltk.tokenize library
def doc_tokenization(doc_list):
    tokenized_doc_list = []
    for doc in doc_list:
        tokenized = word_tokenize(doc)
        tokenized_doc_list.append(tokenized)
    return tokenized_doc_list

# To extract tokens from the docs
def create_tokens(docs):
    return [token for token in nltk.word_tokenize(docs) if token.lower() not in stoplist]

# Method to tokenzise word and remove the stopwords
# Get the ngram using the nltk library
def extract_ngrams(tokens, num):
    words = list(ngrams(tokens, num))
    return words

# Find the frequency of occurance of the word in the corpus
def get_frequence(docs, num):
    doc_frequency_object = FreqDist(docs)
    doc_frequency = doc_frequency_object.most_common()
    return doc_frequency, doc_frequency_object

# To find the total unique n-grams and save the result in a file
def get_dict_length(doc_word_feq_list):
    doc_num=1
    with open(output_file_path + 'unigram.txt', 'w') as f:
        for doc in doc_word_feq_list:
            print("Doc: {}; Total Unique n-grams: {}".format(doc_num, len(doc)), file=f)
            doc_num = doc_num + 1
    return len(doc_word_feq_list)

# Plot the graph using the pandas and mapplot libraries
# Saved each file based on the document number in the file
def plot_graph_dep(doc_frequency_list):
    doc_num=1
    for doc in doc_frequency_list:
        print("Doc Num: {}".format(doc_num))
        new_list = []
        for bg, count in doc:
            new_list.append((bg[0], count))
        df = pd.DataFrame(new_list, columns =['Word', 'Frequency']) 
        df.plot(kind='barh',x='Word',y='Frequency', figsize=(10,20))
        plt.savefig(output_file_path + str(doc_num) + '.png')
        doc_num=doc_num+1

# To merge docs
def merge_doc_words(docs):
    merged_doc = ""
    for doc in docs:
        merged_doc = merged_doc + doc
    return merged_doc

# To convert the docs content to lower cases
def convert_to_lower(docs):
    return docs.lower()

# To remove "website: " content from the corpus
def remove_website_tag(doc):
    return re.sub(r'website: https?:\/\/.*[\r\n]*', '', doc, flags=re.MULTILINE)

# To get word frequency
def get_count(word_frequency):
    return len(word_frequency)

# To plot graph
def plot_graph(freq_dist, n_gram):
    x = []
    y = []
    for index, (val,freq) in enumerate(freq_dist):
        x.append(math.log10(index+1))
        y.append(math.log10(freq))
    
    plt.figure(n_gram)
    plt.xlabel('Log(rank)')
    plt.ylabel('log(frequency)')
    plt.suptitle('log(Frequency) vs log(rank)')
    plt.plot(x,y)
    
def plot_graph_ngram_docs(ngram_docs, n_gram, state):
    x = []
    y = []
    freq_dist = nltk.FreqDist(ngram_docs)
    for index, (val,freq) in enumerate(freq_dist.most_common(100)):
        x.append(math.log10(index+1))
        y.append(math.log10(freq))
    
    plt.figure(n_gram)
    plt.xlabel('Log(rank)')
    plt.ylabel('log(frequency)')
    plt.suptitle('log(Frequency) vs log(rank)')
    plt.plot(x,y)
    plt.savefig(output_file_path + '\\' + state + '_' + str(n_gram) + '.png')   

# Depricated - Dont Use this method
def most_frequnent_ngrams(ngram_docs, total_word_count, percentage_coverage):
    coverage_count = int(total_word_count*(percentage_coverage/100))
    freq_dist_coverage = FreqDist(ngram_docs).most_common(coverage_count)
    return len(freq_dist_coverage)

# To find the unique n-grams which covers 90% of the complete corpus
def find_ninty_percent_count(fdist, percentage):
    frequencies = fdist.values()
    total_words = sum(frequencies)
    ninty_percent = int(total_words*(percentage/100))
    
    count = 0
    threshold = 0
    for words, freq in fdist.items():
        if not threshold > ninty_percent:
            count = count + 1
            threshold = threshold + freq
    return count
    
def stemming_tokens(tokens):
    stemmed_tokens = []
    ps = PorterStemmer() 
    for word in tokens:
        stemmed_tokens.append(ps.stem(word))
    return stemmed_tokens
    
# Main method / implementation
for n_gram in [1,2,3]:
    content = read_file_content(files)
    doc_list = extract_doc(content)
    merged_docs = merge_doc_words(doc_list)
    docs_lower_case = convert_to_lower(merged_docs)
    docs_content = remove_website_tag(docs_lower_case)
    tokens = create_tokens(docs_content)
    ngram_docs = extract_ngrams(tokens, n_gram)
    freq_dist, freq_dist_obj = get_frequence(ngram_docs, n_gram)
    
    # Question 1, 2 & 3 - part (a)
    print("Unique {}-grams: {}".format(n_gram, get_count(freq_dist)))
    #plot_graph(freq_dist, n_gram)
    
    # Question 1, 2 & 3 - part (b)
    plot_graph_ngram_docs(ngram_docs, n_gram, "before")
    
    # Question 1, 2 & 3 - part (c)
    ninty_percent_converage = find_ninty_percent_count(freq_dist_obj, 90)
    print("Most frequent {}-grams required to cover the 90% of the complete corpus: {}".format(n_gram, ninty_percent_converage))
    
    # After stemming ---------------------------------------------------------
    stemmed_tokens = stemming_tokens(tokens)
    ngram_docs = extract_ngrams(stemmed_tokens, n_gram)
    freq_dist, freq_dist_obj = get_frequence(ngram_docs, n_gram)

    # Question 1, 2 & 3 - part (a)
    print("After Stemming: Unique {}-grams: {}".format(n_gram, get_count(freq_dist)))
    #plot_graph(freq_dist, n_gram)
    
    # Question 1, 2 & 3 - part (b)
    plot_graph_ngram_docs(ngram_docs, n_gram, "after")
    
    # Question 1, 2 & 3 - part (c)
    ninty_percent_converage = find_ninty_percent_count(freq_dist_obj, 90)
    print("After Stemming: Most frequent {}-grams required to cover the 90% of the complete corpus: {}".format(n_gram, ninty_percent_converage))    
    #print(get_dict_length(word_frequency_list))
    #plot_graph(word_frequency_list)
