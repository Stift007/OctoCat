import asyncio
import random
import string
from discord.ext import commands
from prsaw import RandomStuff
from data import m8ballspeech, lastDMs
import discord
from random import choice
import datetime,time

lastdms = lastDMs.lastDM

startTime = 0

class Utils(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def chat(self,ctx,*,user_input="Hello!"):
        return await ctx.send("Error: This command is currently under maintenance. Sorry for any inconvenience")
        try:
            rs = RandomStuff()
            response = rs.get_ai_response(user_input["message"])
            await ctx.send(response)
            rs.close()
        except Exception as ex:
            await ctx.send(f"Error: {ex}")

    @commands.command()
    async def servers(self,ctx):
        users=0
        for guild in self.bot.guilds:
            users += len(guild.members)
        embed = discord.Embed(title="Popularity of OctoCat",color=discord.Color.random())
        embed.add_field(name="Server Count",value=f"OctoCat is active on {len(self.bot.guilds)} Servers")
        embed.add_field(name="Member Count",value=f"Watching {users} Members")
        await ctx.send(embed=embed)


    @commands.command()
    async def uptime(self,ctx):
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
        await ctx.send(f"Time since last Bot reboot: {uptime}")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self} has been loaded")
        global startTime
        startTime = time.time()

    @commands.command()
    async def calculate(this,ctx,*,operation):
        await ctx.reply(eval(operation))
        
    @commands.command()
    async def hack(self,ctx,member:discord.Member=None):
        if not member:
            return await ctx.send("Try again but this time specify an actual Member")
        elif member.bot:
            return await ctx.send("You can't hack Bots, they're too powerful for you")

        await member.send(f"{ctx.author} Is hacking you on {ctx.guild.name} in #{ctx.channel.name}!11!!!! :grimacing:")
        msg = await ctx.send(f"Hacking {member} now...")

        await asyncio.sleep(2)
        await msg.edit(content=f"[**3.94%**] Logging into Account (2fa bypassed...)")
        await asyncio.sleep(2)
        await msg.edit(content=f"[**6.27%**] Stealing Email...")
        mailaccs = [f"{member.name}.can.haz.friends",f'{member.name}_the_nerd',f'iamvery{member.name}']
        maiservs = ['icloud.com','discord.com','youtube.com','hotmail.co.uk','freedom.fr','msn.com','web.de','octocatbot.xyz']
        password = ''.join(random.choice(string.ascii_letters+string.digits) for i in range(random.randint(8,12)))

        await asyncio.sleep(2)
        await msg.edit(content=f"[**10%**] Email hacked:\nEmail: `{random.choice(mailaccs)}@{random.choice(maiservs)}`\nPassword: `{password}`")

        await asyncio.sleep(2)
        await msg.edit(content=f"[**14,2%**] Finding IP Address...")
        await asyncio.sleep(2)
        await msg.edit(content=f"[**16.7%**] IP Found: `127.0.0.1:{random.randint(1,9999)}`")
        await asyncio.sleep(2)
        await msg.edit(content=f"[**24%**] Fetching Messages with friends... (If there are any)")
        await asyncio.sleep(2)
        await msg.edit(content=f"[**25.12%**] Last DM: `{random.choice(lastdms)}`")
        await asyncio.sleep(3)
        await msg.edit(content=f"[**29.22%**] Finding most used word...")
        await asyncio.sleep(2)
        await msg.edit(content=f"[**33.129%**] Most used Word: `{random.choice(lastDMs.mostWord)}`")
        await asyncio.sleep(2)
        await msg.edit(content=f"[**40%**] Injecting Trojan into Discriminator {member.discriminator}`")
        await asyncio.sleep(6)
        await msg.edit(content=f"[**52.49%**] Uploading Data to Reddit...")
        await asyncio.sleep(2)
        await msg.edit(content=f"[**56.2%**] Selling the Account on the Deep Web...")
        await asyncio.sleep(5)
        await msg.edit(content=f"[**60.92%**] Injecting Backdoor to PC...")
        await asyncio.sleep(2)
        await msg.edit(content=f"[**62%**] Downloading Personal Data...\n[```C:/Users/{member.name}/Homework/img1.png```]")
        for i in range(31):
            await asyncio.sleep(0.1)
            await msg.edit(content=f"[**62%**] Downloading Personal Data...\n[```C:/Users/{member.name}/Homework/img{i}.png```]")
        await asyncio.sleep(2)
        for i in range(101):
            await msg.edit(content=f"[**82.92%**] Formatting Hard Disk...\n[{i}% Complete]")
            await asyncio.sleep(0.05)

        await msg.edit(content=f"[**90.24%**] Cleaning up...")
        await asyncio.sleep(3)
        await msg.edit(content=f"[**100%**] *Totally* Real Hack Completed")
        await asyncio.sleep(2)
        
        
        
        

    @commands.command()
    async def m8ball(self,ctx,*,question):
        try:
            await ctx.send(choice(m8ballspeech.SPEECHES))
        except:
            await ctx.send("The Syntax of this command is\n\n```o!m8ball <your Question>```")

def setup(bot):
    bot.add_cog(Utils(bot))
