import discord
import os
from discord.ext import commands
from . import checks


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
    async def change_description(self, *, description: str=''):
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

    @checks.is_owner()
    @commands.command()
    async def add_coowner(self, member: discord.Member=None):
        ': Add a co-owner to your server'
        config = self.bot.config
        if member is None:
            return
        else:
            if 'coowners' not in config.data:
                config.data['coowners'] = []
            if member.id not in config.data['coowners']:
                config.data['coowners'].append(member.id)
                config.save()
                await self.bot.say(f'{member.mention} has been added as a co-owner!')

    @checks.is_owner()
    @commands.command()
    async def remove_coowner(self, member: discord.Member=None):
        ': Remove a co-owner from your server'
        config = self.bot.config
        if member is None:
            return
        else:
            if 'coowners' not in config.data:
                config.data['coowners'] = []
            if member.id in config.data['coowners']:
                config.data['coowners'].remove(member.id)
                config.save()
                await self.bot.say(f'{member.mention} has been removed from co-owners!')

    @checks.is_coowner()
    @commands.command(pass_context=True)
    async def coowners(self, ctx):
        ': Check the co-owners of the server'
        coowners = ''
        for coowner in self.bot.config.data.get('coowners', []):
            coowners += f'{ctx.message.server.get_member(coowner).mention}\n'
        embed = discord.Embed(title='Co-Owners', description=coowners)
        await self.bot.say(embed=embed)


def setup(bot):
    bot.add_cog(Bot_Settings(bot))
