import csv
from rank_bm25 import BM25Okapi
import pybomb
from dash import Dash, html, dcc
import dash
import dash_dangerously_set_inner_html
import random
import requests

#%%

GIANTBOMB_API = " " # NEED TO INCLUDE API KEY! https://www.giantbomb.com/api/

#%%

with open('assets/all_games.csv',  encoding="utf8") as read_obj:
  
    # Return a reader object which will
    # iterate over lines in the given csvfile
    csv_reader = csv.reader(read_obj)
  
    # convert string to list
    list_of_csv = list(csv_reader)[1:]
    
temp = [" ".join(doc).lower() for doc in list_of_csv]

tokenized_data = [doc.split(" ") for doc in temp]

bm25 = BM25Okapi(tokenized_data)

#%%

giantbomb_consoles = {
    "ps" : {"id": pybomb.PS1, "name": "PlayStation"},
    "n64" : {"id": 43, "name": "Nintendo 64"},
    "gg" : {"id": 5, "name": "Game Gear"},
    "gbc" : {"id": 57, "name": "Game Boy Color"},
    "gb" : {"id": 3, "name": "Game Boy"},
    "snes" : {"id": 9, "name": "Super Nintendo Entertainment System"},
    "genesis" : {"id": 6,  "name": "Sega Genesis"}
    }

# TODO handle garbage queries

def get_rec_objs(game_query):
    headers = {
        'Cookie': 'device_view=full',
        'User-Agent': 'PostmanRuntime/7.26.8'
    }

    games_client = pybomb.GamesClient(GIANTBOMB_API)

    response = games_client.quick_search(
    name=game_query,
    limit=1,
    sort_by='original_release_date',
    desc=True
    )

    results = response.results

    try:
        result = [result for result in results if result['original_release_date'] is not None ][0]

        query = result['deck']
    except:
        query = random.choice(list_of_csv)[5]

    tokenized_query = query.lower().split(" ")

    docs = bm25.get_top_n(tokenized_query, list_of_csv, n=10)

    children = []
    rec_games = []
    
    for i in range(len(docs)):
        if(len(rec_games) < 5):
            guid = docs[i][6]
            print(docs[i][0], guid)
            try:
                #url = "https://www.giantbomb.com/api/game/{}/?api_key={}&format=json&platform={}".format(guid, GIANTBOMB_API, giantbomb_consoles[docs[i][4]]["id"])
                #response = requests.request("GET", url, headers=headers, data={})

                #rec_game = response.json()['results']

                response = games_client.quick_search(
                name=docs[i][0],
                limit=1,
                platform=giantbomb_consoles[docs[i][4]]["id"],
                sort_by='original_release_date',
                desc=True
                )

                rec_game = response.results[0]            

                print(rec_game['name'])
                print(rec_game['deck'])       

                if(rec_game['name'] not in rec_games):
                    rec_games.append(rec_game['name'])     
                    children.append(html.Center(children = [html.H1(" ~~~~~ " + rec_game['name'] + " - " + giantbomb_consoles[docs[i][4]]["name"] + " ~~~~~ ")]))
                    children.append(html.Br())
                    children.append(html.Img(src=rec_game['image']['small_url']))
                    children.append(html.P(rec_game['deck']))

                    try:
                        description = rec_game['description'].replace('a href="', 'a href="https://www.giantbomb.com')
                    
                        children.append(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(description))
                    except:
                        children.append(dash_dangerously_set_inner_html.DangerouslySetInnerHTML("<p>No Description Available</p>"))
            except Exception as e:
                print(e)
                pass

    return children

#%%

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.H1('Retro Game Recommender', className="app-header--title")
        ]
    ),
    html.Div(
        className="app-header",
        children=[
            html.H2('Search', className="app-header--title")
        ]
    ),
    html.Div(
        className="app-header",
        children=[
            dcc.Input(id='game-name', value='Dark Souls', type='text'),
            html.Button(id='submit-button', type='submit', children='Submit'),
        ]
    ),
    html.Div(
        children=[
            html.Br()
        ]
    ),
    html.Div(
        className="app-header",
        children=[
            html.H2('Results', className="app-header--title")
        ]
    ), 
    html.Div(
        id = 'results-div',
        children = []
    )
])

@app.callback(
    dash.Output('results-div', 'children'),
    [dash.Input('submit-button', 'n_clicks')],
    [dash.State('game-name', 'value')],
    )

def update_output(clicks, input_value):
    if clicks is not None:
        print(clicks, input_value)
        return get_rec_objs(input_value)

if __name__ == '__main__':
    app.run_server(debug=True)
    pass