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


def is_owner():
    '''Checks if the message author is the server owner'''
    def predicate(ctx):
        return ctx.message.author is ctx.message.server.owner
    return commands.check(predicate)