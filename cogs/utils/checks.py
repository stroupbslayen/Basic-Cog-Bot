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


def check_owner(ctx):
    coowners = Pyson('cogs/data/config').data.get('coowners', [])
    author = ctx.author.id
    owner = ctx.message.guild.owner.id
    if author in coowners or author == owner:
        return True
    return False


def is_owner():
    '''Checks if the message author is the server owner or a coowner'''
    def predicate(ctx):
        return check_owner(ctx)
    return commands.check(predicate)


def is_admin():
    '''Checks if the message author is the owner or has admin perms'''
    def predicate(ctx):
        author = ctx.author
        if check_owner(ctx):
            return True
        if ('administrator', True) in author.guild_permissions:
            return True
        else:
            return False
    return commands.check(predicate)
