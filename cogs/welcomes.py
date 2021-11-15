from discord.ext import commands
import json


class WelcomeAndBye(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    async def open_json(self,guild):
        with open("data/welcomeByes.json","r") as f:
            content = json.load(f)
        if str(guild.id) not in content:
            content[str(guild.id)] = {}
            content[str(guild.id)]["welcome"] = "none"
            content[str(guild.id)]["bye"] = "none"
            with open("data/welcomeByes.json","w+") as f:
                json.dump(content,f)
            return True
        return False

    @commands.command()
    async def setwelcome(self,ctx,*,message):
        await self.open_json(ctx.guild)
        with open("data/welcomeByes.json","r") as f:
            data = json.load(f)
        data["welcome"] = message
        with open("data/welcomeByes.json","w+") as f:
            json.dump(data,f)
        await ctx.send(f"Welcome Message Configured Successfully! (Now set to {message})")


    @commands.command()
    async def resetwelcome(self,ctx):
        await self.open_json(ctx.guild)
        with open("data/welcomeByes.json","r") as f:
            data = json.load(f)
        data["welcome"] = "none"
        with open("data/welcomeByes.json","w+") as f:
            json.dump(data,f)
        await ctx.send(f"Welcome Message Configured Successfully! (Now set to none)")

    @commands.command()
    async def setexitmsg(self,ctx,*,message):
        await self.open_json(ctx.guild)
        with open("data/welcomeByes.json","r") as f:
            data = json.load(f)
        data["bye"] = message
        with open("data/welcomeByes.json","w+") as f:
            json.dump(data,f)
        await ctx.send(f"Exit Message Configured Successfully! (Now set to {message})")


    @commands.command()
    async def resetexitmsg(self,ctx):
        await self.open_json(ctx.guild)
        with open("data/welcomeByes.json","r") as f:
            data = json.load(f)
        data["bye"] = "none"
        with open("data/welcomeByes.json","w+") as f:
            json.dump(data,f)
        await ctx.send(f"Exit Message Configured Successfully! (Now set to none)")
    
    @commands.Cog.listener()
    async def on_member_join(self,member):
        await self.open_json(member.guild)
        with open("data/welcomeByes.json","r") as f:
            data = json.load(f)
        if data[str(member.guild.id)]["welcome"] != "none":
            await member.send(data[str(member.guild.id)]["welcome"])

    
    @commands.Cog.listener()
    async def on_member_leave(self,member):
        await self.open_json(member.guild)
        with open("data/welcomeByes.json","r") as f:
            data = json.load(f)
        if data[str(member.guild.id)]["bye"] != "none":
            await member.send(data[str(member.guild.id)]["bye"])


def setup(bot):
    bot.add_cog(WelcomeAndBye(bot))


# config = {"token":configData[token],"prefix":"o!","categories": {"General":{"ping":"None","owo":"text","say":"*,args"},"Gambling":{"dice":"None","roll":"None","coin":"None"},"FUN/NSFW":{"insult":"Member","reddit":"subreddit"}}}