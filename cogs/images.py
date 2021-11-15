import os
import discord
import random
from io import BytesIO
import aiohttp
from discord.ext import commands
import praw
import requests
from data import reddit
from PIL import Image

APP_ID = reddit.APP_ID
SECRET = reddit.SECRET
class Images(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def avatarfusion(this,ctx,member_1:discord.Member,member_2:discord.Member):
        asset1 = member_1.avatar_url_as(size=128)
        data1 = BytesIO(await asset1.read())
        asset2 = member_2.avatar_url_as(size=128)
        data2 = BytesIO(await asset2.read())
        background = Image.open(data1)
        foreground = Image.open(data2)

        background.paste(foreground, (0, 0), foreground)
        background.save(f"overlay{ctx.author.id}.png")
        await ctx.reply(file=discord.File(f"overlay{ctx.author.id}.png"))
        os.remove(f"overlay{ctx.author.id}.png")

    @commands.command()
    async def reddit(self,ctx,subreddit:str = ""):
        if subreddit in open("data/REDDIT_NSFW_SUBS").read() and not ctx.channel.is_nsfw():
            return await ctx.send("NSFW Subreddits are locked outside of NSFW-Marked channels.")

        subreddit = subreddit.replace("r/","")
        reddit = praw.Reddit(client_id="ON1G_de1I2-cFIaAUWB7ew",
                            client_secret="YUvMk-ZianKdX7AJ_vCQOxlLUVaHaQ",
                            user_agent="<agentOcto:1.0.0>")
        sub = reddit.subreddit(subreddit)

        subs = []

        for submission in sub.top(limit=50):
            subs.append(submission)

        random_sub = random.choice(subs)

        name = random_sub.title
        url = random_sub.url
        comments = random_sub.num_comments
        updoots  = random_sub.score
        embed = discord.Embed(title=name).set_image(url=url).set_footer(text=f"💬 {comments} / 👍 {updoots}")
        await ctx.send(embed=embed)


#This here is One of three Commands on one of 7 Extensions
    
#This here is One of three Commands on one of 7 Extensions
    @commands.command()
    async def meme(self,ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://www.reddit.com/r/memes.json") as r:
                memes = await r.json()
                embed = discord.Embed(

                    color=discord.Color.purple()
                )
                embed.set_image(url=memes["data"]["children"][random.randint(0,25)]["data"]["url"])
                embed.set_footer(text=f'Powered by r/memes | Meme requested by {ctx.author}')
                await ctx.send(embed=embed)


    @commands.command()
    async def cat(self,ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("http://aws.random.cat/meow") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Meow",color=discord.Color.random())
                    embed.set_image(url=data['file'])
                    embed.set_footer(text="http://random.cat/")

                    await ctx.send(embed=embed)

    @commands.command()
    async def dog(self,ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://random.dog/woof.json") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Woof",color=discord.Color.random())
                    embed.set_image(url=data['url'])
                    embed.set_footer(text="http://random.dog/")

                    await ctx.send(embed=embed)

    @commands.command(aliases=["floof"])
    async def fox(self,ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://randomfox.ca/floof") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Floofy",color=discord.Color.random())
                    embed.set_image(url=data['image'])
                    embed.set_footer(text="http://randomfox.ca/")

                    await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Images(bot))
