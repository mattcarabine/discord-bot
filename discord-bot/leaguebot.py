import json
import os
import logging

from riotwatcher import RiotWatcher, EUROPE_WEST, LoLException, error_404

PLAYER_LIST_LOC = os.path.join(os.environ.get('DATA_PATH'), 'players.json')
CHAMP_LIST_LOC = os.path.join(os.environ.get('DATA_PATH'), 'champions.json')
league_bot_logger = logging.getLogger('leaguebot')
league_bot_logger.level = logging.INFO

class LeagueBot(object):
    def __init__(self, client):
        self.players = self.load_player_list()
        self.champions = self.load_champions()
        self.client = client
        self.riot = RiotWatcher(os.environ.get('RIOT_API_KEY'), default_region=EUROPE_WEST)

    def load_player_list(self):
        if os.path.exists(PLAYER_LIST_LOC):
            with open(PLAYER_LIST_LOC, 'r') as f:
                return json.loads(f.read())
        else:
            return {}

    def load_champions(self):
        if os.path.exists(CHAMP_LIST_LOC):
            with open(CHAMP_LIST_LOC, 'r') as f:
                return json.loads(f.read())
        else:
            return {}

    def add_player(self, message, **kwargs):
        try:
            player = kwargs['player']
        except KeyError:
            player = message.content.split('add', 1)[1].strip()
        try:
            summoner = self.riot.get_summoner(name=player)
        except LoLException as e:
            if e == error_404:
                self.client.send_message(message.channel, 'Error - Player {} does not exist'.format(player))
            else:
                self.client.send_message(message.channel, 'An unknown error occurred, let Matt know!')
            return

        self.players[summoner['name'].lower()] = summoner['id']
        self.client.send_message(message.channel, 'Added {} to list of players'.format(player))
        self.save_player_list()

    def print_players(self, message):
        if self.players:
            player_list = '\n'
            for player in self.players:
                player_list += '{}\n'.format(player)
            self.client.send_message(message.channel, player_list)
        else:
            self.client.send_message(message.channel, 'Player list empty')

    def save_player_list(self):
        with open(PLAYER_LIST_LOC, 'w') as f:
            f.write(json.dumps(self.players))

    def get_current_games(self, message):
        for player in self.players:
            self.get_current_game(message, player=player)

    def get_current_game(self, message, **kwargs):
        try:
            player = kwargs['player']
        except KeyError:
            player = message.content.split('current-game', 1)[1].strip().lower()
            if player not in self.players.keys():
                try:
                    summoner = self.riot.get_summoner(name=player)
                except LoLException as e:
                    if e == error_404:
                        self.client.send_message(message.channel, 'Error - Player {} does not exist'.format(player))
                    else:
                        self.client.send_message(message.channel, 'An unknown error occurred, let Matt know!')
                    return
                else:
                    player_id = summoner['id']
            else:
                player_id = self.players[player]
        else:
            player_id = self.players[player]

        try:
            curr_game = self.riot.get_current_game(player_id)
        except LoLException as e:
            if e == error_404:
                self.client.send_message(message.channel, '{} is not in a game'.format(player))
            else:
                league_bot_logger.warning(e)
        else:
            game_length = (int(curr_game['gameLength']) / 60) + 3
            for participant in curr_game['participants']:
                if participant['summonerName'].lower() == player.lower():
                    champion = self.champions[str(participant['championId'])]
                    lolnexus_url = 'http://www.lolnexus.com/EUW/search?name={}&region=EUW'.format(player)
                    self.client.send_message(
                        message.channel, '{} has been in a game for {} minutes'
                        '- Playing {}\nLink to game: {}'
                        .format(player, game_length, champion, lolnexus_url))
                    break
