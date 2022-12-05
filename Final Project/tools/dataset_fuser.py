#%%

import pandas as pd
import glob

#%%

dfs = []
for file in glob.glob("*.csv"):
    if("all_games" not in file):
        print(file)
        dfs.append(pd.read_csv(file))
    
#%%

df = pd.concat(dfs).reset_index(drop=True)
bad_rows = list(df[df['original_release_date'] >= "2001-04-24"].index)

df = df.drop(bad_rows)
df.to_csv('all_games.csv', index=False)