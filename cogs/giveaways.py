import discord
import datetime,asyncio,random
from discord.colour import Color
from discord.ext import commands
from utils import convertTime

class Giveaway(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def gstart(self,ctx:commands.Context,time=None,*,prize:str=None):
        if not time:
            return await ctx.send("Please include a Time")
        elif not prize:
            return await ctx.send("Please include a Prize")
        embed = discord.Embed(title='New Giveaway!',description=f"{ctx.author.mention} is giving away **{prize}**!")
        time_converter = {"s":1,"m":60,"h":3600,"d":86400}
        gawtime = int(time[0]*time_converter[time[-1]])
        embed.set_footer(text=f"Ends in {time}")
        gaw_msg = await ctx.send(embed=embed)

        await gaw_msg.add_reaction("🎉")
        await asyncio.sleep(gawtime)

        new_gaw_msg = await ctx.channel.fetch_message(gaw_msg.id)

        users = await gaw_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))
        winner = random.choice(users)

        await ctx.send(f":tada: {winner.mention} won {prize}! :tada:")
def setup(bot):
    bot.add_cog(Giveaway(bot))