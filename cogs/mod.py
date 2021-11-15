from discord.ext import commands
import discord as discord
import json
import asyncio

#with open("data/modlog.json","r") as f:
#    cases = json.load(f)

    
class Moderation(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    """def update_cases(self,case:int=1):
        global cases
        with open("data/modlog.json","w") as f:
#            new_case = cases["modInit"]+case
 #           cases["modInit"] += case
  #          json.dump(cases,f)
            return
    def updateDeletedMessages(self,case:int=1):
        global cases
        self.update_cases(case)
        with open("data/modlog.json","w") as f:
            #cases["deletedMessages"] += case
            #json.dump(cases,f)
            return

    def updateMutes(self,case:int=1):
        global cases
        self.update_cases(case)
        with open("data/modlog.json","w") as f:
            cases["mutes"] += case
            json.dump(cases,f)

    def updateBans(self,case:int=1):
        global cases
        self.update_cases(case)
        with open("data/modlog.json","w") as f:
            cases["bans"] += case
            json.dump(cases,f)

    def updateKicks(self,case:int=1):
        global cases
        self.update_cases(case)
        with open("data/modlog.json","w") as f:
            cases["kicks"] += case
            json.dump(cases,f)

    def updateUnmutes(self,case:int=1):
        global cases
        self.update_cases(case)
        with open("data/modlog.json","w") as f:
            cases["unmutes"] += case
            json.dump(cases,f)
"""



    @commands.Cog.listener()
    async def on_message(self,message):

        banned_words =[] #["fuck",
        # "nigg",
        # "fuk",
        # "cunt",
        # "cnut",
        # "bitch",
        # "dick",
        # "d1ck",
        # "pussy",
        # "asshole",
        # "b1tch",
        # "b!tch",
        # "blowjob",
        # "cock",
        # "c0ck"]

        for i in banned_words:
                    if i in message.content.lower() and not message.channel.is_nsfw():
                        await message.delete()
                        await message.author.send(f"Your Message - {message.content} - contains one or more banned words and has therefore been deleted")
                        self.updateDeletedMessages()


        global cases
        TeamRole = discord.utils.get(message.guild.roles,name="Team")

        if message.author.bot:
            return

        
        counter = 0
        member = message.author
        with open("data/spam_detect","r+") as f:
            for lines in f:
                if lines.strip("\n") == str(message.author.id):
                    counter +=1
            f.write(f"{str(message.author.id)}\n")
            if counter > 10:
                guild = message.guild
                mutedRole = discord.utils.get(guild.roles,name="Muted")
                member = message.author

                if not mutedRole:
                    mutedRole = await guild.create_role(name="Muted")

                    for channel in guild.channels:
                        await channel.set_permissions(mutedRole, speak=False,send_messages=False, read_message_history=False,read_messages=False)

                await message.author.add_roles(mutedRole,reason=f"Mass-Spamming in #{message.channel.name}")
                embed = discord.Embed(title = f"Muted {member}",color=0xFFFA00)
                embed.add_field(name="User",value=f"{member.name}#{member.discriminator} ({member.id})")
                embed.add_field(name="Moderator",value=f"OctoCat#2397")
                embed.add_field(name="Reason",value=f"Mass-Spamming in #{message.channel.name} | 2d",inline=False)
                await message.channel.send(embed=embed)
                try:
                    await member.send(f"You were muted from {guild.name}, Mass-Spamming {message.channel.name}")
                except:
                    pass        
                await asyncio.sleep(172800)
                await member.remove_roles(mutedRole)
                await self.updateUnmutes()
                embed = discord.Embed(title=f"Unmuted {member}",color=0x00FF2C)
                embed.add_field(name="User",value=f"{member.name}#{member.discriminator} ({member.mention})")
                embed.add_field(name="Moderator",value=f"OctoCat#2397")
                embed.add_field(name="Reason",value=f"Time's up",inline=False)
                await message.channel.send(embed=embed)
            
        if message.content.lower() == "good bot":
            await message.add_reaction("👍")

        elif message.content.lower() == "are you a good bot?":
    	    await message.channel.send("https://preview.redd.it/36amh4mmue341.png?auto=webp&s=3c8e7a3bab38f3cd527888584e470f1f9a43ed19")

    
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self,ctx,amt:int=2):
        await ctx.channel.purge(limit=amt)

    @commands.command(aliases=["sm"])
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self,ctx,seconds:int=0):
        try:
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.send(f"Slow Mode is now {seconds} Seconds!")
        except Exception as ex:
            await ctx.send(f"Cannot set Slowmode - {ex}")

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self,ctx, member: discord.Member=None,*, nick=None):
        if not member:member=ctx.author
        if not nick:nick=ctx.author.name
        await member.edit(nick=nick)
        await ctx.send(f'Nicked {member.mention} to {nick}!')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self,ctx,member : discord.Member=None,*,reason:str="Reason Not Provided"):
        global cases
        if member:
            try:
                embed = discord.Embed(description = f"Kicked {member}",color=discord.Color.green())
                await member.ban(reason=reason)
                await ctx.send(embed=embed)
                try:
                    await member.send(f"You were kicked from {ctx.guild.name}, {reason}")
                except:
                    pass    

            except Exception as ex:
                await ctx.send(f"Cannot kick {member} - {ex}")
        else:
            await ctx.send("Please specify a User to kick via @mention")
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def unban(self,ctx,*,member=None):
        if not member:
            return await ctx.send("Please specify a Member - Like this: o!unban member#1234")
        global cases
        bannedUsers = await ctx.guild.bans()
        try:
            name,discriminator = member.split("#")
        except:
            return await ctx.send("Please specify a Member - Like this: o!unban member#1234")


        for ban in bannedUsers:
            user = ban.user

            if(user.name,user.discriminator) == (name,discriminator):
                await ctx.guild.unban(user)
                embed = discord.Embed(title = f"{member} was unbanned",color=0x00FF2C)
                
                await ctx.send(embed=embed)
        await ctx.send(f"{member} Wasn't found")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def mute(self,ctx,member : discord.Member=None,*,reason:str="Because"):
