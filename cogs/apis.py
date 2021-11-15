from typing import AsyncContextManager
from discord.ext import commands
import discord
import asyncio
import os
import datetime
import requests
from pprint import pprint
import random
import wikipedia


class wiki(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Wikipedia Cog has been loaded\n-----")

    def viki_sum(self,arg):
        definition = wikipedia.summary(arg,sentences=3,chars=1000)
        return definition

    @commands.command()
    async def pypi(self,ctx,keyword):
        try:
            r = requests.get(f"https://pypi.org/pypi/{keyword}/json").json()
            embed = discord.Embed(title=keyword)
            embed.set_author(name=r['info']['author'] + f'({r["info"]["author_email"]})')
            embed.add_field(name="Classifiers",value=r['info']['classifiers'])
            embed.description = r['info']['description'][:1021]+"..."
            await ctx.send(embed=embed)
        except Exception as ex:
            print(ex)
            await ctx.send(f'No Results found for {keyword}')



    @commands.command()
    async def wiki(self,ctx,*,word):
        embed = discord.Embed(title="***Wikipedia Search:***",description=self.viki_sum(word))
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(wiki(bot))