class BotConfig:
    '''Configs for the bot'''
    def __init__(self,_dict):
        self.reboot = True
        self.startup_extensions = []
        self.bot_settings = _dict.get('Bot Settings')
        self.token = _dict.get('token')