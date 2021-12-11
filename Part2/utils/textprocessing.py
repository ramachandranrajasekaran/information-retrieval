# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 07:15:02 2020

@author: R Ramachandran
"""

import re

"""
Remove all non words from the content
@parameter the input text content
@return non word character removed content
"""
def remove_nonwords(text):
    non_words = re.compile(r"[^a-z']")
    processed_text = re.sub(non_words, ' ', text)
    return processed_text.strip()

"""
Text processing main method to remove the non words and convert the content
into the individual words
@parameter the text content
@return the list of words
"""
def preprocess_text(text):
    processed_text = remove_nonwords(text.lower())
    words = [word for word in processed_text.split()]
    return words
