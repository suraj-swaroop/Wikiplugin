#!/usr/bin/env python
# coding: utf-8

# ETL script for textstat metrics on the text of each wikipedia article: 
# (textstat is a python package that calculates various metrics on sentence
# complexity, such as the Dale–Chall formula, or the Flesch Reading Ease score) 

import pandas as pd
import textstat
import sys, re
# https://pypi.org/project/textstat/

# Need to install textstat
#get_ipython().system('pip install textstat')



# Input: text
# Output: textstat outputs
def textstat_stats(text):
    difficulty = textstat.flesch_reading_ease(text)
    grade_difficulty = textstat.flesch_kincaid_grade(text)
    gfog = textstat.gunning_fog(text)
    smog = textstat.smog_index(text)
    ari = textstat.automated_readability_index(text)
    cli = textstat.coleman_liau_index(text)
    lwf = textstat.linsear_write_formula(text)
    dcrs = textstat.dale_chall_readability_score(text)
    idx = ['difficulty', 'grade_difficulty','gfog','smog','ari','cli','lwf','dcrs']

    return pd.Series([difficulty, grade_difficulty, gfog, smog, ari, cli, lwf, dcrs], index=idx)

if __name__ == '__main__':
#     if len(sys.argv) < 1:
#         print("[Error] Invalid input")
#         sys.exit(1)

#     filepath = sys.argv[1]
#     date = re.search(r'(preprocess)(.*?)(\.csv)', filepath).group(2)
    
    date = '20200101'
    filepath = 'Results/preprocess-'+date+'.csv'
    article_df = pd.read_csv(filepath, delimiter=',', encoding='utf-8')

    # Set language: English
    textstat.set_lang("en")
    
    temp_df = article_df.apply(lambda x: textstat_stats(x['text']), axis=1)
    textstat_df = pd.concat([article_df, temp_df], axis=1, sort=False)

    # Save output
    textstat_df.to_csv (r'Results/textstat-'+date+'.csv', index = False, header=True)