'''
A list of checks to use for the bot.

Example:

Transforming common checks into its own decorator:

    .. code-block:: python

        def is_me():
            def predicate(ctx):
                return ctx.author.id == 'my-user-id'
            return commands.check(predicate)

        @bot.command()
        @is_me()
        async def only_me():
            await bot.say('Only you!')

'''

import discord
from discord.ext import commands
from ..utils import Pyson


def bot_owner():
    'Checks for if the user is the bot owner or a coowner'
    async def predicate(ctx):
        coowners = Pyson('cogs/data/config').data.get('coowners', [])
        bot = await ctx.bot.application_info()
        if ctx.author.id in coowners:
            return True
        if ctx.author == bot.owner:
            return True
    return commands.check(predicate)


def server_owner():
    '''Checks if the message author is the server owner'''
    def predicate(ctx):
        if not ctx.guild:
            return False
        if ctx.author is ctx.guild.owner:
            return True
        return False
    return commands.check(predicate)


def is_admin():
    '''Checks if the message author admin perms'''
    def predicate(ctx):
        if not ctx.guild:
            return False
        author = ctx.author
        if ('administrator', True) in author.guild_permissions:
            return True
        return False
    return commands.check(predicate)
