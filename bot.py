import os
from pathlib import Path
import asyncio
import discord
from discord.ext import commands
from cogs.utils import Pyson, MakeConfig, checks, BotConfig, syscheck

syscheck()

# Check if a config file exists
config_path = Path('cogs/data/config.json')
if not os.path.isfile(config_path):
    MakeConfig(str(config_path))

config = Pyson(str(config_path))
settings = BotConfig(config.data)


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
        settings.reboot = False
        await self.bot.logout()
        await self.bot.close()

    # unload an extension
    @checks.is_owner()
    @commands.command()
    async def unload(self, cog: str = None):
        ''': Unload an extension'''
        try:
            for extension in settings.startup_extensions:
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
            extension='cogs.'+cog
            self.bot.unload_extension(extension)
            self.bot.load_extension(extension)
            await self.bot.say('Reloaded Extension: '+cog)
        except:
            await self.bot.say('Invalid Extension Name!')


# auto reconnect
async def boot():
    while not bot.is_closed:
        try:
            await bot.start(settings.token)
        except Exception:
            print('Connection lost, retrying...')
            await asyncio.sleep(5)


# pull all extensions from the cogs folder
def load_extensions():
    settings.startup_extensions = []
    path = Path('./cogs')
    for dirpath, dirnames, filenames in os.walk(path):
        if dirpath.strip('./') == str(path):
            for cog in filenames:
                settings.startup_extensions.append(
                    ('cogs.'+cog).strip('.py'))

    # load cogs from extensions
    if __name__ == "__main__":
        for extension in settings.startup_extensions:
            try:
                bot.load_extension(extension)
                print('Loaded {}'.format(extension))
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))


while settings.reboot:
    config = Pyson(str(config_path))
    settings = BotConfig(config.data)
    bot = commands.Bot(**settings.bot_settings)
    bot.add_cog(Utils(bot))
    load_extensions()
    bot.loop.run_until_complete(boot())
