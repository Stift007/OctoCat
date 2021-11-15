from discord.ext import commands
import praw
import anime_images_api
from data import reddit
import hmtai
APP_ID = reddit.APP_ID
SECRET = reddit.SECRET
import discord
import random

class AnimeImages(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.Reddit = None
        if APP_ID and SECRET:
            self.Reddit = praw.Reddit(client_id=APP_ID,client_secret=SECRET,user_agent="OctoCat:%s1.0" % APP_ID)
    
    @commands.command()
    async def hug(self,ctx,member:discord.Member=None):
        if not member:
            return await ctx.send("Please specify a member!")
        embed = discord.Embed(title=f"{ctx.author.name} hugs {member.name}! Don't squeeze too hard!")
        anime = anime_images_api.Anime_Images()
        sfw = anime.get_sfw('hug')
        embed.set_image(url=sfw)
        await ctx.send(embed=embed)

    @commands.command()
    async def kiss(self,ctx,member:discord.Member=None):
        if not member:
            return await ctx.send("Please specify a member!")
        embed = discord.Embed(title=f"{ctx.author.name} kisses {member.name}! :heart:")
        anime = anime_images_api.Anime_Images()
        sfw = anime.get_sfw('kiss')
        embed.set_image(url=sfw)
        await ctx.send(embed=embed)

    @commands.command()
    async def slap(self,ctx,member:discord.Member=None):
        if not member:
            return await ctx.send("Please specify a member!")
        embed = discord.Embed(title=f"{ctx.author.name} slaps {member.name}! Ouch!")
        anime = anime_images_api.Anime_Images()
        sfw = anime.get_sfw('slap')
        embed.set_image(url=sfw)
        await ctx.send(embed=embed)


    @commands.command()
    async def wink(self,ctx,member:discord.Member=None):
        if not member:
            return await ctx.send("Please specify a member!")
        embed = discord.Embed(title=f"{ctx.author.name} winks at {member.name}! 😉")
        anime = anime_images_api.Anime_Images()
        sfw = anime.get_sfw('wink')
        embed.set_image(url=sfw)
        await ctx.send(embed=embed)

    @commands.command()
    async def pat(self,ctx,member:discord.Member=None):
        if not member:
            return await ctx.send("Please specify a member!")
        embed = discord.Embed(title=f"{ctx.author.name} pats {member.name}!")
        anime = anime_images_api.Anime_Images()
        sfw = anime.get_sfw('pat')
        embed.set_image(url=sfw)
        await ctx.send(embed=embed)

    @commands.command()
    async def kill(self,ctx,member:discord.Member=None):
        if not member:
            return await ctx.send("Please specify a member!")
        embed = discord.Embed(title=f"{ctx.author.name} kills {member.name}! Brutal!")
        anime = anime_images_api.Anime_Images()
        sfw = anime.get_sfw('kill')
        embed.set_image(url=sfw)
        await ctx.send(embed=embed)

    @commands.command()
    async def cuddle(self,ctx,member:discord.Member=None):
        if not member:
            return await ctx.send("Please specify a member!")
        embed = discord.Embed(title=f"{ctx.author.name} cuddles with {member.name} 😊")
        anime = anime_images_api.Anime_Images()
        sfw = anime.get_sfw('cuddle')
        embed.set_image(url=sfw)
        await ctx.send(embed=embed)

    @commands.command()
    async def boobs(self,ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send(f"{ctx.author.mention}, Please use that in an NSFW Channel.")
            return
        embed = discord.Embed()
        anime = anime_images_api.Anime_Images()
        nsfw = anime.get_nsfw('boobs')
        embed.set_image(url=nsfw)
        await ctx.send(embed=embed)

    @commands.command()
    async def hentai(self,ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send(f"{ctx.author.mention}, Please use that in an NSFW Channel.")
            return
        embed = discord.Embed()
        anime = anime_images_api.Anime_Images()
        nsfw = anime.get_nsfw('hentai')
        embed.set_image(url=nsfw)
        await ctx.send(embed=embed)
        

    @commands.command(aliases=["am"])
    async def animeme(self, ctx):
        async with ctx.channel.typing():
            try:
                subreddit = self.Reddit.subreddit("animememes")
                all_subs = []

                top = subreddit.top(limit=500)

                for submission in top:
                    all_subs.append(submission)

                random_sub = random.choice(all_subs)

                name = random_sub.title
                url  = random_sub.url

                embed = discord.Embed(title=name,color=discord.Color.blue())

                author = random_sub.author
                embed.description=f"Posted by {author}"

                embed.set_image(url=url)

                if submission.over_18():
                    if ctx.channel.is_nsfw():
                                
                        msg = await ctx.send(embed=embed)
                        await msg.add_reaction('👍')
                        await msg.add_reaction('👎')
                    else:
                        await ctx.send("Cannot send NSFW Content to non-NSFW Channel!") 

                else:
                    
                    msg = await ctx.send(embed=embed)
                    await msg.add_reaction('👍')
                    await msg.add_reaction('👎')
            except Exception as ex:
                await ctx.send(ex)

    @commands.command()
    async def blowjob(self, ctx,member:discord.Member=None,*,args=""):
        if not ctx.channel.is_nsfw():
            return await ctx.send("Command blocked outside of NSFW Channels")

        if not member:
            return await ctx.send("you forgot to specify a member!")

        embed=discord.Embed(title=f"{ctx.author} blowjobs {member} {args}").set_image(url=hmtai.useHM("v1","blowjob"))
        await ctx.send(embed=embed)

    @commands.command()
    async def footjob(self, ctx,member:discord.Member=None,*,args=""):
        if not ctx.channel.is_nsfw():
            return await ctx.send("Command blocked outside of NSFW Channels")
        
        if not member:
            return await ctx.send("you forgot to specify a member!")
        embed=discord.Embed(title=f"{ctx.author} footjobs {member} {args}").set_image(url=hmtai.useHM("v1","foot"))
        await ctx.send(embed=embed)


   
def setup(bot):
    bot.add_cog(AnimeImages(bot))


# config = {"token":configData[token],"prefix":"o!","categories": {"General":{"ping":"None","owo":"text","say":"*,args"},"Gambling":{"dice":"None","roll":"None","coin":"None"},"FUN/NSFW":{"insult":"Member","reddit":"subreddit"}}}