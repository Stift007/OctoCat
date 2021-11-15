import discord
from discord.ext import commands



class Test_(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def say(self,ctx,*,args):
        
        if "@" in args.lower():
            return await ctx.author.send("You can't use the say-command to let me mention People. Sorry, but no.")
        await ctx.send(args)

    # @commands.Cog.listener()
    # async def on_message(self,m):
    #     #####################
    #     # DAD JOKES INCOMING

    #     # Removing words like I'm or Im
    #     mc = m.content
    #     mc = mc.replace("I'm","I am")
    #     mc = mc.replace("Im","I am")
    #     mc = mc.replace("I is","I am")
    #     try:
    #         name = mc.split("I am")[1]
    #         embed = discord.Embed()
    #         embed.description = f'Hey {name}, I\'m OctoCat!'
    #         embed.set_footer(text="*I am a bot, and this action was performed automatically. Please contact the Developers if you have any questions or concerns.*")
    #         await m.reply(embed=embed)
    #     except:
    #         pass
    #     await self.bot.process_commands(m)

    

def setup(bot):
    bot.add_cog(Test_(bot))


# config = {"token":configData[token],"prefix":"o!","categories": {"General":{"ping":"None","owo":"text","say":"*,args"},"Gambling":{"dice":"None","roll":"None","coin":"None"},"FUN/NSFW":{"insult":"Member","reddit":"subreddit"}}}