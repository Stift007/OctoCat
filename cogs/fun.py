from discord.ext import commands
import discord
import requests
import random

class Fun(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def gayrate(self, ctx,member:discord.Member=None):
        em = discord.Embed()
        em.description = f":rainbow: {member.name or ctx.author.name} is {random.randint(1,100)}% Gay :rainbow:"
        await ctx.send(embed=em)

    

    @commands.command()
    async def quote_message(self,ctx,_id):
        embed = discord.Embed()
        embed.set_author(icon_url=ctx.author.avatar_url,name=ctx.author)
        msg = ctx.channel.fetch_message(_id)
        embed.description = msg.content + f"\n\n\n[Jump to Message!]({msg.url})"
        await ctx.send(embed=embed)

    @commands.command()
    async def chucknorris(self,ctx):
        r = requests.get("https://api.chucknorris.io/jokes/random")
        joke = r.json()
        embed = discord.Embed(title="Chuck Norris Joke!")
        embed.set_thumbnail(url=joke["icon_url"])
        embed.description = joke["value"]
        await ctx.send(embed=embed)

    

    

def setup(bot):
    bot.add_cog(Fun(bot))


# config = {"token":configData[token],"prefix":"o!","categories": {"General":{"ping":"None","owo":"text","say":"*,args"},"Gambling":{"dice":"None","roll":"None","coin":"None"},"FUN/NSFW":{"insult":"Member","reddit":"subreddit"}}}