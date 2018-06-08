import os
from pathlib import Path
import asyncio
import discord
from discord.ext import commands
from cogs.utils import Pyson, MakeConfig, checks, syscheck

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


class Utils:
    '''Some useful utils for the discord bot'''

    def __init__(self, bot):
        self.bot = bot

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
        try:
            for extension in bot.startup_extensions:
                if cog in extension:
                    self.bot.unload_extension(extension)
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
    bot.reboot = True
    bot.startup_extensions = []
    bot.command_prefix = bot.config.data.get(
        'Bot Settings').get('command_prefix')
    bot.description = bot.config.data.get('Bot Settings').get('description')
    bot.pm_help = bot.config.data.get('Bot Settings').get('pm_help')
    bot.token = bot.config.data.get('token')

# pull all extensions from the cogs folder


def load_extensions():
    bot.startup_extensions = []
    path = Path('./cogs')
    for dirpath, dirnames, filenames in os.walk(path):
        if dirpath.strip('./') == str(path):
            for cog in filenames:
                bot.startup_extensions.append(
                    ('cogs.'+cog).strip('.py'))

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
    load_extensions()
    bot.add_cog(Utils(bot))
    bot.loop.run_until_complete(boot())
