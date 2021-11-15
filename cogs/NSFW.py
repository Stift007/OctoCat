from utils import get_momma_jokes
from discord.ext import commands
import discord



class NSFW(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def insult(self,ctx,member : discord.Member = None):
        insult = await get_momma_jokes()
        if member:
            await ctx.send(f"{member.name} eat this: {insult} ")
        else:
            await ctx.send(f"Hey, {ctx.author.name} this one's for you: {insult} ")

def setup(bot):
    bot.add_cog(NSFW(bot))