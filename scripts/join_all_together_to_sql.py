#!/usr/bin/env python
# coding: utf-8

import pandas as pd

date = '20200101'

df_textstat = pd.read_csv('Results/textstat-'+date+'.csv')

#Reading in all necessary datasets
df_textstat = df_textstat
df_topics = pd.read_csv('Results/topic_modelling-'+date+'.csv')
df_clickstream = pd.read_csv('Results/clickstream-'+date[:-2]+'.csv')
df_clickstream = df_clickstream.groupby('title').sum()
df_complexity = pd.read_csv('../Datasets/complexity_samples.csv')
df_complexity = df_complexity.drop(columns=['link', 'assigned to'])
df_graph = pd.read_csv('Results/graphical_metrics.csv').rename(columns={'Article':'title'})

#Joining all datasets
print('Joining Datasets')
df_joined = df_topics.join(df_textstat.set_index('title'), on='title', lsuffix='_topics', rsuffix='_textstat')
df_joined = df_joined.join(df_clickstream, on='title', rsuffix='_clickstream')
df_joined = df_joined.join(df_complexity.set_index('title'), on='title', rsuffix ='_complexity')
df_joined = df_joined.join(df_graph.set_index('title'), on='title', rsuffix='_graph')

#Building new dataset
columns = ['Snapshot', 'Article', 'Article Vector Centroid', 'Article Topics Distributions', 'TextStat Fleisch Reading Difficulty', 'Eigenvector Centrality', 'Louvain Community', 'Clicks in month', 'Article Length', 'Target Complexity']
df_new = pd.DataFrame(columns = columns)

#Getting all necessary columns
df_new['Article'] = df_joined['title']
df_new['Article Vector Centroid'] = df_joined['centroid_vec_topics']
df_new = df_new.assign(Snapshot = date[:-2])
df_new['Article Topics Distributions'] = df_joined['topics']
df_new['TextStat Fleisch Reading Difficulty'] = df_joined['difficulty']
df_new['Eigenvector Centrality'] = df_joined['EigenvectorCentrality']
df_new['Louvain Community'] = df_joined['CommunityID']
df_new['Clicks in month'] = df_joined['count']
df_new['Article Length'] = df_joined['text_topics'].apply(lambda x: len(x))
df_new['Target Complexity'] = df_joined['score']

#Writing to CSV
print('Writing to CSV')
df_new.to_csv('Results/article_summary-'+date[:-2]+'.csv')

#Saving to MySQL Format
# from pandas.io import sql
# import MySQLdb

# con = MySQLdb.connect()
# df_new.to_sql(con=con, name='article_summary-'+date[:-2], if_exists='replace', flavor='mysql')