import discord
import logging
import os

from bot.league_bot import LeagueBot

stream_handler = logging.StreamHandler()
log_format = logging.Formatter(
    fmt='%(levelname)s|%(name)s: %(message)s')
logger_discordbot = logging.getLogger('discordbot')
stream_handler.setLevel(level=logging.INFO)
stream_handler.setFormatter(fmt=log_format)
logger_discordbot.setLevel(logging.DEBUG)
logger_discordbot.addHandler(stream_handler)


def main():
    client = discord.Client()
    client.login(os.environ.get('DISCORD_EMAIL'),
                 os.environ.get('DISCORD_PASSWORD'))

    league_bot = LeagueBot(client)
    bots = {'leaguebot': league_bot}

    @client.event
    def on_message(message):
        for prefix, bot in bots.iteritems():
            if message.content.startswith(prefix):
                bot.channel = message.channel
                bot.on_message(message.content.split(' ', 1)[1])

    @client.event
    def on_ready():
        logging.getLogger('discordbot').info(
            'Logged in as {}'.format(client.user))

    client.run()


if __name__ == '__main__':
    main()
