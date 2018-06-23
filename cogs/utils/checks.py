'''
A list of checks to use for the bot.

Example:

Transforming common checks into its own decorator:

    .. code-block:: python

        def is_me():
            def predicate(ctx):
                return ctx.message.author.id == 'my-user-id'
            return commands.check(predicate)

        @bot.command()
        @is_me()
        async def only_me():
            await bot.say('Only you!')

'''

import discord
from discord.ext import commands
from ..utils import Pyson


def is_owner():
    '''Checks if the message author is the server owner'''
    def predicate(ctx):
        return ctx.message.author is ctx.message.server.owner
    return commands.check(predicate)


def is_admin():
    '''Checks if the message author is the owner or has admin perms'''
    def predicate(ctx):
        author = ctx.message.author
        # if author is ctx.message.server.owner:
        # return True
        if ('administrator', True) in author.server_permissions:
            return True
        else:
            return False
    return commands.check(predicate)


def is_coowner():
    'Checks if the message author is a co-owner of the server'
    def predicate(ctx):
        coowners = Pyson('cogs/data/config').data.get('coowners', [])
        author = ctx.message.author.id
        owner = ctx.message.server.owner.id
        if author in coowners or author == owner:
            return True
        return False
    return commands.check(predicate)
