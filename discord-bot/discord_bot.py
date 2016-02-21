import logging


class DiscordBot(object):
    commands = {}

    def __init__(self, client, logger_name, channel=None):
        self.client = client
        self.logger = logging.getLogger('discordbot.{}'.format(logger_name))
        self.channel = channel

    def send_message(self, message):
        if self.channel:
            self.client.send_message(self.channel, message)
        else:
            self.logger.warning(
                'Unable to send message `{}`, no channel specified'
                .format(message))

    def on_message(self, message):
        message = message.split(' ')
        for command, func in self.__class__.commands.iteritems():
            if message[0] == command:
                func(self, *message[1:])

    @classmethod
    def add_command(cls, command):
        def simple_decorator(f):
            cls.commands[command] = f

        return simple_decorator
