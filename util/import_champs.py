from riotwatcher import RiotWatcher
import json
import os

w = RiotWatcher(os.environ.get('RIOT_API_KEY'))
CHAMP_LIST_LOC = os.path.join(os.environ.get('DATA_PATH'), 'champions.json')

champs = w.static_get_champion_list()

print champs

new_champs = {}
for champ in champs['data'].itervalues():
    new_champs[champ['id']] = champ['name']

with open(CHAMP_LIST_LOC, 'w') as f:
    f.write(json.dumps(new_champs, sort_keys=True))
