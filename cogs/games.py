from discord.ext import commands
import asyncio
import random
from data import ToDData
import time


class Game(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def ToD(self,ctx,tod="truth"):
        if tod.lower() == "truth":
            if random.randint(0,1) == 1:
                await ctx.send(random.choice(ToDData.SUPRISED_TRUTH_REACTIONS))
                await asyncio.sleep(random.randint(1,3))
            await ctx.send(random.choice(ToDData.TRUTHS))
            await asyncio.sleep(5)
            await ctx.send(random.choice(ToDData.APOLOGIZES_TRUTH))
        elif tod.lower() == "dare":
            if random.randint(0,1) == 1:
                await ctx.send(random.choice(ToDData.SURPRISED_DARE_REACTIONS))
                await asyncio.sleep(random.randint(1,3))
            await ctx.send(random.choice(ToDData.DARES))
            await asyncio.sleep(5)
            await ctx.send(random.choice(ToDData.APOLOGIZES_DARE))

def setup(bot):
    bot.add_cog(Game(bot))