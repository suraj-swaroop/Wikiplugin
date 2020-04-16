#!/usr/bin/env python
# coding: utf-8

import os
import sys
import bz2
import pandas as pd
import xmltodict, nltk
import json
import re, string, ast
import numpy as np

from nltk import download, tokenize, word_tokenize 
from nltk.corpus import stopwords
from gensim.models import Word2Vec
from gensim.test.utils import get_tmpfile

# nltk.download('stopwords')
# nltk.download('punkt')

stop_words = stopwords.words('english')

def preprocess_sentence(doc):
    return tokenize.sent_tokenize(doc)

def preprocess_word(doc):
    doc = doc.lower()  # Lower the text.
    doc = word_tokenize(doc)  # Split into words.
    doc = [w for w in doc if not w in stop_words]  # Remove stopwords.
    doc = [w for w in doc if w.isalpha()]  # Remove numbers and punctuation.
    while (doc.count('n')): 
        doc.remove('n') 
    while (doc.count('br')): 
        doc.remove('br') 
    return doc

def preprocess_link(doc):
    if doc.startswith(', '):
        doc = doc[2:]
    doc = doc.split(', ')
    return doc

def get_centroid_vec(token_list):
    if len(token_list) == 0: return []
    centroid_vec = np.zeros(shape=100)
    for w in token_list:
        vec = model.wv[w]
        centroid_vec = centroid_vec + vec
    return centroid_vec/len(token_list)

# Checking a directory
def check_path(inputPath):
    try:
        if not os.path.exists(inputPath):
            print("[Warning] Create the path. Path:[{}]".format(inputPath))
            os.makedirs(inputPath)
    except OSError:
        print ("[Error] Checking the directory %s failed" % inputPath)
        sys.exit(1)


# Main
if __name__ == '__main__':   
    # Check arguments
    if len(sys.argv) < 2:
        print("[Error] Invalid inputs")
        sys.exit(1)       
        
#     date = re.search(r'(enwiki\-)(.*?)(-pages)', filepath).group(2)
#     date = '20200101'
#     filepath = '../Datasets/enwiki-'+date+'-pages-articles-multistream1.xml-p10p30302'
        
    filepath = sys.argv[1]
    date = filepath.split("-")[1]
    print("Path: {}".format(filepath))

    with bz2.open(filepath) as file:
        doc = xmltodict.parse(file.read())
    df_text = pd.DataFrame(columns=['title', 'text', 'wiki_link', 'redirect'])
    
    # Reading in each article
    for page in doc['mediawiki']['page']:
        title = page['title']
        text_w = ''
        text_s = ''
        wiki_link = ''
        redirect = 'F'

        if 'redirect' in page:
            # only keeping redirecting link
            txt = re.search('(\[\[(.*?)\]\])', page['revision']['text']['#text']).group(1)
            txt = re.sub('\[*\]*', '', txt)
            redirect = 'T'
            wiki_link = txt.strip()

        else:
            # getting rid of {{~}}, [[File:~]], <!-- ~ -->, <ref ~ />, <ref ~</ref>, <br~>
            txt = re.sub(r'({{(.*?)}})|(\[\[File:(.*?)\n)|(\<\!\-\-(.*?)\-\-\>)|(\<ref(.*?)\/\>)|(\<ref(.*?)\<\/ref\>)|(\<br(\s?\/?)\>)', 
                         '', page['revision']['text']['#text'], 0, re.DOTALL)

            # separating internal links
            link = re.findall('(\[\[(.*?)\]\])', txt)
            text_w = re.sub('(\[\[(.*?)\]\])|(\\n)', ' ', txt, 0, re.DOTALL)
            text_s = re.sub('(?<=^\[\[\b).*(?=\b\|(.*?)\]\])|(\\n)',' ',txt, 0, re.DOTALL) #keeping the links first
            text_s = re.sub('(\[\[(.*?)\]\])|(\\n)', ' ', text_s, 0, re.DOTALL)

            for c in link:
                if '|' in c[1]:
                    sep = c[1].split('|')
                    wiki_link = wiki_link + ', ' + sep[0]
                    text_w = text_w + ', ' + sep[1]
                else:
                    wiki_link = wiki_link + ', ' + c[1]
                    text_w = text_w + ', ' + c[1]

        df_text = df_text.append({'title': title, 'text': text_w, 'wiki_link': wiki_link, 'redirect': redirect, 'sentences': text_s}, ignore_index=True) 

    df_text['sentences'] = df_text['sentences'].apply(preprocess_sentence)
    df_text['text'] = df_text['text'].apply(preprocess_word)
    df_text['wiki_link'] = df_text['wiki_link'].apply(preprocess_link)

    ##Centroid Word Vector Calculation
    print('Beginning Word Vector Calculation')
    path = get_tmpfile("word2vec.model")
    model = Word2Vec(sentences = df_text['text'], min_count=0, window=2)
    df_text['centroid_vec'] =  df_text['text'].apply(get_centroid_vec)
    
    # Write CSV
    outputPath = "../Outputs/text"
    check_path(outputPath)
    
    print('Writing CSV')
    left = filepath.find('/enwiki')
    right = filepath.find('.bz2')
    outputPath = outputPath + "/" + "wikipedia_text_"+ str(filepath[left+1:right]) + ".csv"    
    
    df_text.to_csv(outputPath, index=False, header=True)
    