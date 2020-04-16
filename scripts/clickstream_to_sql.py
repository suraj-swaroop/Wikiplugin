#!/usr/bin/env python
# coding: utf-8

import sqlalchemy
import pandas as pd
import re
import gzip
import sys

folder = sys.argv[1] # '../download/clickstream/202001/'
file = sys.argv[2] # 'clickstream-enwiki-2020-01.tsv.gz'

path = folder+file

df = pd.read_csv(path, delimiter='\t', 
                       encoding='utf-8', names=['referer', 'resource', 'path', 'count'],compression='gzip')

# get all external link click count for resource
df_external_count = df.groupby(['resource', 'path'])['count'].sum()
df_external_count = df_external_count.reset_index()
df_external_count = df_external_count.loc[df_external_count['path'] == 'external']
df_external_count['referer'] = 'other-external'

# get all internal link click count for resource
df_internal = df.loc[df['path'] == 'link']
df_internal = df_internal.dropna()

# combine them together
df_combined = pd.concat([df_internal, df_external_count], axis=0)
df_combined = df_combined.sort_values(by=['resource', 'path', 'count']).reset_index(drop=True)

reg = re.compile(r'[^a-zA-Z0-9\-\_.]')

def preprocess(doc):
    rs = ''
    if(reg.search(doc) == None): 
        rs = doc
    return rs

# get english alphabets, numbers, -, and _ only
df_combined['resource'] = df_combined['resource'].apply(preprocess)
df_result = df_combined[df_combined['resource'].map(len) > 0]

# get date from file name
#date = file[-11:-4].replace('-', '')
start = file.find('-',12)
end = file.find('.')
date = file[start+1:end]
df_result['date'] = date

# reorder and rename the columns
df_result = df_result[['date', 'resource', 'referer', 'count']].rename(
    columns={'resource': 'title', 'referer': 'from'})
df_result = df_result.reset_index(drop=True)

# Writing to CSV
df_result.to_csv('../Outputs/clickstream/clickstream-'+date+'.csv')


# You would uncomment this if you wanted to additionally write to our database (if you had the key file). 

#with open('../database.key', 'r') as file:
#    DB_URIfix = file.read()

#engine = sqlalchemy.create_engine(DB_URIfix)
#datatypes = {
#    'Snapshot': sqlalchemy.types.INTEGER(),
#    'From': sqlalchemy.types.NVARCHAR(8000),
#    'To': sqlalchemy.types.NVARCHAR(8000),
#    'RelationType': sqlalchemy.types.NVARCHAR(50),
#    'Count': sqlalchemy.types.INTEGER()
#}

#print('writing to database')
#df.loc[start:end].to_sql('Clickstream',engine, index=False,dtype=datatypes,if_exists='append')
#pritn('done writing to database')