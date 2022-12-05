#%%

import pandas as pd
import requests
import os
import json
from bs4 import *
import requests
import pickle
from io import StringIO
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import time

#%%

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

#%%

def get_data_set(df):
    headers = {
        'Cookie': 'device_view=full',
        'User-Agent': 'PostmanRuntime/7.26.8'
    }
    
    if("guid" not in df.columns):
        df['guid'] = ""
    
    for index, row in df.iterrows():
        if(len(row['guid']) == 0):
            print(index)
        
            time.sleep(1)
            url = "https://www.giantbomb.com/api/search/?api_key={}&format=json&query={}&resources=game".format(GIANTBOMB_API, row['Title'])
            response = requests.request("GET", url, headers=headers, data={})
            
            try:
                game_data = response.json()['results'][0]
                
                cols = ['deck', 'guid', 'id', 'number_of_user_reviews', 'original_release_date', 'site_detail_url']
                
                row['Title'] = game_data['name']
                
                for col in cols:
                    try:
                        row[col] = game_data[col]
                    except:
                        pass
                    
                try:
                    row['game_rating'] = game_data['original_game_rating'][0]['name']
                except:
                    pass
                
                html_parsed = ''
                
                try:    
                    html = game_data['description']
                    html_split = [strip_tags(split.split('<h')[0][2:])  for split in html.split('</h')[1:] if len(split.split('<h')[0][2:]) > 0]
                    
                    html = "<body>" + html + "</body>"
                    soup = BeautifulSoup(html, "html.parser")
                    
                    body = soup.find('body') 
                    
                    descs = []
                    
                    for child in body.find_all_next("h2"):
                        descs.append(strip_tags(str(child)))
                    
                    
                    for i in range(len(descs)):
                        html_parsed += " <div> " + descs[i] + ' : ' + html_split[i] + ' </div> '
                except:
                    pass
                
                row['description'] = html_parsed
                
                for col in list(row.index):
                    if col not in df.columns:
                        df[col] = ""
                        
                df.at[index] = row
                
            except:
                pass
    
    return df


#%%

GIANTBOMB_API = "" # NEED TO INCLUDE API KEY! https://www.giantbomb.com/api/

#%%



source_urls = {}
source_urls['genesis'] = ['https://en.wikipedia.org/wiki/List_of_Sega_Genesis_games']
source_urls['snes'] = ['https://en.wikipedia.org/wiki/List_of_Super_Nintendo_Entertainment_System_games']
source_urls['gb'] = ['https://en.wikipedia.org/wiki/List_of_Game_Boy_games']
source_urls['gbc'] = ['https://en.wikipedia.org/wiki/List_of_Game_Boy_Color_games']
source_urls['gg'] = ['https://en.wikipedia.org/wiki/List_of_Game_Gear_games']
source_urls['ps'] = ['https://en.wikipedia.org/wiki/List_of_PlayStation_games_(A%E2%80%93L)', 'https://en.wikipedia.org/wiki/List_of_PlayStation_games_(M%E2%80%93Z)']
source_urls['n64'] = ['https://en.wikipedia.org/wiki/List_of_Nintendo_64_games']


#%%

game_dfs = {}

for k, v in source_urls.items():
    game_dfs[k] = []
    
    for url in v:
        dfs = pd.read_html(url)
        game_dfs[k].append(dfs[[len(df) for df in dfs].index(max([len(df) for df in dfs]))])
        
#%%

with open('raw_games.pkl', 'wb') as handle:
    pickle.dump(game_dfs, handle)
     
#%%

with open('raw_games.pkl', 'rb') as handle:
    b = pickle.load(handle)
    
#%%

dfs = []

for k,v in b.items():
    for w in v:
        df = w.copy()
        if('MultiIndex' in str(type(df.columns))):
            df.columns = [' '.join(col).strip().replace('[12][13]','').split('[')[0].split('(')[0] for col in df.columns.values]
            df.columns = [col.split(' ')[0] if col.split(' ')[0] == col.split(' ')[-1] else col for col in df.columns]
        else:
            df.columns = [col.split('[')[0] for col in list(df.columns)]
            
        df['console'] = k
        print(k, len(df))
        dfs.append(df)
        
