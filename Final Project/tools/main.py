# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 20:14:05 2022

@author: Rushs
"""
import pandas as pd
import csv
from rank_bm25 import *
from rank_bm25 import BM25Okapi
#adding words to stopwords
from nltk.tokenize import word_tokenize
from gensim.parsing.preprocessing import STOPWORDS
import pybomb

#%%

my_key = ""

#%%


def spl_chars_removal(lst):
    lst1=list()
    for element in lst:
        str=''
        str = re.sub('[⁰-9a-zA-Z]',' ',element)
        lst1.append(str)
    return lst1


#adding custom words to the pre-defined stop words list
# all_stopwords_gensim = STOPWORDS.union(set(['disease']))

def stopwprds_removal_gensim_custom(lst):
    lst1=list()
    for str in lst:
        text_tokens = word_tokenize(str)
        tokens_without_sw = [word for word in text_tokens if not word in all_stopwords_gensim]
        str_t = ' '.join(tokens_without_sw)
        lst1.append(str_t)
 
    return lst1


#%%

# data = pd.read_csv('psx_games.csv')
# print(data)


  
with open('psx_games.csv',  encoding="utf8") as read_obj:
  
    # Return a reader object which will
    # iterate over lines in the given csvfile
    csv_reader = csv.reader(read_obj)
  
    # convert string to list
    list_of_csv = list(csv_reader)[1:]
    

"""
temp = list_of_csv[1]
temp = " ".join(temp)
print(temp)
"""

#%%
#df = pd.DataFrame(list_of_csv)    
temp = [" ".join(doc).lower() for doc in list_of_csv]

tokenized_data = [doc.split(" ") for doc in temp]

#%%

# print(tokenized_data)
# tokenized_data = spl_chars_removal(tokenized_data)

# tokenized_data = stopwprds_removal_gensim_custom(tokenized_data)

#print('new data: ')
#print(tokenized_data)

bm25 = BM25Okapi(tokenized_data)
# <rank_bm25.BM25Okapi at 0x1047881d0>

#%%


# TODO handle garbage queries

game_query = 'Dark Souls'

games_client = pybomb.GamesClient(my_key)

response = games_client.quick_search(
  name=game_query,
  limit=1,
  #platform=pybomb.PS3,
  sort_by='original_release_date',
  desc=True
)

results = response.results

result = [result for result in results if result['original_release_date'] is not None ][0]

query = result['deck']

#response.results[0]['deck']


tokenized_query = query.lower().split(" ")

# doc_scores = bm25.get_scores(tokenized_query)
# array([0.        , 0.93729472, 0.        ])

docs = bm25.get_top_n(tokenized_query, list_of_csv)

response = games_client.quick_search(
  name=docs[0][0],
  limit=1,
  platform=pybomb.PS1,
  sort_by='original_release_date',
  desc=True
)

rec_game = response.results[0]

print(rec_game['name'])
print(rec_game['deck'])


html = ''

html += '<h1>' + rec_game['name'] + '</h1><br>'

html += '<img src="' + rec_game['image']['small_url'] + '">'
html += '<p>' + rec_game['deck'] + '</p>' 
html += rec_game['description'].replace('a href="', 'a href="https://www.giantbomb.com')

f = open("rec_game.html","w")

f.write(html)
f.close()


#%%

# print(docs)
# =============================================================================
# 
# count = 0
# 
# for doc in docs:
#     print("Game " + str(count))
#     print(doc)
#     count += 1
# 
# 
# =============================================================================

"""

df_search = df[df[query].isin(docs)]
df_search.head()

"""
# print(bm25.get_top_n(tokenized_query, list_of_csv, n=2) )

# bm25.get_top_n(tokenized_query, corpus, n=1)
# where n = the number of search results returned
# ['It is quite windy in London']
