import os
from datetime import datetime
from pathlib import Path
import asyncio
import discord
from discord.ext import commands
from cogs.utils import Pyson, MakeConfig, checks, syscheck, log_error

syscheck()

if not os.path.isdir('cogs/data'):
    os.makedirs('cogs/data')


# Check if a config file exists
config_path = Path('cogs/data/config.json')
if not os.path.isfile(config_path):
    MakeConfig(str(config_path))


# dummy class to get the bot started...
class bot:
    reboot = True


base_extensions = {

    'Bot_Logging': 'cogs.utils.logger',
    'Bot_Settings': 'cogs.utils.Bot_Settings',
    'Utils': './'

}


class Utils:
    '''Some useful utils for the discord bot'''

    def __init__(self, bot):
        self.bot = bot
        self.bot.starttime = datetime.now()

    async def on_ready(self):
        print('Logged in as: '+self.bot.user.name)
        print('With user ID: '+self.bot.user.id)

    # reboot the bot
    @checks.is_owner()
    @commands.command()
    async def reboot(self):
        ''': Reboot the bot'''
        await bot.say('Rebooting!')
        await self.bot.logout()
        await self.bot.close()

    # shutdown the bot
    @checks.is_owner()
    @commands.command()
    async def shutdown(self):
        ''': Shutdown the bot'''
        await bot.say('Shutting Down!')
        bot.reboot = False
        await self.bot.logout()
        await self.bot.close()

    # unload an extension
    @checks.is_owner()
    @commands.command()
    async def unload(self, cog: str = None):
        ''': Unload an extension'''
        if cog in base_extensions:
            await bot.say('Cannot unload a base extension')
            return
        try:
            self.bot.unload_extension('cogs.'+cog)
            await self.bot.say('Unloaded Extension: '+cog)
        except:
            await self.bot.say('Invalid Extension Name!')

    # load an extension
    @checks.is_owner()
    @commands.command()
    async def load(self, cog: str = None):
        ''': Load an extension'''
        try:
            self.bot.load_extension('cogs.'+cog)
            await self.bot.say('Loaded Extension: '+cog)
        except:
            await self.bot.say('Invalid Extension Name!')

    # reload an extension
    @checks.is_owner()
    @commands.command(name='reload')
    async def _reload(self, cog: str = None):
        ''': Reload an extension'''
        try:
            extension = 'cogs.'+cog
            self.bot.unload_extension(extension)
            self.bot.load_extension(extension)
            await self.bot.say('Reloaded Extension: '+cog)
        except:
            await self.bot.say('Invalid Extension Name!')

    @commands.command()
    async def uptime(self):
        ''': See how long I've been online'''
        time = datetime.now() - self.bot.starttime
        days = time.days
        hours, remainder = divmod(time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        await bot.say(f"I've been online for {days} days, {minutes} min, {seconds} seconds!")


# auto reconnect
async def boot():
    while not bot.is_closed:
        try:
            await bot.start(bot.token)
        except Exception as e:
            print(f'Error: {e}\nRetrying Connection')
            print('Connection lost, retrying...')
            await asyncio.sleep(5)


# load bot settings
def load_settings():
    bot.config = Pyson(str(config_path))
    bot.startup_extensions = []
    bot.reboot = True
    bot.command_prefix = bot.config.data.get(
        'Bot Settings').get('command_prefix')
    bot.description = bot.config.data.get('Bot Settings').get('description')
    bot.pm_help = bot.config.data.get('Bot Settings').get('pm_help')
    bot.token = bot.config.data.get('token')


def load_base_extensions():
    for extension in base_extensions.values():
        try:
            bot.load_extension(extension)
        except:
            pass


# pull all extensions from the cogs folder
def load_extensions():
    path = Path('./cogs')
    for dirpath, dirnames, filenames in os.walk(path):
        if dirpath.strip('./') == str(path):
            for cog in filenames:
                extension = 'cogs.'+cog[:-3]
                if extension not in base_extensions.values():
                    bot.startup_extensions.append(extension)

    # load cogs from extensions
    if __name__ == "__main__":
        for extension in bot.startup_extensions:
            try:
                bot.load_extension(extension)
                print('Loaded {}'.format(extension))
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))


while bot.reboot:
    bot = commands.Bot(command_prefix='')
    load_settings()
    load_base_extensions()
    bot.add_cog(Utils(bot))
    load_extensions()

    @bot.event
    async def on_error(event, *args, **kwargs):
        try:
            raise
        except Exception as error:
            print(error)
            await log_error(error, event, *args, **kwargs)
    bot.loop.run_until_complete(boot())
