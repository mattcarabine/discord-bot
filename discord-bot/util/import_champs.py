from riotwatcher import RiotWatcher
import os

def import_champs():
    w = RiotWatcher(os.environ.get('RIOT_API_KEY'))
    champs = w.static_get_champion_list()

    new_champs = {}
    for champ in champs['data'].itervalues():
        new_champs[champ['id']] = champ['name']

    return new_champs

if __name__ == '__main__':
    import_champs()