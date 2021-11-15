from dhooks import Webhook, Embed
import discord
import psutil
import json
import random
from discord.ext import commands

Hook = Webhook("https://discord.com/api/webhooks/859019870619566081/FChbx0-7rmXgYH4VNbXKf30mDF91cxOqTVqmLdyPKn03Ip3qumAr-73jTToBHxxfNqoI")

def adjust_size(size):
    factor = 1024
    for i in ["B", "KiB", "MiB", "GiB", "TiB"]:
        if size > factor:
            size = size / factor
        else:
            return f"{size:.3f}{i}"

class Logs(commands.Cog):
	def __init__(self,bot):
		self.client = bot
	@commands.Cog.listener()
	async def on_guild_join(self,guild:discord.Guild):
		g = len(self.client.guilds)
		em = Embed(title="Bot Added",description=f"Bot was added to {guild.name}")
		em.add_field(name="Member Count",value=guild.member_count)
		em.set_footer(text=f"This is guild #{g}")
		if guild.member_count <= 2:
			em.color = 0xFF0000

		Hook.send(embed=em)

	@commands.Cog.listener()
	async def on_message(self,message):
		vram = psutil.virtual_memory()
		embed = Embed(title="CRITICAL VRAM USAGE",color=discord.Color.red())
		embed.add_field(name="Total",value=adjust_size(vram.total))
		embed.add_field(name="Available",value=adjust_size(vram.available))
		embed.add_field(name="Used",value=adjust_size(vram.used))
		embed.add_field(name="Percentage",value=adjust_size(vram.percent))
		if vram.percent >= 70:
			print(vram.percent)
			Hook.send(embed=embed)

	@commands.command()
	async def contribute(self,ctx,uname,from_video,url):

		result = json.dumps({
			"Name":uname,
			"Origin":from_video,
			"URL":url
		})

		await ctx.send("You added this: "+result)
		em = Embed(title="Contribution to the API")
		em.description = result
		Hook.send(embed=em)

	@commands.Cog.listener()
	async def on_disconnect(self):
		em = Embed(description=f"Bot disconnected")
		Hook.send(embed=em)


	@commands.Cog.listener()
	async def on_connect(self):
		em = Embed(description=f"Bot reconnected")
		Hook.send(embed=em)


	@commands.Cog.listener()
	async def on_ready(self):
		em = Embed(description=f"Bot activated")
		Hook.send(embed=em)

		

def setup(bot):
	bot.add_cog(Logs(bot))