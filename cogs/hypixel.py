import json
import discord
from datetime import datetime, time
import json
from discord.ext import commands
from pprint import PrettyPrinter,pprint
import requests


class Hypixel(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        with open("data/minestats.json","r") as f:
            self.data = json.load(f)

        uuid = "db14a367-08b1-4432-a6d8-4200b69c9083"
        uuid_dashed = "db14a367-08b1-4432-a6d8-4200b69c9083"
        self.API_KEY = "ef31f74e-3700-4f99-a572-a96341c19c31"


    @commands.command()
    async def minehut(self,ctx,arg):
        self.data["minehut"] += 1
        self.data["totalRequestsPosted"] += 1
        msg = await ctx.send("Fetching Data from API...")
        r = requests.get('https://api.minehut.com/server/'+arg+'?byname=True')
        json_data = r.json()
        if 'ok' in json_data:
            if json_data['ok'] == False:
                return await msg.edit(content=f":x: Error - {json_data['msg']}")
        
        desc = json_data['server']['motd']
        online = json_data['server']['online']
        playerCount = json_data['server']['playerCount']
        embed = discord.Embed(
            title = f"{arg} Server Info",
            description=f"Description: {desc}\nOnline: {online}\nPlayer Count: {playerCount}",
            color = discord.Color.dark_green()
        ).set_thumbnail(url="https://cdn.icon-icons.com/icons2/2699/PNG/512/minecraft_logo_icon_168974.png")
        await msg.delete()
        await ctx.send(embed=embed)

    @commands.command()
    async def hypixeluser(self,ctx,uname):
        self.data["hypixel"]["stats"] += 1
        self.data["hypixel"]["requestsPosted"] += 1
        self.data["totalRequestsPosted"] += 1
        msg = await ctx.send("Fetching Data from API...")
        name_link = f"https://api.hypixel.net/player?key={self.API_KEY}&name={uname}"
#        uuid_link = f"https://api.hypixel.net/player?key={self.API_KEY}&uuid={self.uuid_dashed}"
        resp = self.api_req(name_link)
            
        with open(f"user.json","w+") as f:
            json.dump(resp,f)

        await msg.delete()
        if resp["success"] == True:
            embed = discord.Embed(
                title=uname,
                description=resp["player"]["uuid"],
                color=discord.Color.dark_green()
            )
            embed.add_field(name="Hypixel ID",value=resp["player"]["_id"])
            embed.add_field(name="Hypixel Coins",value=resp["player"]["achievements"]["general_coins"])
            embed.add_field(name="Most recent Game",value=resp["player"]["mostRecentGameType"])

            await ctx.send(embed=embed)
        else:
            self.data["hypixel"]["rateLimits"] += 1
            await ctx.send(f":x: {resp['cause'].capitalize()}")
        print(resp["success"])

    @commands.command()
    async def skyblock(self,ctx,uname):
        msg = await ctx.send("Fetching Data from API...")
        r = requests.get(f"https://sky.shiiyu.moe/api/v2/profile/{uname}").json()
        with open(f"user.json","w+") as f:
            json.dump(r,f)

        self.data["hypixel"]["skyblock"] += 1
        self.data["hypixel"]["requestsPosted"] += 1
        self.data["totalRequestsPosted"] += 1
        embed = discord.Embed(url=f"http://sky.shiiyu.moe/api/v2/{uname}",title=f"{uname}",color=discord.Color.green())
        embed.add_field(name="Profile:",value=r["PROFILE_ID"]["cute_name"])
        



    @commands.command()
    async def bedwars(self,ctx,uname):

        self.data["hypixel"]["bedwars"] += 1
        self.data["hypixel"]["requestsPosted"] += 1
        self.data["totalRequestsPosted"] += 1
        msg = await ctx.send("Fetching Data from API...")
        name_link = f"https://api.hypixel.net/player?key={self.API_KEY}&name={uname}"
        #uuid_link = f"https://api.hypixel.net/player?key={API_KEY}&uuid={uuid_dashed}"
        resp = self.api_req(name_link)
            
        with open(f"user.json","w+") as f:
            json.dump(resp,f)
            
        await msg.delete()
        if resp["success"] == True:
            embed = discord.Embed(
                title=f"{uname}'s Bedwars Stats",
                description=f"{resp['player']['stats']['Bedwars']['games_played_bedwars_1']} Solo Rounds played so far",
                color=discord.Color.dark_green()
            )
            embed.add_field(name="Experience",value=resp['player']['stats']['Bedwars']['Experience'])
            embed.add_field(name="Deaths",value=resp['player']['stats']['Bedwars']['deaths_bedwars'])
            embed.add_field(name="Kills",value=resp['player']['stats']['Bedwars']['kills_bedwars'])
            embed.add_field(name="Rounds lost",value=resp['player']['stats']['Bedwars']['losses_bedwars'])

            await ctx.send(embed=embed)
        else:
            await ctx.send(f":x: {resp['cause'].capitalize()}")
        print(resp["success"])

    def api_req(self,call):
        """
        Send a GET request to an API
        """
        resp = requests.get(call)
        return resp.json()


def setup(bot):
    bot.add_cog(Hypixel(bot))