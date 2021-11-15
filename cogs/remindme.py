from discord.ext import commands
from utils import convertTime
import time


class RemindMe(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def remindme(self,ctx,date="10s",*,args=None):
        secs = convertTime(date)
        await ctx.reply(f"Done! I will remind you of {args} in {date} (Which is {secs} Seconds)")
        time.sleep(abs(secs))
        
        await ctx.reply("Time's up! Come here!")
    

def setup(bot):
    bot.add_cog(RemindMe(bot))


# config = {"token":configData[token],"prefix":"o!","categories": {"General":{"ping":"None","owo":"text","say":"*,args"},"Gambling":{"dice":"None","roll":"None","coin":"None"},"FUN/NSFW":{"insult":"Member","reddit":"subreddit"}}}