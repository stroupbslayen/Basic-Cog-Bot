import os
import traceback
import logging
from .pyson import Pyson
import discord
from discord.ext import commands
from . import checks


if not os.path.isfile('./cogs/data/log_config.json'):
    make = Pyson('./cogs/data/log_config')
    make.data = {
        'log_level': logging.INFO,
        'log_error': True,
        'log_message': True,
        'log_message_edit': True,
        'log_command': True,
        'log_command_error': True,
        'traceback': False
    }
    make.save

LOGS = logging.getLogger('discord')
LOGS.setLevel(logging.INFO)
HANDLER = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
HANDLER.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
LOGS.addHandler(HANDLER)


async def log_error(error, event, *args, **kwargs):

    if Pyson('./cogs/data/config').data['traceback']:
        tb = kwargs.get('tb')
        if tb:
            print(tb)
    else:
        print(error)
    LOGS = logging.getLogger(f'discord.{event}.error')
    LOGS.warning('Event: {} Error: {}'.format(event, error))

human = {
    'True': 'on',
    'False': 'off'
}


class Bot_Logging:

    def __init__(self, bot):
        self.bot = bot
        self.bot.add_check(self.log_command)
        self.bot.logging = Pyson('./cogs/data/log_config')
        LOGS.setLevel(self.bot.logging.data['log_level'])

    async def on_message(self, message):
        if self.bot.logging.data['log_message']:
            if message.author.id != self.bot.user.id:
                LOGS = logging.getLogger('discord.message')
                LOGS.info(f'Server_id: {message.guild.id} '
                          f'Author_id: {message.author.id} '
                          f'Message: {message.content}')

    async def on_message_edit(self, before, after):
        if self.bot.logging.data['log_message_edit']:
            if before.author.id != self.bot.user.id:
                LOGS = logging.getLogger('discord.message.edit')
                LOGS.info(f'Server_id: {before.guild.id} '
                          f'Author_id: {before.author.id} '
                          f'Original: {before.content} '
                          f'Edited: {after.content}')

    async def on_command_error(self, ctx, error):
        if self.bot.config.data.get('traceback'):
            await commands.bot.BotBase(self.bot).on_command_error(ctx, error)
        else:
            print(error)
        if self.bot.logging.data['log_command_error']:
            LOGS = logging.getLogger('discord.command.error')
            LOGS.warning(f'Server_id: {ctx.message.guild.id} '
                         f'Author_id: {ctx.message.author.id} '
                         f'Command: {ctx.invoked_with} '
                         f'Error: {error} ')

    def log_command(self, ctx):
        if self.bot.logging.data['log_command']:
            LOGS = logging.getLogger('discord.command')
            LOGS.info(f'Server_id: {ctx.message.guild.id} '
                      f'Author_id: {ctx.message.author.id} '
                      f'Command: {ctx.invoked_with}')
        return True

    @checks.is_owner()
    @commands.group(pass_context=True)
    async def toggle_log(self, ctx):
        ''': Toggle what the bot will log'''
        if not ctx.invoked_subcommand:
            await ctx.channel.send('No/Invalid toggle')

    @toggle_log.command(name='message')
    async def _message(self, ctx):
        ''': Log Messages'''
        await self.log_toggler(ctx, 'log_message', 'Message')

    @toggle_log.command(name='message_edit')
    async def _message_edit(self, ctx):
        ''': Log Edited Messages'''
        await self.log_toggler(ctx, 'log_message_edit', 'Message Edit')

    @toggle_log.command(name='error')
    async def _error(self, ctx):
        ''': Log Errors'''
        await self.log_toggler(ctx, 'log_error', 'Error')

    @toggle_log.command(name='command')
    async def _command(self, ctx):
        ''': Log Commands used'''
        await self.log_toggler(ctx, 'log_command', 'Command')

    @toggle_log.command(name='command_error')
    async def _command_error(self, ctx):
        ''': Log Errors from Commands'''
        await self.log_toggler(ctx, 'log_command_error', 'Command Error')

    @toggle_log.command(name='level')
    async def _log_level(self, ctx, level: str=None):
        '''': Set the logging level (Default Level: INFO)'''
        levelname = level.upper()
        level = logging._nameToLevel.get(levelname)
        if level is None:
            await ctx.channel.send('Invalid Level')
        else:
            self.bot.logging.data['log_level'] = level
            self.bot.logging.save
            LOGS.setLevel(self.bot.logging.data['log_level'])
            await ctx.channel.send(f'Log Level is now: {levelname}')

    async def log_toggler(self, ctx, log_type, generic_name):
        self.bot.logging.data[log_type] = not self.bot.logging.data[log_type]
        self.bot.logging.save
        if log_type == 'traceback':
            await ctx.channel.send(f'{generic_name} is now: {human[str(self.bot.logging.data[log_type])]}')
        else:
            await ctx.channel.send(f'{generic_name} logging is now: {human[str(self.bot.logging.data[log_type])]}')
