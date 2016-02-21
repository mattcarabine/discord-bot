import json
import os
import logging

from riotwatcher import RiotWatcher, EUROPE_WEST, LoLException, error_404
from discord_bot import DiscordBot

PLAYER_LIST_LOC = os.path.join(os.environ.get('DATA_PATH'), 'players.json')
CHAMP_LIST_LOC = os.path.join(os.environ.get('DATA_PATH'), 'champions.json')
league_bot_logger = logging.getLogger('leaguebot')
league_bot_logger.level = logging.INFO


class LeagueBot(DiscordBot):

    def __init__(self, client):
        super(LeagueBot, self).__init__(client, 'leaguebot')
        self.players = self.load_player_list()
        self.champions = self.load_champions()
        self.riot = RiotWatcher(os.environ.get('RIOT_API_KEY'),
                                default_region=EUROPE_WEST)

    @staticmethod
    def load_player_list():
        if os.path.exists(PLAYER_LIST_LOC):
            with open(PLAYER_LIST_LOC, 'r') as f:
                return json.loads(f.read())
        else:
            return {}

    @staticmethod
    def load_champions():
        if os.path.exists(CHAMP_LIST_LOC):
            with open(CHAMP_LIST_LOC, 'r') as f:
                return json.loads(f.read())
        else:
            return {}

    @DiscordBot.add_command('add')
    def add_player(self, *args):
        player = ''.join(args)
        try:
            summoner = self.riot.get_summoner(name=player)
        except LoLException as e:
            if e == error_404:
                self.send_message('Error - Player {} does not exist'
                                  .format(player))
            else:
                self.send_message('An unknown error occurred, let Matt know!')
                league_bot_logger.warning(e)
            return

        self.players[summoner['name'].lower()] = summoner['id']
        self.send_message('Added {} to list of players'.format(player))
        self._save_player_list()

    @DiscordBot.add_command('list')
    def print_players(self, *args):
        if self.players:
            player_list = '\n'
            for player in self.players:
                player_list += '{}\n'.format(player)
            self.send_message(player_list)
        else:
            self.send_message('Player list empty')

    def _save_player_list(self):
        with open(PLAYER_LIST_LOC, 'w') as f:
            f.write(json.dumps(self.players))

    @DiscordBot.add_command('current-games')
    def get_current_games(self, *args):
        for player in self.players:
            self.get_current_game(player)

    @DiscordBot.add_command('current-game')
    def get_current_game(self, *args):
        player = ''.join(args)
        if player not in self.players.keys():
            try:
                summoner = self.riot.get_summoner(name=player)
            except LoLException as e:
                if e == error_404:
                    self.send_message(
                        'Error - Player {} does not exist'.format(player))
                else:
                    self.send_message(
                        'An unknown error occurred, let Matt know!')
                    league_bot_logger.warning(e)
                return
            else:
                player_id = summoner['id']
        else:
            player_id = self.players[player]

        try:
            curr_game = self.riot.get_current_game(player_id)
        except LoLException as e:
            if e == error_404:
                self.send_message('{} is not in a game'.format(player))
            else:
                league_bot_logger.warning(e)
        else:
            game_length = (int(curr_game['gameLength']) / 60) + 3
            for participant in curr_game['participants']:
                if participant['summonerName'].lower() == player.lower():
                    champion = self.champions[str(participant['championId'])]
                    lolnexus_url = (
                        'http://www.lolnexus.com/EUW/search?name={}&region=EUW'
                        .format(player))

                    self.send_message(
                        '{} has been in a game for {} minutes - Playing {}\n'
                        'Link to game: {}'
                        .format(player, game_length, champion, lolnexus_url))
                    break
