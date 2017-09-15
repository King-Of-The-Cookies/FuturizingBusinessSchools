#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 10:54:06 2017

@author: katerinadoyle

ANALYZE EMPLOYER REVIEW DATA

"""


#==============================================================================
# PACKAGES
#==============================================================================

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *

import os
os.chdir("/Users/katerinadoyle/Dropbox/repos/future_bus_school")

import pandas as pd
import re

from sklearn.feature_extraction.text import TfidfVectorizer

import string
from string import punctuation

#import vaderSentiment
#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#==============================================================================
# FUNCTIONS
#==============================================================================
def clean(df, column):
    nw_df = df.drop_duplicates(subset = column)
    nw_df = df.dropna(subset = [column], inplace=True)
    return nw_df

def tidy_split(df, column, sep='|', keep=False):
    """
    Split the values of a column and expand so the new DataFrame has one split
    value per row. Filters rows where the column is missing.

    Params
    ------
    df : pandas.DataFrame
        dataframe with the column to split and expand
    column : str
        the column to split and expand
    sep : str
        the string used to split the column's values
    keep : bool
        whether to retain the presplit value as it's own row

    Returns
    -------
    pandas.DataFrame
        Returns a dataframe with the same columns as `df`.
    """
    indexes = list()
    new_values = list()
    df = df.dropna(subset=[column])
    for i, presplit in enumerate(df[column].astype(str)):
        values = presplit.split(sep)
        if keep and len(values) > 1:
            indexes.append(i)
            new_values.append(presplit)
        for value in values:
            indexes.append(i)
            new_values.append(value)
    new_df = df.iloc[indexes, :].copy()
    new_df[column] = new_values
    return new_df

    
stemmer = PorterStemmer()

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    lowers = text.lower()
    no_punctuation = lowers.translate(str.maketrans('','',string.punctuation))
    tokens = nltk.word_tokenize(no_punctuation)
    stems = stem_tokens(tokens, stemmer)
    return stems

def tokenzie_nostem(text):
    lowers = text.lower()
    no_punctuation = lowers.translate(str.maketrans('','',string.punctuation))
    tokens = nltk.word_tokenize(no_punctuation)
    return tokens    


#==============================================================================
# DATA IMPORT AND FORMAT
#==============================================================================

txt_master = pd.read_csv("reviews_ind.csv",sep=";", header=None, names=("company", "review"), index_col=False)#, decode = "UTF-8") 
cons_master = pd.read_csv("cons_ind.csv", sep=";", header=None, names=["company", "con"],index_col=False, encoding = "UTF-8")
pros_master = pd.read_csv("pros_ind.csv", sep=";", header=None, names=("company", "pro"), index_col=False, encoding = "UTF-8")

#832368 text review entries, 436564 cons entries, and 452538 pro entries,
#==============================================================================
# CLEAN DATASETS
#==============================================================================

# remove duplicates
#txt = txt.drop_duplicates(subset = "review")
#txt = clean(txt_master, 'review') # error with function. doesn't return anything
txt = txt_master.drop_duplicates(subset="review")
cons = cons_master.drop_duplicates(subset = "con")
pros = pros_master.drop_duplicates(subset="pro")

# after removing duplicates 430718 text review entries, 145316 cons entries, and 154016 pro entries

#==============================================================================
# preprocessing: chunking, tokenize, stemming
#==============================================================================

# CHUNKING
# chunk entries. use punctuation, as delimiter of chunk. then tokenize ? does it matter if first chunk then tokenize?
#sep_punc = [",", ";"]
cons = tidy_split(cons_master, "con", sep=";")
cons = tidy_split(cons, "con", sep=",")
cons = tidy_split(cons, "con", sep=".")

# remove blank lines and NAs?

# TOKENIZE & STEMMING
cons_tk = [ ] 
for row in cons.iloc[:,1]:
    row_token = tokenize(row)
    cons_tk.append(row_token) #append this as column to test    

# add company name again
cons_tk_df = pd.DataFrame(cons_tk)
cons_df = pd.concat([cons, cons_tk_df], axis = 1, join_axes=[cons.index])

###########################

# CHUNKING
# chunk entries. use punctuation, as delimiter of chunk. then tokenize ? does it matter if first chunk then tokenize?
#sep_punc = [",", ";"]
pros = tidy_split(pros_master, "pro", sep=";")
pros = tidy_split(pros, "pro", sep=",")
pros = tidy_split(pros, "pro", sep=".")

# remove blank lines and NAs?

# TOKENIZE
# no stemming as stem words not part of lexicon
pros_tk = [ ] 
for row in pros.iloc[:,1]:
    row_token = tokenzie_nostem(row)
    pros_tk.append(row_token) #append this as column to test    

# add company name again
pros_tk_df = pd.DataFrame(pros_tk)
pros_df = pd.concat([pros, pros_tk_df], axis = 1, join_axes=[pros.index])

###########################

txt = tidy_split(txt_master, "review", sep=",")
txt = tidy_split(txt, "review", sep=".")

# remove blank lines and NAs?

# TOKENIZE
# no stemming as stem words not part of lexicon
txt_tk = [ ] 
for row in txt.iloc[:,1]:
    row_token = tokenzie_nostem(row)
    txt_tk.append(row_token) #append this as column to test    

# add company name again
txt_tk_df = pd.DataFrame(txt_tk)
txt_df = pd.concat([txt, txt_tk_df], axis = 1, join_axes=[txt.index])


#==============================================================================
# word frequency for pros and cons
#==============================================================================

#keywords here basis for dictionray?

#==============================================================================
# proportion pros/cons
#==============================================================================

#this gives me information about why a company is good/bad to work for

pro_grp = pd.DataFrame(pros_df['company'].value_counts())
con_grp = pd.DataFrame(cons_df['company'].value_counts())

procon_grp = pd.concat([pro_grp, con_grp], axis = 1)
procon_grp.columns=['nbr_pro', 'nbr_con']

procon_grp['prop'] = procon_grp.iloc[:,0]/procon_grp.iloc[:, 1]
procon_grp.to_csv("procon_prop.csv", sep=",", header=True, index=True)
#==============================================================================
# sentiment analysis
#==============================================================================
#sentim_analyzer = SentimentAnalyzer()
#unigram_feats = sentim_analyzer.unigram_word_feats(txt.iloc[0:100, 'review'])
#len(unigram_feats)

sid= SentimentIntensityAnalyzer()
txt_ss = [ ]
for entry in txt.loc[: ,'review']: #empty for some companies. why?
    ss = sid.polarity_scores(entry)
    txt_ss.append(ss)

# add company name again
txt_ss_df = pd.DataFrame(txt_ss)
review_sentiment = pd.concat([txt.reset_index(drop=True), txt_ss_df.reset_index(drop=True)], axis = 1) 
review_grp = review_sentiment.groupby(['company']).mean()

review_grp.to_csv("review_grp.csv", sep=",", header=True, index=True)
