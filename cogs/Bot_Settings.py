import discord
import os
from discord.ext import commands
from .utils import checks


class Bot_Settings():
    def __init__(self, bot):
        self.bot = bot

    @checks.is_owner()
    @commands.command()
    async def change_prefix(self, prefix: str = '!'):
        ''': Change the prefix for using bot commands'''
        self.bot.command_prefix = prefix
        self.bot.config.data['Bot Settings']['command_prefix'] = prefix
        self.bot.config.save()
        await self.bot.reply(f'commands will now be called with **{prefix}**')

    @checks.is_owner()
    @commands.command()
    async def change_description(self, *, description: str = ''):
        ''': Change the description for the bot displayed in the help menu'''
        self.bot.description = description
        self.bot.config.data['Bot Settings']['description'] = description
        self.bot.config.save()
        await self.bot.reply(f'The bots description is now ```{description}```')

    @checks.is_owner()
    @commands.command()
    async def toggle_help(self):
        ''': Toggle how the bot send the help menu in a pm'''
        self.bot.pm_help = not self.bot.pm_help
        self.bot.config.data['Bot Settings']['pm_help'] = not self.bot.config.data['Bot Settings']['pm_help']
        self.bot.config.save()
        if self.bot.pm_help:
            await self.bot.say('The help menu will be sent as a PM now.')
        else:
            await self.bot.say('The help menu will be posted locally.')


def setup(bot):
    bot.add_cog(Bot_Settings(bot))
