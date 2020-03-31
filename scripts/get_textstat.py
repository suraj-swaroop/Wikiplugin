#!/usr/bin/env python
# coding: utf-8

# ETL script for textstat metrics on the text of each wikipedia article: 
# (textstat is a python package that calculates various metrics on sentence
# complexity, such as the Dale–Chall formula, or the Flesch Reading Ease score) 

import os
import sys, re
import textstat
import pandas as pd

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


# Checking a directory
def check_path(inputPath):
    try:
        if not os.path.exists(inputPath):
            print("[Warning] Create the path. Path:[{}]".format(inputPath))
            os.makedirs(inputPath)
    except OSError:
        print ("[Error] Checking the directory %s failed" % inputPath)
        sys.exit(1)
        
        
def main(filepath):
    article_df = pd.read_csv(filepath, delimiter=',', encoding='utf-8')

    # Set language: English
    textstat.set_lang("en")
    
    temp_df = article_df.apply(lambda x: textstat_stats(x['text']), axis=1)
    textstat_df = pd.concat([article_df, temp_df], axis=1, sort=False)

    # Save output
    outputPath = "../Outputs/textstat/"
    check_path(outputPath)
    
    left = filepath.find('_')
    right = filepath.find('.csv')
    outputPath = outputPath + "textstat_"+ str(filepath[left+1:right]) + ".csv"    
    
    # Get text stat data
    textstat_df.to_csv(outputPath, index=False, header=True)
    

if __name__ == '__main__':
    # Check arguments
    if len(sys.argv) < 2:
        print("[Error] Invalid inputs")
        sys.exit(1)       
        
    filepath = sys.argv[1]
    print("Path: {}".format(filepath))
    
    main(filepath)    
    