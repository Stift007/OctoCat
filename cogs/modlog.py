import asyncio
from discord import colour
from discord.ext import commands
import discord as discord
from discord_components import DiscordComponents,Button,ButtonStyle,InteractionEventType
import json
import datetime

class SysLog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    async def edit_role_json(self,guild,channel:discord.Role, verified:discord.Role):
        await self.open_modlog_json(guild,channel.id)
        with open("data/channels.json","r") as f:
            config = json.load(f)
        
        config[str(guild.id)]["role"] = str(channel.id)
        config[str(guild.id)]["verified"] = str(verified.id)
        with open("data/channels.json","w+") as f:
            json.dump(config,f)


    async def open_role_json(self,guild,channel="", verified:discord.Role=""):
        with open("data/channels.json","r") as f:
            config = json.load(f)
            print(config)
        if str(guild.id) in config:
            return False
        config[str(guild.id)] = {}
        config[str(guild.id)]["role"] = str(channel.id)
        config[str(guild.id)]["verified"] = str(verified.id)
        with open("data/channels.json","w+") as f:
            json.dump(config,f)

    async def edit_modlog_json(self,guild,channel:discord.TextChannel):
        await self.open_modlog_json(guild,channel.id)
        with open("data/channels.json","r") as f:
            config = json.load(f)
        
        config[str(guild.id)]["MODLOG"] = str(channel.id)
        with open("data/channels.json","w+") as f:
            json.dump(config,f)


    async def open_modlog_json(self,guild,channel=""):
        with open("data/channels.json","r") as f:
            config = json.load(f)
            print(config)
        if str(guild.id) in config:
            return False
        config[str(guild.id)] = {}
        config[str(guild.id)]["MODLOG"] = str(channel)
        with open("data/channels.json","w+") as f:
            json.dump(config,f)

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def set_modlog_channel(self,ctx,channel:discord.TextChannel=None):
        if not channel:
            return await ctx.send("Please mention a Channel!")
        await self.open_modlog_json(ctx.guild,channel.id)
        await self.edit_modlog_json(ctx.guild,channel)
        em = discord.Embed(title="This is the new Mod Log Channel!",color=discord.Color.green())
        await channel.send(embed=em)

        
    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def set_auto_role(self,ctx,role:discord.Role=None,verified:discord.Role=None):
        if not role:
            return await ctx.send("Please mention a Channel!")
        await self.open_role_json(ctx.guild,role,verified)
        await self.edit_role_json(ctx.guild,role,verified)
        em = discord.Embed(title=f"{role.mention} is the new Autorole!",color=discord.Color.green())
        await ctx.send(embed=em)


    @commands.Cog.listener()
    async def on_member_join(self,member:discord.Member):
        await self.open_modlog_json(member.guild)
        await self.open_role_json(member.guild)
        guild:discord.Guild = member.guild
        with open("data/channels.json","r") as f:
            config = json.load(f)
        if config[str(guild.id)]["MODLOG"] != "":
                c = guild.get_channel(int(config[str(guild.id)]["MODLOG"]))
                em = discord.Embed(title="➡️ New Member!",color=discord.Color.green())
                em.description = f"Hello, {member}! \nWe hope you'll enjoy your stay in **{guild.name}**!"
                em.set_thumbnail(url=member.avatar.url)
                em.set_footer(text=f"This is User {len(guild.members)} - ID: {member.id}")
                await c.send(embed=em)
                if config[str(guild.id)]["role"] != "" and config[str(guild.id)]["verified"] != "":
                    try:
                        ar = guild.get_role(int(config[str(guild.id)]["role"]))
                        vr = guild.get_role(int(config[str(guild.id)]["role"]))
                        await member.add_roles(ar)
                        embed = discord.Embed(title=f"Verify for {guild.name}",
                        description="Please press the *green* Button to verify",
                        color=discord.Color.blurple()
                        )
                        embed.set_footer(text="*I am a bot, and this action was performed automatically. Please [contact the Developers](http://45.85.219.90:4000/support) if you have any questions or concerns.*")
                        msg = await c.send(embed=embed,
                            components=[
                                [
                                    Button(style=ButtonStyle.red,label="No",emoji="❌"),
                                    Button(style=ButtonStyle.green,label="Verify",emoji="✅")
                                ],
                            ],
                        )

                        def check(resp):
                            return member == resp.user and c == resp.channel

                        try:
                            resp = self.bot.wait_for("button_click",check=check,timeout=15)

                        except asyncio.TimeoutError:
                            tembed = discord.Embed(title="Verification expired")
                            tembed.set_footer(text="*I am a bot, and this action was performed automatically. Please [contact the Developers](http://45.85.219.90:4000/support) if you have any questions or concerns.*")
                            tembed.description = "You took too long and the Verification link has expired."
                            tembed.color=discord.Color.red()
                            await msg.edit(
                                embed=tembed,
                                components=[
                                    Button(style=ButtonStyle.red, label="Timeout!",disabled=True)
                                ]
                            )
                        
                        if resp.component.label == "No":
                            await resp.respond(content="Alright then, keep your Secrets")

                        if resp.component.label == "Verify":
                            await member.remove_roles(ar)
                            await member.add_roles(vr)
                            await member.send("You have been verified!")
                    except Exception as ex:
                        await c.send(ex)


    @commands.command()
    async def verify(self,ctx):
                    try:
                            
                        guild = ctx.guild
                        c = ctx.channel
                        member = ctx.author
                        await self.open_modlog_json(member.guild)
                        await self.open_role_json(member.guild)
                        guild:discord.Guild = member.guild
                        with open("data/channels.json","r") as f:
                            config = json.load(f)
                        ar = guild.get_role(int(config[str(guild.id)]["role"]))
                        vr = guild.get_role(int(config[str(guild.id)]["role"]))
                        await member.add_roles(ar)
                        embed = discord.Embed(title=f"Verify for {guild.name}",
                        description="Please press the *green* Button to verify",
                        color=discord.Color.blurple()
                        )
                        embed.set_footer(text="*I am a bot, and this action was performed automatically. Please [contact the Developers](http://45.85.219.90:4000/support) if you have any questions or concerns.*")
                        msg = await ctx.send(embed=embed,
                            components=[
                                [
                                    Button(style=ButtonStyle.red,label="No",emoji="❌"),
                                    Button(style=ButtonStyle.green,label="Verify",emoji="✅")
                                ],
                            ],
                        )

                        def check(resp):
                            return member == resp.user and c == resp.channel

                        try:
                            resp = await self.bot.wait_for("button_click",check=check,timeout=15)

                        except asyncio.TimeoutError:
                            tembed = discord.Embed(title="Verification expired")
                            tembed.set_footer(text="*I am a bot, and this action was performed automatically. Please [contact the Developers](http://45.85.219.90:4000/support) if you have any questions or concerns.*")
                            tembed.description = "You took too long and the Verification link has expired."
                            tembed.color=discord.Color.red()
                            tembed.set_footer(text="*I am a bot, and this action was performed automatically. Please [contact the Developers](http://45.85.219.90:4000/support) if you have any questions or concerns.*")
                        
                            await msg.edit(
                                embed=tembed,
                                components=[
                                    Button(style=ButtonStyle.red, label="Timeout!",disabled=True)
                                ]
                            )
                        
                        if resp.component.label == "No":
                            await ctx.respond(content="Alright then, keep your Secrets")

                        if resp.component.label == "Verify":
                            await member.remove_roles(ar)
                            await member.add_roles(vr)
                            await member.send("You have been verified!")
                    except Exception as ex:
                        await ctx.send(ex)


    
    @commands.Cog.listener()
    async def on_member_remove(self,member:discord.Member):
        guild:discord.Guild = member.guild
        with open("data/channels.json","r") as f:
            config = json.load(f)
        if config[str(guild.id)]["MODLOG"] != "":
                c = guild.get_channel(int(config[str(guild.id)]["MODLOG"]))
                
                em = discord.Embed(title="⬅️ Member Left!",color=discord.Color.red())
                em.description = f"{member} Left the Server."
                em.set_thumbnail(url=member.avatar.url)
                em.set_footer(text=f"We are now {len(guild.members)} - ID: {member.id}")
                await c.send(embed=em)


    

def setup(bot):
    bot.add_cog(SysLog(bot))


# config = {"token":configData[token],"prefix":"o!","categories": {"General":{"ping":"None","owo":"text","say":"*,args"},"Gambling":{"dice":"None","roll":"None","coin":"None"},"FUN/NSFW":{"insult":"Member","reddit":"subreddit"}}}