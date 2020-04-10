#!/usr/bin/env python
# coding: utf-8

import sys, os
import pandas as pd
import xmltodict, nltk
import json
import re, string, ast
import numpy as np

from gensim import models
from gensim.corpora import Dictionary, MmCorpus
from nltk import download, tokenize, word_tokenize, pos_tag 
from nltk.corpus import stopwords

import pickle
nltk.download('punkt')


#Separates text into list of words
def tokenize_text(s):
    line = re.sub('[!@#$]', '', s)
    tokenize = word_tokenize(line)
    result_list = []
    for j in tokenize:
        result = j.split('"=')
        result = re.sub('[\W_]+', '', j)
        result_list.append(result)
        result_list = [x for x in result_list if x]
        #result = ' '.join(result_list)
    return result_list


def nltk_stopwords():
    return set(nltk.corpus.stopwords.words('english'))


#builds dictionary and corpus based on article texts
def prep_corpus(docs, additional_stopwords=set(), no_below=1, no_above=0.5):
    print('Building dictionary...')
    dictionary = Dictionary(docs)
    stopwords = nltk_stopwords().union(additional_stopwords)
    stopword_ids = map(dictionary.token2id.get, stopwords)
    dictionary.filter_tokens(stopword_ids)
    dictionary.compactify()
    dictionary.filter_extremes(no_below=no_below, no_above=no_above, keep_n=None)
    dictionary.compactify()

    print('Building corpus...')
    corpus = [dictionary.doc2bow(doc) for doc in docs]
    return dictionary, corpus


#returns model, dictionary and corpus
def model_all():
    dictionary, corpus = prep_corpus(df_text['text_tokens'])
    MmCorpus.serialize('wiki_articles.mm', corpus)
    dictionary.save('wiki_articles_new.dict')
    lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=5, passes=50)
    return lda, dictionary, corpus


# Checking a directory
def check_path(inputPath):
    try:
        if not os.path.exists(inputPath):
            print("[Warning] Create the path. Path:[{}]".format(inputPath))
            os.makedirs(inputPath)
    except OSError:
        print ("[Error] Checking the directory %s failed" % inputPath)
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("[Error] Invalid inputs")
        sys.exit(1)       
        
    filepath = sys.argv[1]
    date = filepath.split("_")[1]
    print("Path: {}".format(filepath))
    
    # Create a dataframe
    df_text = pd.read_csv(filepath)
    df_text['text_tokens'] = df_text['text'].apply(tokenize_text)
    df_text['text_clean'] = df_text['text_tokens'].apply(lambda x: ' '.join(x))

#     #Building LDA Model
#     print('Building LDA model')
#     lda, dictionary, corpus = model_all()
    
#     print('Saving Model')
#     file = open('lda.pkl', 'wb')
#     pickle.dump(lda, file)
#     file.close()

#     print('Saving Dictionary')
#     file = open('dictionary.pkl', 'wb')
#     pickle.dump(dictionary, file)
#     file.close()

    # Reading dictionary and model files:
    print("Loading lda model")
    with open('lda.pkl', 'rb') as f:
        lda = pickle.load(f)

    print("Loading dictionary")
    with open('dictionary.pkl', 'rb') as f:
        dictionary = pickle.load(f)
    
    #Adding topic distribution to dataframe
    print('Calculating topics for each article')
    mm = [dictionary.doc2bow(text) for text in df_text['text_tokens']]
    topics = pd.DataFrame(dict(lda[x]) for x in mm)
    df_text['topics'] = topics.values.tolist()
    df_text['topics'].loc[df_text['redirect']== 'T'] = '[]'
    
    #Write to CSV
    print('Writing to CSV')
    outputPath = "../Outputs/modelling/"
    check_path(outputPath)
    df_text.to_csv(outputPath + "topic_modelling-" + date + ".csv")
