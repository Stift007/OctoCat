from discord.ext import commands
import discord as discord
import random

class Minesweeper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Play a Game of Minesweeper - Still in Beta")
    async def minesweeper(self,ctx):

        line1 = ""
        for i in range(5):
            line1 += random.choice(["||:white_check_mark:||","||:boom:||"])
        line2 = ""
        for i in range(5):
            line2 += random.choice(["||:white_check_mark:||","||:boom:||"])
        line3 = ""
        for i in range(5):
            line3 += random.choice(["||:white_check_mark:||","||:boom:||"])
        line4 = ""
        for i in range(5):
            line4 += random.choice(["||:white_check_mark:||","||:boom:||"])
        line5 = ""
        for i in range(5):
            line5 += random.choice(["||:white_check_mark:||","||:boom:||"])
        
        
        
        await ctx.send(f"""
            Minesweeper in a 5x5 Field.
            (Spoiler: I dont know how Many Mines I hid)
            {line1}
            {line2}
            {line3}
            {line4}
            {line5}
        """)
    

def setup(bot):
    bot.add_cog(Minesweeper(bot))
