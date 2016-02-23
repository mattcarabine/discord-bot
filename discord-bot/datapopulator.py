import logging
import os
import riotwatcher
import sys
import time

from manager.manager import FileManager, CouchbaseManager, FileNotFoundError

SLEEP_TIME = 15

stream_handler = logging.StreamHandler()
log_format = logging.Formatter(
    fmt='%(levelname)s|%(name)s: %(message)s')
logger_datapop = logging.getLogger('datapop')
stream_handler.setLevel(level=logging.INFO)
stream_handler.setFormatter(fmt=log_format)
logger_datapop.setLevel(logging.DEBUG)
logger_datapop.addHandler(stream_handler)


class MatchHistoryUpdater():
    def __init__(self):
        self.riot = riotwatcher.RiotWatcher(
            default_region=riotwatcher.EUROPE_WEST,
            key=os.environ.get('RIOT_API_KEY'))
        self.storage_manager = CouchbaseManager(
            os.environ.get('MATCH_HISTORY_BUCKET'))

        self.player_dict = self.storage_manager.get('players')
        logger_datapop.info('Setup complete')
        while True:
            for _, player_id in self.player_dict.iteritems():
                self.update_recent_games(player_id)
                time.sleep(SLEEP_TIME)
            self.player_dict = self.get_players()

    def get_players(self):
        try:
            player_dict = self.storage_manager.get('players')
        except FileNotFoundError:
            player_dict = self.riot.get_summoners(names=['Loltown'])
            self.storage_manager.set('players', player_dict)
        return player_dict

    def update_recent_games(self, player_id):
        api_matches = self.riot.get_recent_games(player_id)
        key = 'matches-{}'.format(player_id)
        try:
            db_matches = self.storage_manager.get(key)
        except FileNotFoundError:
            self.storage_manager.set(key, api_matches)
        else:
            game_ids = list()
            for db_match in db_matches['games']:
                game_ids.append(db_match['gameId'])

            for api_match in api_matches['games']:
                if api_match['gameId'] in game_ids:
                    break
                else:
                    db_matches['games'].insert(0, api_match)
                    logger_datapop.info('Added game {} to {}'.format(
                        api_match['gameId'], player_id))

            self.storage_manager.set(key, db_matches)
            logger_datapop.debug('Updated {}'.format(key))

if __name__ == '__main__':
    MatchHistoryUpdater()
