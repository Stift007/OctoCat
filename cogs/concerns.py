from discord.ext import commands



class OwnerRequests(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def deletePersonalData(self,ctx,*,reason="Unspecified"):
            await ctx.author.send(f"Your Request has been submitted. The Bot Developers will delete your Personal Data ASAP.")
            await self.bot.get_guild(828300715616895006).get_channel(828300716891308091).send(f"{ctx.author} ({ctx.author.id}) requested A Removal of all of his Personal Data.\nReason: {reason}")

            
    @commands.command()
    async def issue(self,ctx,*,reason=None):
        if not reason:
            await ctx.author.send(f"Please Specify a reason")
        await ctx.author.send(f"Your Request has been submitted. The Bot Developers will take a look ASAP.")
        await self.bot.get_guild(828300715616895006).get_channel(828300716891308091).send(f"{ctx.author} ({ctx.author.id}) Issued a Security Problem.\nReason: {reason}")

    

def setup(bot):
    bot.add_cog(OwnerRequests(bot))


# config = {"token":configData[token],"prefix":"o!","categories": {"General":{"ping":"None","owo":"text","say":"*,args"},"Gambling":{"dice":"None","roll":"None","coin":"None"},"FUN/NSFW":{"insult":"Member","reddit":"subreddit"}}}