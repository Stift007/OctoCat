from discord.channel import TextChannel
from discord.ext import commands
import discord
import asyncio
import datetime

class Admin(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    

    @commands.command()
    async def whois(self,ctx,member:discord.Member=None):
        if not member:
            member=ctx.author
            roles = [role for role in ctx.author.roles]
        else:
            roles = [role for role in ctx.author.roles]

        embed = discord.Embed(title=f"{member}", colour=member.colour, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_author(name="Detailed User Info: ")
        embed.add_field(name="ID:", value=member.id, inline=False)
        embed.add_field(name="User Name:",value=member.display_name, inline=False)
        embed.add_field(name="Discriminator:",value=member.discriminator, inline=False)
        embed.add_field(name="Current Status:", value=str(member.status).title(), inline=False)
        embed.add_field(name="Current Activity:", value=f"{str(member.activity.type).title().split('.')[1]} {member.activity.name}" if member.activity is not None else "None", inline=False)
        embed.add_field(name="Created At:", value=member.created_at.strftime("%a, %d, %B, %Y, %I, %M, %p UTC"), inline=False)
        embed.add_field(name="Joined At:", value=member.joined_at.strftime("%a, %d, %B, %Y, %I, %M, %p UTC"), inline=False)
        embed.add_field(name=f"Roles [{len(roles)}]", value=" **|** ".join([role.mention for role in roles]), inline=False)
        embed.add_field(name="Top Role:", value=member.top_role, inline=False)
        embed.add_field(name="Bot?:", value=member.bot, inline=False)
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)
        return

    
    @commands.command()
    async def serverinfo(self,ctx):
        guild  = ctx.guild
        bots   = 0
        humans = 0
        textChannels = len(guild.text_channels)
        voiceChannels = len(guild.voice_channels)
        for member in guild.members:
            if member.bot:
                bots += 1
            else:
                humans += 1
        embed = discord.Embed(title=f"{guild.name}", colour=discord.Colour.random(), timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar.url)
        embed.add_field(name="Generic Info",value=f"❯ **Name**: {guild.name}\n❯ **ID**: {guild.id}\n❯ **Owner**: {guild.owner}\n❯ **Region**: {guild.region}\n❯ **Created At**: {guild.created_at}\n\n",inline=False)
        embed.add_field(name="Statistics",value=f"❯ **Role Count**: {len(guild.roles)}\n❯ **Member Count**: {guild.member_count}\n❯ **Humans**: {humans}\n❯ **Bots**:{bots}\n❯ **Text Channels**: {textChannels}\n❯ **Voice Channels**: {voiceChannels}",inline=False)
        await ctx.send(embed=embed)
        return



    @commands.command()
    async def userinfo(self,ctx,member:discord.Member=None):
        if not member:member=ctx.author
        em = discord.Embed(title=f"Basic Information about {member.name}",description=member.mention, color = discord.Color.green())
        em.add_field(name= "ID",value=member.id)
        em.set_thumbnail(url=member.avatar.url)
        em.set_footer(icon_url=ctx.author.avatar_url,text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=em)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reload(self,ctx,cog : str):
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            em = discord.Embed(title="Whoops!",description="Cannot load this Extension",color=discord.Color.red())
            em.add_field(name="Error Details",value=f"The Extension you wanted to enable returned the following Error: {e}.",inline=False)
            em.add_field(name="If Problems continue...",value="If Problems continue, Tell us on the [Support Server](https://discord.gg/287BTjesCe) with !error <your error>",inline=False)
            await ctx.send(embed=em)
            return
        await ctx.send(f"Cog {cog} has been reloaded!")
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unload(self,ctx,cog : str):
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            em = discord.Embed(title="Whoops!",description="Cannot load this Extension",color=discord.Color.red())
            em.add_field(name="Error Details",value=f"The Extension you wanted to disable returned the following Error: {e}.",inline=False)
            em.add_field(name="If Problems continue...",value="If Problems continue, Tell us on the [Support Server](https://discord.gg/287BTjesCe) with !error <your error>",inline=False)
            await ctx.send(embed=em)
            return
        await ctx.send(f"Cog {cog} has been unloaded!")
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def refresh(self,ctx,cog : str):
        if cog == "cogs.admin":
            await ctx.send("Cannot rebuild Administration Cog - This might result in an unusable Bot.")
            return
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            em = discord.Embed(title="Whoops!",description="Cannot refresh this Extension",color=discord.Color.red())
            em.add_field(name="Error Details",value=f"The Extension you wanted to rebuild returned the following Error: {e}.",inline=False)
            em.add_field(name="If Problems continue...",value="If Problems continue, Tell us on the [Support Server](https://discord.gg/287BTjesCe) with !error <your error>",inline=False)
            await ctx.send(embed=em)
            return
        await ctx.send(f"Cog {cog} has been rebuilt!")

def setup(bot):
    bot.add_cog(Admin(bot))