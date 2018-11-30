import os
from pathlib import Path
from datetime import datetime
import traceback
from discord.ext import commands
import discord
if not os.path.isdir('cogs/data'):
    os.makedirs('cogs/data')
from cogs.utils import Pyson, MakeConfig, checks, syscheck, log_error, Bot_Logging, Bot_Settings
import aiohttp

syscheck()


# Check if a config file exists
config_path = Path('cogs/data/config.json')
if not os.path.isfile(config_path):
    MakeConfig(str(config_path))

settings = Pyson(str(config_path))

bot = commands.Bot(**settings.data.get('Bot Settings'))


@bot.event
async def on_error(event, *args, **kwargs):
    try:
        raise
    except Exception as error:
        tb = traceback.format_exc()
        await log_error(error, event, tb=tb, **kwargs)


class Utils:
    '''Some useful utils for the discord bot'''

    def __init__(self, bot):
        self.bot = bot
        self.bot.starttime = datetime.now()

    async def on_ready(self):
        print(f'Logged in as: {self.bot.user.name}')
        print(f'With user ID: {self.bot.user.id}')

    @checks.bot_owner()
    @commands.command()
    async def shutdown(self, ctx):
        ''': Shutdown the bot'''
        await ctx.channel.send('Shutting Down!')
        bot.reboot = False
        await self.bot.logout()
        await self.bot.close()

    # unload an extension
    @checks.bot_owner()
    @commands.command()
    async def unload(self, ctx, cog: str = None):
        ''': Unload an extension'''
        try:
            self.bot.unload_extension('cogs.'+cog)
            await ctx.channel.send('Unloaded Extension: '+cog)
        except:
            await ctx.channel.send('Invalid Extension Name!')

    # load an extension
    @checks.bot_owner()
    @commands.command()
    async def load(self, ctx, cog: str = None):
        ''': Load an extension'''
        try:
            self.bot.load_extension('cogs.'+cog)
            await ctx.channel.send('Loaded Extension: '+cog)
        except:
            await ctx.channel.send('Invalid Extension Name!')

    # reload an extension
    @checks.bot_owner()
    @commands.command(name='reload')
    async def _reload(self, ctx, cog: str = None):
        ''': Reload an extension'''
        try:
            extension = 'cogs.'+cog
            self.bot.unload_extension(extension)
            self.bot.load_extension(extension)
            await ctx.channel.send('Reloaded Extension: '+cog)
        except:
            await ctx.channel.send('Invalid Extension Name!')

    @commands.command()
    async def uptime(self, ctx):
        ''': See how long I've been online'''
        time = datetime.now() - self.bot.starttime
        days = time.days
        hours, remainder = divmod(time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        await ctx.channel.send(f"I've been online for {days} days, {minutes} min, {seconds} seconds!")


# load bot settings
def load_settings():

    bot.command_prefix = bot.config.data.get('Bot Settings').get('command_prefix')
    bot.description = bot.config.data.get('Bot Settings').get('description')
    bot.pm_help = bot.config.data.get('Bot Settings').get('pm_help')
    bot.token = bot.config.data.get('token')
    bot.case_insensitive = bot.config.data.get('Bot Settings').get('case_insensitive')


# pull all extensions from the cogs folder
def load_extensions():
    bot.startup_extensions = []
    path = Path('./cogs')
    for dirpath, dirnames, filenames in os.walk(path):
        if dirpath.strip('./') == str(path):
            for cog in filenames:
                extension = 'cogs.'+cog[:-3]
                bot.startup_extensions.append(extension)

    # load cogs from extensions
    if __name__ == "__main__":
        for extension in bot.startup_extensions:
            try:
                bot.load_extension(extension)
                print(f'Loaded {extension}')
            except Exception as e:
                print(f'Failed to load extension {extension}\n{e}')


# create an aiohttp session that cogs can use
async def create_aiohttp():
    bot.aiohttp = aiohttp.ClientSession()


bot.config = Pyson(str(config_path))
bot.add_cog(Bot_Settings(bot))
bot.add_cog(Bot_Logging(bot))
bot.add_cog(Utils(bot))
load_extensions()
bot.loop.create_task(create_aiohttp())
bot.run(settings.data.get('token'))