#        return await ctx.send("Please Specify a Member to mute or refer to o!help") if not member
        global cases
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles,name="Muted")

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False,send_messages=False, read_message_history=False,read_messages=False)

        await member.add_roles(mutedRole,reason=reason)
        embed = discord.Embed(description = f"Muted {member}",color=0xFFFA00)
        await ctx.send(embed=embed)
        try:
            await member.send(f"You were muted from {ctx.guild.name}, {reason}")
        except:
            pass
    

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def rero(self,ctx, *,role: discord.Role):
        if ctx.author.id == 576187414033334282:
            if role is None:
                await ctx.send('Please write *correct role name* to delete') 

        try:
            await role.delete()
            await ctx.send(f'{role} was **yeeted**!')

        except discord.Forbidden:
            await ctx.send('I do not have permission to delete this role')
            
    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self,ctx,member : discord.Member=None,*,reason:str="Because"):
        global cases
        
        if member:
            try:
                embed = discord.Embed(description = f"Banned {member}",color=discord.Color.green())
                await member.ban(reason=reason)
                await ctx.send(embed=embed)
                self.update_cases()
                try:
                    await member.send(f"You were banned from {ctx.guild.name}, {reason}")
                except:
                    pass    

            except Exception as ex:
                await ctx.send(f"Cannot ban {member} - {ex}")
        else:
            await ctx.send("Please specify a User to ban via @mention")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self,ctx,member: discord.Member,*,reason:str=""):
        global cases
        mutedRole = discord.utils.get(ctx.guild.roles,name="Muted")
        await member.remove_roles(mutedRole)
        embed = discord.Embed(title=f"{member} was unmuted",color=discord.Color.green())
        await ctx.send(embed=embed)

        #await ctx.send(f"Unmuted {member.mention}!")

def setup(bot):
    bot.add_cog(Moderation(bot))
