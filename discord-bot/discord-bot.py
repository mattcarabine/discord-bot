import discord
import re
import os

from leaguebot import LeagueBot

client = discord.Client()
client.login(os.environ.get('DISCORD_EMAIL'),
             os.environ.get('DISCORD_PASSWORD'))

l = LeagueBot(client)
commands = {r'^leaguebot add (\w|\s){3,16}$': l.add_player,
            r'^leaguebot list$': l.print_players,
            r'^leaguebot current-games$': l.get_current_games,
            r'^leaguebot current-game (\w|\s){3,16}$': l.get_current_game}

@client.event
def on_message(message):
    for command, function in commands.iteritems():
        if re.search(command, message.content):
            function(message)

@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run()



