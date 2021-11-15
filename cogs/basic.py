import platform
import os
from itertools import count
import random
import socket
from discord.ext import commands
from utils import text_to_owo
from data import idconfig
import discord
import asyncio
import requests
import datetime


AllowedIDs = idconfig.allowedIDsForAds

funs = [
    "OctoCat was born during a boring online Class",
    "OctoCat was usually meant to be a Music Bot.",
    "There are many Commands that aren't listed on the `help` command..."
]

with open("data/cases.txt","r") as f:
    cases = f.read()
    cases = int(cases)


class Basic(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    def update_cases(self,case:int=1):
        global cases
        with open("data/cases.txt","w") as f:
            new_case = cases+case
            cases += case
            f.write(str(new_case))

    @commands.Cog.listener()
    async def on_ready(self):
        print("Octo is Active, Meow!")
        while True:
            print("Cleared Spam Filter")
            await asyncio.sleep(10)
            with open("data/spam_detect","r+") as f:
                f.truncate(0)

    
    @commands.Cog.listener()
    async def on_command_error(self,ctx,ex):
                
        print(ex)
        if isinstance(ex, commands.errors.MissingPermissions):
            await ctx.send("You don't have the Required Permissions to use {0.content}".format(ctx.message))
        if isinstance(ex, commands.BotMissingPermissions):
            await ctx.send("Bot doesn't have the Required Permissions to use {0.content}".format(ctx.message))

    @commands.command()
    async def ping(self,ctx):
        em = discord.Embed(title="Pinging...")
        em.add_field(name="OctoCat Server 1",value=f"<a:tloading:852534383885156413> Loading...",inline=False)
        em.add_field(name="OctoCat Server 2",value=f"...",inline=False)
        em.add_field(name="Discord",value=f"...",inline=False)
        msg = await ctx.send(embed=em)
        if platform.system().lower() == "windows":
            param = "-n"
        else:
            param = "-c"

        ip = "45.85.219.90"
        exit_code = os.system(f"ping {param} 1 -w2 {ip} > /dev/null 2>&1")
        print(exit_code)
        if(not exit_code == 0):
            em = discord.Embed(title="Pinging...")
            em.add_field(name="OctoCat Server 1",value=f":x: Not Connected",inline=False)
            em.add_field(name="OctoCat Server 2",value=f"<a:tloading:852534383885156413> Loading...",inline=False)
            em.add_field(name="Discord",value=f"...",inline=False)
        else:
            em = discord.Embed(title="Pinging...")
            em.add_field(name="OctoCat Server 1",value=f":white_check_mark: Connected",inline=False)
            em.add_field(name="OctoCat Server 2",value=f"<a:tloading:852534383885156413> Loading...",inline=False)
            em.add_field(name="Discord",value=f"...",inline=False)
        
        await msg.edit(embed=em)
        if platform.system().lower() == "windows":
            param = "-n"
        else:
            param = "-c"

        ip = "http://octocatbot.xyz"
        exit_code1 = os.system(f"ping {param} 20 -w2 {ip} > /dev/null 2>&1")
        print(exit_code1)
        if(not exit_code1 == 0):
            em = discord.Embed(title="Pinging...")
            em.add_field(name="OctoCat Server 1",value=f":x: Not Connected",inline=False)
            em.add_field(name="OctoCat Server 2",value=f":x: Not Connected",inline=False)
            em.add_field(name="Discord",value=f"<a:tloading:852534383885156413> Loading...",inline=False)
        else:
            em = discord.Embed(title="Pinging...")
            em.add_field(name="OctoCat Server 1",value=f":white_check_mark: Connected",inline=False)
            em.add_field(name="OctoCat Server 2",value=f":white_check_mark: Connected",inline=False)
            em.add_field(name="Discord",value=f"<a:tloading:852534383885156413> Loading...",inline=False)
        
        await msg.edit(embed=em)
        latency = round(self.bot.latency*1000)
        em = discord.Embed(title="Pinging...")
        em.add_field(name="OctoCat Server 1",value=f"{':white_check_mark: Connected' if exit_code == 0 else ':x: Not Connected'}",inline=False)
        em.add_field(name="OctoCat Server 2",value=f"{':white_check_mark: Connected' if exit_code1 == 0 else ':x: Not Connected'}",inline=False)
        em.add_field(name="Discord",value=f":white_check_mark: Connected - {latency}",inline=False)
        await msg.edit(embed=em)
        

    @commands.command()
    async def stonks(self,ctx):
	    await ctx.send("https://i.kym-cdn.com/entries/icons/facebook/000/029/959/Screen_Shot_2019-06-05_at_1.26.32_PM.jpg")

    @commands.command()
    async def funfact(self,ctx):
        embed = discord.Embed()
        embed.description = random.choice(funs)
        await ctx.send(embed=embed)

    @commands.command()
    async def owo(self,ctx):
        await ctx.send(text_to_owo(ctx.message.content.replace("o!owo","")))

    @commands.command()
    async def avatar(self, ctx):
        embed = discord.Embed(title=f"{ctx.author}'s Avatar")
        embed.set_image(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Basic(bot))
