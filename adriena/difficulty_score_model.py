import pandas as pd
import numpy as np
import sys,re, pickle, nltk
from nltk import word_tokenize
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import Binarizer

nltk.download('punkt')

df = pd.read_csv('../Outputs/Summary/article_summary-202001.csv') #reads the summary data

df['Article Topics Distributions'] = df['Article Topics Distributions'].apply(lambda x:x[1:-1].split(','))
df['Articles Vector Centroid'] = df['Article Vector Centroid'].apply(lambda x:x[1:-1].split())

df[['ATD_1','ATD_2','ATD_3', 'ATD_4','ATD_5']] = pd.DataFrame(df['Article Topics Distributions'].values.tolist(), index= df.index).replace('nan', '0').replace(' nan', '0').apply(pd.to_numeric)
df_avc = pd.DataFrame(df['Articles Vector Centroid'].values.tolist(), index= df.index).add_prefix('AVC_')
df = pd.concat([df, df_avc[:]], axis=1)
df = df.drop(['Article Topics Distributions','Articles Vector Centroid'],axis=1)

df['Degree'].fillna(0, inplace=True)
df['Betweenness Centrality'].fillna(0, inplace=True)
df['Clicks in month'].fillna(0, inplace=True)
df = df[df['Article Vector Centroid'] != '[]']

df_train = df[df['Target Complexity'] >= 0]

def targetify(col):
    if col == 2 or col == 3:
        return 1
    else:
        return 0
    
df_train['Target Complexity'] = df['Target Complexity'].apply(targetify)

features  = [c for c in df.columns]
features.remove('Unnamed: 0')
features.remove('Snapshot')
features.remove('Article')
features.remove('Article Vector Centroid')
features.remove('Target Complexity')

X = df_train[features]
y = df_train['Target Complexity']

scaler = MinMaxScaler(feature_range=(0, 1))
scaler.fit(X[['Article Length', 'Clicks in month']])

X[['Article Length', 'Clicks in month']] = scaler.transform(X[['Article Length', 'Clicks in month']])
model = LogisticRegression().fit(X, y)
pickle.dump(model, open('../Outputs/model/complexity_model.sav', 'wb'))

df[['Article Length', 'Clicks in month']] = scaler.transform(df[['Article Length', 'Clicks in month']])
df['proba'] =  model.predict_proba(df[features])[:,1]

df_sorted = df.sort_values(by='proba', ascending=False)

df_sorted.to_csv('../Outputs/probabilities.csv')