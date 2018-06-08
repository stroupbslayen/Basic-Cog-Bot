import os
from .pyson import Pyson


class MakeConfig:

    def __init__(self, config_path="config"):
        self.config = Pyson(config_path)
        self.token = None
        self.prefix = '!'
        self.description = None
        self.pm_help = False
        self.get_info()
        self.config.data = {
            'token': self.token,
            'Bot Settings': {
                'command_prefix': self.prefix,
                'description': self.description,
                'pm_help': self.pm_help
            }
        }
        self.config.save()

    def get_info(self):
        self.token = input('Please enter your discord bot token: ')
        prefix = input(
            'Please enter the prefix you would like to use (default is !): ')
        if prefix != '':
            self.prefix = prefix
        description = input(
            'Please enter you bots description (optional):  ')
        self.description = f'''{description}'''
        pm = input('Would you like the help menu to be sent in a PM? (y/n): ')
        if pm.lower() in ['y', 'yes']:
            self.pm_help = True
        else:
            self.pm_help = False
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