df = pd.concat(dfs).reset_index(drop=True)

#%%

# get gbc dataset

gbc_df = df[df['console'] == 'gbc']
gbc_df["NA"] = ""

for index, row in gbc_df.iterrows():
    row["NA"] = "(NA)" in row['First released']
    row["First released"] = row['First released'].split("(NA)")[-1].split("(")[0].strip()
    gbc_df.at[index] = row

gbc_df = gbc_df[gbc_df['NA'] != False]
gbc_df = gbc_df.dropna(axis=1,how='all').reset_index(drop=True)

gbc_df = gbc_df[['Title', 'Developer', 'Publisher', 'First released', 'console']].reset_index(drop=True)

#%%

gbc_df = get_data_set(gbc_df)

#%%

gbc_df.to_csv('gbc_games.csv', index=False)


#%%
# get gb dataset

gb_df = df[df['console'] == 'gb']
gb_df = gb_df[gb_df['Release date North America'] != 'Unreleased']
gb_df = gb_df.dropna(axis=1,how='all').reset_index(drop=True)

gb_df = gb_df[['Title', 'Developer', 'Publisher', 'Release date North America', 'console']].reset_index(drop=True)

#%%

gb_df = get_data_set(gb_df)

#%%

gb_df.to_csv('gb_games.csv', index=False)


#%%
# get snes dataset

snes_df = df[df['console'] == 'snes']
snes_df = snes_df[snes_df['Release date North America'] != 'Unreleased']
snes_df = snes_df.dropna(axis=1,how='all').reset_index(drop=True)

snes_df = snes_df[['Title', 'Developer', 'Publisher', 'Release date North America', 'console']].reset_index(drop=True)

#%%

snes_df = get_data_set(snes_df)

#%%

snes_df.to_csv('snes_games.csv', index=False)

#%%

# get genesis dataset

genesis_df = df[df['console'] == 'genesis']
genesis_df = genesis_df[genesis_df['Release date NA'] != 'Unreleased']
genesis_df = genesis_df.dropna(axis=1,how='all').reset_index(drop=True)

genesis_df = genesis_df[['Title', 'Developer', 'Publisher', 'Release date NA', 'console']].reset_index(drop=True)

#%%

genesis_df = get_data_set(genesis_df)

#%%

genesis_df.to_csv('genesis_games.csv', index=False)


#%%
# get gg dataset

gg_df = df[df['console'] == 'gg']
gg_df = gg_df[gg_df['Release date NA'] != 'Unreleased']
gg_df = gg_df.dropna(axis=1,how='all').reset_index(drop=True)

gg_df = gg_df[['Title', 'Developer', 'Publisher', 'Release date NA', 'console']].reset_index(drop=True)

#%%

gg_df = get_data_set(gg_df)

#%%

gg_df.to_csv('gg_games.csv', index=False)

#%%

# get n64 dataset

n64_df = df[df['console'] == 'n64']
n64_df = n64_df[n64_df['Release date North America'] != 'Unreleased']
n64_df = n64_df.dropna(axis=1,how='all').reset_index(drop=True)

n64_df = n64_df[['Title', 'Developer', 'Publisher', 'Release date North America', 'console']].reset_index(drop=True)

#%%

n64_df = get_data_set(n64_df)

#%%

n64_df.to_csv('n64_games.csv', index=False)


#%%

# get ps dataset

ps_df = df[df['console'] == 'ps']
ps_df = ps_df[ps_df['Regions released North America'] != 'Unreleased']


ps_df['Title'] = ps_df['Title'].apply(lambda x: x.split('•')[0])

ps_df = ps_df[['Title', 'Developer', 'Publisher', 'Regions released North America', 'console']].reset_index(drop=True)

#%%

ps_df = get_data_set(ps_df)

#%%

ps_df.to_csv('psx_games.csv', index=False)

