'''This is a file to run topic modelling on wikipedia articles
	Before you run this code make sure to pip install the below libraries
	1. xmltodict			2.nltk			3.gensim   '''

import pandas as pd
import xmltodict, nltk
import json
import re, string, ast
import numpy as np

from gensim import models
from gensim.corpora import Dictionary, MmCorpus
from nltk import download, tokenize, word_tokenize, pos_tag 
from nltk.corpus import stopword
nltk.download('punkt')


def filter_words(text):
    '''Given a string of text, tokenize the text and pull out only the nouns, adverbs and adjectives'''
    is_noun = lambda pos: pos[:2] == 'NN' or pos[:2] == 'JJ' or pos[:2] == 'RB'
    tokenized = word_tokenize(text)
    all_nouns = [word for (word, pos) in pos_tag(tokenized) if is_noun(pos)]
    return ' '.join(all_nouns)

def nltk_stopwords():
    return set(nltk.corpus.stopwords.words('english'))

def prep_corpus(docs, additional_stopwords=set(), no_below=1, no_above=0.5):
    #building the dictionary
    dictionary = Dictionary(docs)
    stopwords = nltk_stopwords().union(additional_stopwords)
    stopword_ids = map(dictionary.token2id.get, stopwords)
    dictionary.filter_tokens(stopword_ids)
    dictionary.compactify()
    dictionary.filter_extremes(no_below=no_below, no_above=no_above, keep_n=None)
    dictionary.compactify()

    # building the dictionary
    corpus = [dictionary.doc2bow(doc) for doc in docs]

    return dictionary, corpus

def model_all():
    dictionary, corpus = prep_corpus(tokens_df['tokens'])
    MmCorpus.serialize('wiki_articles.mm', corpus)
    dictionary.save('wiki_articles.dict')
    lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=3, passes=50)
    lda.save('anarchism_all.model')
    lda.show_topics(formatted=False)

def model_single():
    single_topic_list = []
    for i in range(0,len(tokens_df['tokens'])):
        x = pd.DataFrame(tokens_df['tokens'][i], columns=['title'])
        x['tokenized_tokens'] = x['title'].apply(word_tokenize)
        dictionary, corpus = prep_corpus(x['tokenized_tokens'])
        print(dictionary)
        MmCorpus.serialize('wiki_articles.mm', corpus)
        dictionary.save('wiki_articles.dict')
        lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=3, passes=50)
        lda.save('anarchism_single.model')
        single_topic_list.append(lda.show_topics(formatted=False))


if __name__ == '__main__':
#Picks out nouns, adverbs, adjectives and removes unwanted characters of each sentence for each article
final_ls = []
for i in range(0, len(df_text)):
    fil_sent = df_text['sentences'][i]
    sen_list = []
    for j in range(0,len(fil_sent)):
        b = filter_words(fil_sent[j])
        res = re.sub('['+string.punctuation+']', '', b).split()
        listToStr = ' '.join([str(val) for val in res])
        sen_list.append(listToStr)
    listToStr2 = ' '.join([str(val) for val in sen_list])
    final_ls.append(listToStr2)
df_text['tokens'] = final_ls 

#Selects all the unique sentences and removes any null values
unique_tokens = df_text['tokens'].unique()
unique_tokens = [x for x in unique_tokens if x]
tokens_df = pd.DataFrame(unique_tokens, columns = ['tokens'])

#tokenizes the words to be used in the model
tokens_df['tokens'] = tokens_df['tokens'].apply(word_tokenize)

model_single() #performs topic modelling on each article
model_all() #performs topic modelling on all the articles
