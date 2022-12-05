#%%

import pandas as pd
import requests
import os
import json

#%%



#%%

consoles = {}
consoles['snes'] = '9'

games = {}

#['genesis', 'snes', 'gb', 'game gear', 'ps', 'n64', 'gbc']

API_KEY = os.environ.get('GB_API')

#platforms
#query = {}
#response = requests.get(api_url + , params=query)
#print(response.json())

api_url = "https://www.giantbomb.com/api/games/?api_key={}&format=json&filter=platforms:{}".format(API_KEY, consoles['snes'])
url = "https://www.giantbomb.com/api/search/?api_key={}&format=json&query={}&resources=game".format(API_KEY, "snes")

headers = {
    'Cookie': 'device_view=full',
    'User-Agent': 'PostmanRuntime/7.26.8'
}

response = requests.request("GET", api_url, headers=headers, data={})

results = response.json()['results']

for result in results:
    platforms = [platform['name'] for platform in result['platforms']]
    games[result['name']] = [result['guid'], result['name'], result['deck'], platforms]

#return jsonify({"response": response.text})
#print(response.json())
#print(response.json()['results'][0]['platforms'])