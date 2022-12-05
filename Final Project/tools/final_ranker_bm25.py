# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 18:22:52 2022

@author: Rushs
"""

#Okapi BM25 ranker

from rank_bm25 import BM25Okapi
import requests
import json

corpus = [
    "Hello there good man!",
    "It is quite windy in London",
    "How is the weather today?"
]

tokenized_corpus = [doc.split(" ") for doc in corpus]

bm25 = BM25Okapi(tokenized_corpus)
# <rank_bm25.BM25Okapi at 0x1047881d0>

query = "windy London"
tokenized_query = query.split(" ")

doc_scores = bm25.get_scores(tokenized_query)
# array([0.        , 0.93729472, 0.        ])

print(bm25.get_top_n(tokenized_query, corpus, n=1) )

# bm25.get_top_n(tokenized_query, corpus, n=1)
# where n = the number of search results returned
# ['It is quite windy in London']

