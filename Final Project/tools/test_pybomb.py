import pybomb

my_key = "3c5c41d657ce9b9ec4a3e752bf98a1a7de0e412a"
game_client = pybomb.GameClient(my_key)

game_id = 80643
return_fields = ('id', 'name', 'platforms', 'deck')

response = game_client.fetch(game_id, return_fields)

print (response.results)
print (response.deck)
print (response.result)
print (response.uri)
print (response.num_page_results)
print (response.num_total_results)


#%%

games_client = pybomb.GamesClient(my_key)

response = games_client.quick_search(
  name='call of duty',
  limit=1,
  #platform=pybomb.PS3,
  sort_by='original_release_date',
  desc=True
)

results = response.results

result = [result for result in results if result['original_release_date'] is not None ][0]
