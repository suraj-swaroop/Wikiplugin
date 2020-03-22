#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import xmltodict
import json
import re, string
import nltk
from nltk import download
from nltk import word_tokenize
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')
stop_words = stopwords.words('english')


def preprocess(doc):
    doc = doc.lower()                               # Lower the text.
    doc = word_tokenize(doc)                        # Split into words.
    doc = [w for w in doc if not w in stop_words]   # Remove stopwords.
    doc = [w for w in doc if w.isalpha()]           # Remove numbers and punctuation.
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



df_click = pd.read_csv('Datasets/clickstream-enwiki-2020-01.tsv', delimiter='\t', encoding='utf-8', names=['referer', 'resource', 'path', 'count'])


with open('Datasets/enwiki-20200101-pages-articles-multistream-index1.txt-p10p30302', encoding='utf8') as file:
    data_index = file.read()


with open('Datasets/enwiki-20200101-pages-articles-multistream1.xml-p10p30302', encoding='utf8') as file:
    #data_text = file.read()
    doc = xmltodict.parse(file.read())


df_text = pd.DataFrame(columns=['title', 'text', 'wiki_link', 'redirect'])

for page in doc['mediawiki']['page']:
    title = page['title']
    text = ''
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
        text = re.sub('(\[\[(.*?)\]\])|(\\n)', ' ', txt, 0, re.DOTALL)
        
        for c in link:
            if '|' in c[1]:
                sep = c[1].split('|')
                wiki_link = wiki_link + ', ' + sep[0]
                text = text + ', ' + sep[1]
            else:
                wiki_link = wiki_link + ', ' + c[1]
                text = text + ', ' + c[1]
                
    df_text = df_text.append({'title': title, 'text': text, 'wiki_link': wiki_link, 'redirect': redirect}, ignore_index=True)
    


df_text['text'] = df_text['text'].apply(preprocess)

df_text['wiki_link'] = df_text['wiki_link'].apply(preprocess_link)



# I think an excel cell has a limitation to word count. When it's too long, it overflows. You better use df directly instead of csv
df_text.to_csv (r'Results/article_text1.csv', index = False, header=True)


with open('Datasets/pageviews-20200101-000000', encoding='utf8') as file:
    data_view = file.read()
