import random

from discord.ext import commands



class Gambling(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def roll(self,ctx):
        n = random.randrange(1,101)
        await ctx.send(f"You rolled a {n}")

    @commands.command()
    async def dice(self,ctx):
        n = random.randrange(1,7)
        await ctx.send(f"{n}")
    
    @commands.command()
    async def coin(self,ctx):
        n = random.randint(0,1)
        await ctx.send(f"Heads" if n == 1 else "Tails")

def setup(bot):
    bot.add_cog(Gambling(bot))