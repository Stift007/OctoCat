import os,random
import discord
from discord.errors import DiscordException
from dhooks import Webhook
import requests
import abc
import decimal

import dis
from discord import user
from discord.player import FFmpegPCMAudio
# from discord_buttons_plugin import *
import stocksloader
from discord.ext import commands,tasks
import youtube_dl
from PIL import Image,ImageFont,ImageDraw,ImageFilter
from io import BytesIO, TextIOWrapper
import datetime

from discord_components import DiscordComponents,Button,ButtonStyle, InteractionEventType,Interaction
import aiofiles
import asyncio
import json

##### Helper Functions #####

class OctoCat(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        # self.ipc = ipc.Server(self,secret_key="d.")

    async def on_ready(self):
        await set_stocks.start()
        print("OctoCat is ready")
        print(self.shard_count)
    
    async def on_ipc_ready(self):
        Hook = Webhook("https://discord.com/api/webhooks/859019870619566081/FChbx0-7rmXgYH4VNbXKf30mDF91cxOqTVqmLdyPKn03Ip3qumAr-73jTToBHxxfNqoI")
        print("IPC is active")
        em = discord.Embed(desciption="IPC is active")
        Hook.send(embed=em)

    async def on_ipc_error(self,endpoint,error):
        print(endpoint+" raised "+error)

def get_users():
    users = 0
    for i in bot.guilds:
            users += len(i.members)
    return users

def get_prefix(bot,message):
    with open("data/config.json","r") as f:
        prefixes = json.load(f)
    
    return prefixes[str(message.guild.id)]["prefix"]

async def get_bank_data():
    with open('data/mainBank.json','r') as f:
        users = json.load(f)
    return users

async def update_bank(user,change=0,mode="wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change


    with open('data/mainBank.json','w') as f:
        json.dump(users,f)
    
    bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
    return bal

async def open_account(user):
    users = await get_bank_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0
        users[str(user.id)]["job"] = None
        users[str(user.id)]["inventory"] = []

    with open('data/mainBank.json','w') as f:
        json.dump(users,f)
    return True

##### Set up Youtube Downloader

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

_queue = []
_loop = False
now_playing = ''

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

##### Build the Bot

intents = discord.Intents.all()

intents.members = True

def get_prefix(client,message):
	
	with open("data/config.json","r") as f:
		prefixes = json.load(f)
	return prefixes[str(message.guild.id)]["prefix"]

#bot = OctoCat(command_prefix=get_prefix,intents = intents)
bot = OctoCat(command_prefix=get_prefix,intents = intents,case_insensitive=True)
bot.remove_command('help')
bot.warnings = {}
guild_ids = []
for guild in bot.guilds:
    guild_ids.append(guild.id)

# Slash Commands

optionsGAN = [
    {
        "name":"start",
        "description":"The Starting Limit of the Guess",
        "required":False,
        "type":4
    },
    {
        "name":"stop",
        "description":"The stopping Limit of the Guess",
        "required":False,
        "type":4
    }
]

optionsWanted = [
    {
        "name":"user",
        "description":"The wanted Member",
        "required":False,
        "type":6
    }
]

globalPlayer = None
@bot.event
async def on_message(message):
    if message.content.startswith(bot.user.mention):
        await message.channel.send(f"Bot's Prefix is {get_prefix(bot,message)}")

    await bot.process_commands(message)

# @bot.ipc.route()
# async def get_guild_count(data):
#     return len(bot.guilds)

# @bot.ipc.route()
# async def sendmsg(data):
#     await bot.get_guild(data.guildid).get_channel(data.channel_id).send(data.msg)

# @bot.ipc.route()
# async def nickMember(data):
#     member:discord.Member = data.member

#     await member.edit(nick=data.nick)

@bot.event
async def on_guild_join(guild):
    bot.warnings[guild.id] = {}
    em = discord.Embed(title="Heyho! Thanks for adding OctoCat to your Server!",color=discord.Color.blue())
    em.description = "Don't worry, this is the last time you'll see this. This Project is\nand will always be free and open-source,\nIf you want to show your Support, please consider recommending\nthis Bot to your Friends, leaving a Star on GitHub\nor joining the Discord"
    em.add_field(name="Getting started",value="To get started with the Bot, run `o!help`")
    found = False
    for channel in guild.text_channels:
        try:
            await channel.send(embed=em,components=[
                Button(style=ButtonStyle.URL,label="Invite OctoCat",url="https://dis.gd/threads"),
                Button(style=ButtonStyle.URL,label="GitHub Repo",url="https://github.com/Stift007/OctoCat"),
                Button(style=ButtonStyle.URL,label="Support",url=f"https://top.gg/{bot.user.id}/invite")
            ])
            found = True
            break
        except:
            continue


@bot.command()
@commands.has_permissions(kick_members=True)
async def warnings(ctx:commands.Context,member:discord.Member=None):
    if not member:
        return await ctx.send("Please provide a Member")
    
    embed = discord.Embed(title=f"Displaying Warnings for {member.name}",description="",color=discord.Color.red())
    try:
        i = 1
        for admin_id,reason in bot.warnings[ctx.guild.id][member.id][1]:
            admin = ctx.guild.get_member(admin_id)
            embed.description += f"**Warning #{i}** Given by {admin.name} for *'{reason}'*"
            i += 1
        await ctx.send(embed=embed)
    except KeyError:
        await ctx.send("This User has no Warnings yet!")

@bot.command()
async def button(ctx):
    await ctx.send(
        "This is a Button!",
        components=[
            Button(style=ButtonStyle.red,label="This is a Button"),
            Button(style=ButtonStyle.green,label="And this is another button"),
            Button(style=ButtonStyle.URL,label="VOTE",url="http://dis.gd/threads"),
            Button(style=ButtonStyle.red,label="This is a Button",disabled=True)
        ]
    )

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
        embed=discord.Embed(title="**Slow it down Bro**",description=f"You're on cooldown! Try again in {error.retry_after:.2f}s.")
        await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx:commands.Context,member:discord.Member=None,*,reason=None):
    if not member:
        return await ctx.send("Please provide a Member")
    if not reason:
        return await ctx.send("Please provide a Reason")
    try:
        first_warn = False
        bot.warnings[ctx.guild.id][member.id][0] += 1
        bot.warnings[ctx.guild.id][member.id][1].append((ctx.author.id,reason))
    except KeyError:
        first_warn = True
        bot.warnings[ctx.guild.id][member.id] = [1, [(ctx.author.id, reason)]]
    count = bot.warnings[ctx.guild.id][member.id][0]

    with open("data/{0.id}.txt".format(ctx.guild),"a") as f:
        f.write(f"{member.id} {ctx.author.id} {reason}\n")

    await ctx.send(f"{member.mention} now has {count} {'warning' if first_warn else 'warnings'}")


@bot.event
async def on_ready():
    for guild in bot.guilds:
        print(f"Opening {guild.name}...")
        await open_config(guild)
        print(f"Opened {guild.name}!")
    print("All Guilds Were opened!")
    await chpr.start()
    for guild in bot.guilds:
        bot.warnings[guild.id] = {}
        if os.path.exists(f"data/{guild.id}.txt"):
                pass
        else:
            with open(f"data/{guild.id}.txt","a") as f:
                f.write("")

        

    for guild in bot.guilds:
        with open(f"data/{guild.id}.txt","r") as f:
            lines = f.readlines()

            for line in lines:
                data = line.split(" ")
                member_id = int(data[0])
                admin_id  = int(data[1])
                reason    = " ".join(data[2:]).strip("\n")

                try:
                    bot.warnings[guild.id][member_id][0] += 1
                    bot.warnings[guild.id][member_id][1].append((admin_id,reason))
                except KeyError:
                    bot.warnings[guild.id][member_id] = [1, [(admin_id,reason)]]
    
        


for filename in os.listdir('cogs'):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f'cogs.{filename[:-3]}')

##### Commands

# @bot.command()
# async def clyde(ctx,*,text="I am Clyde"):
#     img = Image.open("PIL_Lib/clyde.jpg")

#     draw = ImageDraw.Draw(img)
#     font = ImageFont.truetype("PIL_Lib/unisansbold.ttf",14)

#     draw.text((60,50),text,(255,255,255),font=font)
#     img.save("clyde.jpg")
#     await ctx.send(file=discord.File("clyde.jpg"))

# @bot.command()
# async def delete(ctx,member:discord.Member=None):
#     if not member:member=ctx.author
#     wanted_img = Image.open("PIL_Lib/memedel.jpg")

#     asset = member.avatar_url_as(size=128)
#     data = BytesIO(await asset.read())
#     pfp = Image.open(data)

#     pfp = pfp.resize((336,339))#336,339

#     wanted_img.paste(pfp, (207,285))

#     wanted_img.save("profile.jpg")

#     await ctx.send(file=discord.File("profile.jpg"))

# @bot.command()
# async def rip(ctx,user:discord.Member=None):
#     if not user:
#         user = ctx.author

#     rip = Image.open("PIL_Lib/rip.jpg")

#     asset = user.avatar_url_as(size=128)
#     data = BytesIO(await asset.read())
#     pfp = Image.open(data)

#     pfp = pfp.resize((200,190))

#     rip.paste(pfp, (336,301))

#     rip.save('prip.jpg')

#     await ctx.send(file=discord.File('prip.jpg'))

@bot.command()
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send('You are not connected to any Voice Channel')
        return
    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()

@bot.command()
async def loop(ctx):
    global _loop

    if _loop:
        await ctx.send('Loop Mode is now `Disabled`')
        _loop = False

    else:
        await ctx.send('Loop Mode is now `Enabled`')
        _loop = True


@bot.command()
async def skip(ctx):
    global _queue
    
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.stop()
    player = await YTDLSource.from_url(_queue[0],loop=bot.loop)
    voice_channel.play(player,after=lambda e: print("Player Error %s" % e) if e else None)

@bot.command(description="Stream Radio in your Voice Channel")
async def radio(ctx:commands.Context,url='http://stream.radioparadise.com/rock-128'):
    channel = ctx.author.voice.channel
    global player
    try:
        player = await channel.connect()
    except Exception as ex:
        pass
    await ctx.message.reply(content=f"Now Streaming {url}...")
    player.play(FFmpegPCMAudio(url))

@bot.command()
async def play(ctx,*,video=None):
    global _queue
    global now_playing

    channel = ctx.author.voice.channel
    global player
    try:
        player = await channel.connect()
    except Exception as ex:
        pass
    await ctx.send(f":thumbsup: Joined `{channel.name}` and bound to `#{ctx.channel.name}`")
    
    
    
    async with ctx.typing():
        try:
            server = ctx.message.guild
            
            if not video:
                video = _queue[0]
            voice_channel = server.voice_client
            await ctx.send(f":mag_right: Searching `{video}`...")
            
           
            player = await YTDLSource.from_url(video,loop=bot.loop,stream=True)
            await ctx.send(f"Playing :notes:`{player.title or video}`")
            voice_channel.play(player,after=lambda e: print("Player Error %s" % e) if e else None)
            
            if not _loop:        
                del(_queue[0])

        except Exception as e:
            print(e)
    voice_channel = server.voice_client

@bot.command()
async def nowplaying(ctx):
    volume = player.volume
    title = player.title
    url = player.url
    original = player.original

    embed = discord.Embed(title=title,description=url)
    embed.add_field(name="Original",value=original)
    embed.add_field(name="Volume", value=volume, inline=True)
    await ctx.send(embed=embed)

@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.pause()

@bot.command()
async def stop(ctx):
    global _queue
    
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.stop()

@bot.command()
async def resume(ctx):
    global _queue
    
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.resume()

@bot.command()
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()

@bot.command()
async def see_queue(ctx):
    embed = discord.Embed(title=f"Music Queue",description=f"The Music Queue is {len(_queue)} Items long.")
    if len(_queue) >0:
        embed.add_field(name="Titles/Songs",value= ", ".join(_queue))
    else:
        embed.add_field(name="Titles/Songs",value="There are no Queued Songs :(")  
    if now_playing:

        embed.add_field(name="Now Playing",value=now_playing)
    else:
        embed.add_field(name="Now Playing",value="There is no Song Playing")

    await ctx.send(embed=embed)
    

@bot.command()
async def queue(ctx,*,url):
    global _queue

    _queue.append(url)
    await ctx.send(f'`{url}` has been queued!')

@bot.command()
async def unqueue(ctx,number:int):
    if number > 0:
        number -= 1
    global _queue

    try:
        del(_queue[int(number-1)])
        await ctx.send(f'Your Queue has been changed to `{_queue}`!')

    except:
        await ctx.send(f'Cannot Access the {number}. queued Item - The Queue is either **empty** or the **Index is out of Range**')

def get_stocks_value():
    return 20

shop = {
    "1":{
        "topic":"Boostings",
        "items":[
            {"premium":{
                "name":"premium",
                "cost":100000000000000,
                "description":"Activate Premium on this Server"
            }},
            {"priority_queue":{
                "name":"priority_queue",
                "cost":100000000000,
                "description":"Support Requests are being processed faster"
            }
            }
        ]
    },"2":{
        "topic":"OctoStocks™",
        "items":[
            {"stocks":{
                "name":"stocks",
                "cost":get_stocks_value(),
                "description":"Buy some Stocks"
            }
            }
        ]
    },
}

# @bot.group(invoke_without_command = True)
# async def shop(ctx):
#     pass

# @shop.command(name="2")
# async def _2(ctx):
#     embed = discord.Embed(title="Shop Page 2")
#     embed.add_field(name="Stocks",value=f'`{get_prefix(bot,ctx)}buy stocks`')
    

# @bot.command()
# async def buy(ctx,item):
#     if item == "stocks":
#         await update_inventory(ctx.author,"stocks",1)
#         await ctx.send(f'You bought 1 Stock')

stocks = stocksloader.StockRiser(100,-100)

@bot.command(aliases=["trends"])
async def trend(ctx):
    embed = discord.Embed(title=f"OctoStocks Trends")
    si = stocks.sourceValue
    cv = stocks.currentValue
    embed.add_field(name="Currently",value=cv)
    embed.add_field(name="Yesterday",value=si)
    await ctx.send(embed=embed)

@tasks.loop(hours=24)
async def set_stocks():
    stocks.trends()

@bot.command(aliases=["dep"])
async def deposit(ctx,amount = None):
    await open_account(ctx.author)
    if not amount:
        await ctx.send("Please enter the Amount you want to deposit.")
        return
    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount >bal[0]:
        await ctx.send("You don't have that much Money in your Wallet.")
        return
    if amount <0:
        await ctx.send("Can't deposit A Negative Number!")
        return
        
    try:
        await update_bank(ctx.author,-1*amount)
        await update_bank(ctx.author,amount,mode="bank")
        await ctx.send(f"You deposited {amount} Coins onto your Bank Account!")
    except Exception as e:
        embed = discord.Embed(title="Whoops!",description="This did Not Work.")
        embed.add_field(name="Error Details:",value=e,inline=False)
        embed.add_field(name="Know how to fix?",value="Tell us on the Support Server with !debug <How to Fix It> - [here](https://tinyurl.com/octosupport)",inline=False)
        await ctx.send(embed=embed)


@bot.command(aliases=["don","donate"])
async def send(ctx,member : discord.Member,amount = None):
    await open_account(ctx.author)
    await open_account(member)
    if not amount:
        await ctx.send("Please enter the Amount you want to deposit.")
        return
    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount >bal[1]:
        await ctx.send("You don't have that much Money in your Bank.")
        return
    if amount <0:
        await ctx.send("Can't deposit A Negative Number!")
        return
        
    try:
        await update_bank(ctx.author,-1*amount,mode="bank")
        await update_bank(member,amount,mode="bank")
        await ctx.send(f"You successfully Transferred {amount} Coins from your Bank Account to {member.mention}'s Bank Account!")
        await member.send(f"{ctx.author.name} just sent {amount} Coins to your Bank Account!")
    except Exception as e:
        embed = discord.Embed(title="Whoops!",description="This did Not Work.")
        embed.add_field(name="Error Details:",value=e,inline=False)
        embed.add_field(name="Know how to fix?",value="Tell us on the Support Server with !debug <How to Fix It> - [here](https://tinyurl.com/octosupport)",inline=False)
        await ctx.send(embed=embed)

@bot.command()
async def lyrics(ctx,*,song=None):
    API_BASE_URL ="https://some-random-api.ml"
    if not song:
        song = player.title
    r = requests.get(API_BASE_URL+"/lyrics",data={"title":song}).json()
    embed = discord.Embed(title=r["title"])
    embed.set_author(name=r["author"])
    embed.description = r["lyrics"]
    await ctx.send(embed=embed)
    

@bot.command()
async def rob(ctx,member : discord.Member=None):
    if not member:
        return await ctx.send("Please specify a Member to rob.")
    await open_account(ctx.author)
    await open_account(member)
    
    bal = await update_bank(member)


    if bal[0]<100:
        await ctx.send("It's not worth the effort.")
        return
        
    try:
        earnings = random.randrange(0,bal[0])
        await update_bank(ctx.author,earnings)
        await update_bank(member,-1*earnings)
        if earnings > 0:
            await ctx.send(f"You robbed {earnings} Coins from {member.mention} and got away with it!")
        else:    
            await ctx.send(f"You tried to rob {member.mention}, but they noticed you and called the Police. You got away with it, but didn't earn a Penny.")
        
    except Exception as e:
        embed = discord.Embed(title="Whoops!",description="This did Not Work.")
        embed.add_field(name="Error Details:",value=e,inline=False)
        embed.add_field(name="Know how to fix?",value="Tell us on the Support Server with !debug <How to Fix It> - [here](https://tinyurl.com/octosupport)",inline=False)
        await ctx.send(embed=embed)




async def open_config(guild):
    with open("data/config.json","r+") as f:
        config = json.load(f)
    
    if str(guild.id) in config:
        return False
    
    config[str(guild.id)] = {}
    config[str(guild.id)]["automod"] = {}
    config[str(guild.id)]["automod"]["banned_words"] = [
            "fuck",
            "nigg",
            "fuk",
            "cunt",
            "cnut",
            "bitch",
            "dick",
            "d1ck",
            "pussy",
            "asshole",
            "b1tch",
            "b!tch",
            "cock",
            "c0ck"]
    config[str(guild.id)]["MemberJoinEvent"] = {}
    config[str(guild.id)]["MemberJoinEvent"]["message"] = "NONE"
    config[str(guild.id)]["MemberJoinEvent"]["role"] = "NONE"
    config[str(guild.id)]["MemberLeaveEvent"] = {}
    config[str(guild.id)]["MemberLeaveEvent"]["message"] = "NONE"
    config[str(guild.id)]["nickname"] = "OctoCat"
    config[str(guild.id)]["prefix"] = "o!"
    with open("data/config.json","w+") as f:
        json.dump(config,f)

JOBS = {
    "redditor":{
        "INCOME":1000
    },"babysitter":{
        "INCOME":100
    },"octocat dev":{
        "INCOME":100000
    },"discord mod":{
        "INCOME":5000
    },"youtuber":{
        "INCOME":2500
    },
}

@bot.command()
async def job(ctx,*,_job=None):
    await open_account(ctx.author)
    if not _job:
        embed = discord.Embed(title="Job List")
        embed.description = f"Use `{get_prefix(bot,ctx.message)}job [JOBNAME]` to sign up for a job"
        embed.add_field(name="Redditor",value="Income: `1000`\nDifficulty: 2/10",inline=False)
        embed.add_field(name="Babysitter",value="Income: `100`\nDifficulty: 1/10",inline=False)
        embed.add_field(name="Discord Mod",value="Income: `5000`\nDifficulty: 5/10",inline=False)
        embed.add_field(name="YouTuber",value="Income: `2500`\nDifficulty: 3/10",inline=False)
        await ctx.send(embed=embed)
    else:
        if _job.lower() in ["redditor","youtuber","babysitter","jobless","octocat dev","discord mod"]:
            job_income = JOBS[_job.lower()]["INCOME"]
                        
            with open("data/assignedJobList.json") as f:
                assignedJobs = json.load(f)

            assignedJobs[str(ctx.author.id)]=_job.lower()
            
            await ctx.reply(f"Done! You are now a {_job.capitalize()}!")

            with open("data/assignedJobList.json","w+") as f:
                assignedJobs = json.dump(assignedJobs,f)


@bot.command()
@commands.cooldown(1,86400,commands.BucketType.user)
async def work(ctx):
    await open_account(ctx.author)
    with open("data/assignedJobList.json") as f:
        assignedJobs = json.load(f)

        try:
            _job = assignedJobs[str(ctx.author.id)]
            if _job == "redditor":
                redditorSentences = ["edit: gold? Thank you, kind stranger","Username checks out","Take your upvote and get out."]
                sentence = random.choice(redditorSentences)
                await ctx.send(f"Retype this sentence:\n`{sentence}`")
                try:
                    msg = await bot.wait_for('message', timeout=15.0)
                    if msg.content == sentence:
                        income = JOBS[_job.lower()]["INCOME"]
                        await update_bank(ctx.author,income,"bank")
                        await ctx.send(f"Well done, {ctx.author.mention}! You get the full {income} coins!")
                    else:
                        income = JOBS[_job.lower()]["INCOME"] - random.randint(500,800)
                        await ctx.send(f"Terrible work, {ctx.author.mention}. You only get {income} coins for this shift.")
                        await update_bank(ctx.author,income,"bank")

                except asyncio.TimeoutError:
                    income = JOBS[_job.lower()]["INCOME"] - random.randint(500,800)
                    await ctx.send(f"Terrible work, {ctx.author.mention}. You only get {income} coins for this shift.")
                    await update_bank(ctx.author,income,"bank")

            if _job == "youtuber":
                redditorSentences = ["don't forget to smash that like button","also, only a small percentage of people watching my videos are actually subscribed","before we continue, I'd like to thank our sponsor RAID shadow legends"]
                sentence = random.choice(redditorSentences)
                await ctx.send(f"Retype this sentence:\n`{sentence}`")
                try:
                    msg = await bot.wait_for('message', timeout=30.0)
                    if msg.content == sentence:
                        income = JOBS[_job.lower()]["INCOME"]
                        await update_bank(ctx.author,income,"bank")
                        await ctx.send(f"Well done, {ctx.author.mention}! You get the full {income} coins!")
                    else:
                        income = JOBS[_job.lower()]["INCOME"] - random.randint(500,800)
                        await ctx.send(f"Terrible work, {ctx.author.mention}. You only get {income} coins for this shift.")
                        await update_bank(ctx.author,income,"bank")

                except asyncio.TimeoutError:
                    income = JOBS[_job.lower()]["INCOME"] - random.randint(500,800)
                    await ctx.send(f"Terrible work, {ctx.author.mention}. You only get {income} coins for this shift.")
                    await update_bank(ctx.author,income,"bank")

            if _job == "babysitter":
                redditorSentences = ["sssshh... bedtime","it's bedtime!"]
                sentence = random.choice(redditorSentences)
                await ctx.send(f"Retype this sentence:\n`{sentence}`")
                try:
                    msg = await bot.wait_for('message', timeout=30.0)
                    if msg.content == sentence:
                        income = JOBS[_job.lower()]["INCOME"]
                        await update_bank(ctx.author,income,"bank")
                        await ctx.send(f"Well done, {ctx.author.mention}! You get the full {income} coins!")
                    else:
                        income = JOBS[_job.lower()]["INCOME"] - random.randint(500,800)
                        await ctx.send(f"Terrible work, {ctx.author.mention}. You only get {income} coins for this shift.")
                        await update_bank(ctx.author,income,"bank")

                except asyncio.TimeoutError:
                    income = JOBS[_job.lower()]["INCOME"] - random.randint(500,800)
                    await ctx.send(f"Terrible work, {ctx.author.mention}. You only get {income} coins for this shift.")
                    await update_bank(ctx.author,income,"bank")

            if _job == "discord mod":
                redditorSentences = ["guys, don't post memes into #general","Wanna get banned?","are you a female?","please read the rules"]
                sentence = random.choice(redditorSentences)
                await ctx.send(f"Retype this sentence:\n`{sentence}`")
                try:
                    msg = await bot.wait_for('message', timeout=30.0)
                    if msg.content == sentence:
                        income = JOBS[_job.lower()]["INCOME"]
                        await update_bank(ctx.author,income,"bank")
                        await ctx.send(f"Well done, {ctx.author.mention}! You get the full {income} coins!")
                    else:
                        income = JOBS[_job.lower()]["INCOME"] - random.randint(500,800)
                        await ctx.send(f"Terrible work, {ctx.author.mention}. You only get {income} coins for this shift.")
                        await update_bank(ctx.author,income,"bank")

                except asyncio.TimeoutError:
                    income = JOBS[_job.lower()]["INCOME"] - random.randint(500,800)
                    await ctx.send(f"Terrible work, {ctx.author.mention}. You only get {income} coins for this shift.")
                    await update_bank(ctx.author,income,"bank")

        except KeyError:
            await ctx.send("You haven't signed up for a job yet. Use `o!job` to see all avalable Jobs")
    


@bot.group()
async def config(ctx):
    pass

@config.command()
@commands.has_permissions(manage_nicknames=True)
async def nickname(ctx,*,nick="OctoCat"):
    try:
        with open("data/config.json","r") as f:
            config = json.load(f)
            config[str(ctx.guild.id)]["nickname"] = nick
        await ctx.send(f"Nicked me to {nick}!")
    except Exception as ex:
        await ctx.send(ex)
@bot.command()
async def bag(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    em = discord.Embed(title = "Bag")
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name = name, value = amount)    

    await ctx.send(embed = em)   

@bot.event
async def on_voice_state_update(member,before,after):
    if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                voice_client = member.guild.voice_client
                await voice_client.disconnect()

@bot.command()
@commands.cooldown(1,150,commands.BucketType.user)
async def slots(ctx,amount = None):
    await open_account(ctx.author)
    if not amount:
        await ctx.send("Please enter the Amount you want to deposit.")
        return
    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount >bal[0]:
        await ctx.send("You don't have that much Money in your Bank.")
        return
    if amount <0:
        await ctx.send("Can't deposit A Negative Number!")
        return

    finalList = []
    for i in range(3):
        a = random.choice(["X","0","Q","P"])

        finalList.append(a)

    await ctx.send(", ".join(finalList))
    if finalList[0] == finalList[1] or finalList[0] == finalList[2] or finalList[1] == finalList[2]:
        await update_bank(ctx.author,2*amount)
        await ctx.send(f"Congrats! You just won {2*amount} Coins!")
    else:
        await update_bank(ctx.author,-1*amount)
        await ctx.send(f"You lost {amount} Coins...")
    
        
@bot.command() # Normal message wait_for
async def test(ctx):
    await ctx.send("Do you want me to say hi? `(y/n)`")
    msg = await bot.wait_for('message', timeout=15.0)
    if msg.content == 'y':
        await ctx.send("hi")
    else:
        await ctx.send("ok i wont")

@bot.command()
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)
    if not amount:
        await ctx.send("Please enter the Amount you want to withdraw.")
        return
    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount >bal[1]:
        await ctx.send("You don't have that much Money in your Bank Account.")
        return
    if amount <0:
        await ctx.send("Can't withdraw A Negative Number!")
        return
        
    try:
        await update_bank(ctx.author,amount)
        await update_bank(ctx.author,-1*amount,mode="bank")
        await ctx.send(f"You withdrew {amount} Coins from your Bank Account!")
    except Exception as e:
        embed = discord.Embed()
        embed.add_field(name="An Error Occured",value=e,inline=False)
        await ctx.send(embed=embed)

@bot.command()
async def balance(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()
    user = ctx.author

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt   = users[str(user.id)]["bank"]

    embed = discord.Embed(title=f"{ctx.author.name}'s Balance",color=discord.Color.dark_gold())
    embed.add_field(name="Wallet Balance",value=wallet_amt)
    embed.add_field(name="Bank Balance",value=bank_amt)
    await ctx.send(embed=embed)



@bot.command()
@commands.cooldown(1,10,commands.BucketType.user)
async def search(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()
    user = ctx.author

    chances = random.randint(1,30)
    if chances == 1:
        await ctx.send("You found some stale bread!\n...Yay?")
        return
    elif chances ==2:
        await ctx.send("You found some soggy garlic bread!\n**YAY! Gross!**")
        return
    earnings = random.randrange(100)
    await ctx.send(f"{earnings} Coins were found!")
    users[str(user.id)]["wallet"] += earnings
    with open('data/mainBank.json','w') as f:
        json.dump(users,f)

@bot.command()
@commands.is_owner()
async def addmoney(ctx,amt:int=None):
    await open_account(ctx.author)

    users = await get_bank_data()
    user = ctx.author    
    users[str(user.id)]["wallet"] += amt
    await ctx.send(f"Increased your Balance by {amt}")
    with open('data/mainBank.json','w') as f:
        json.dump(users,f)


@bot.command(aliases=["leads","lb"])
async def leaderboard(ctx,top = 3):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"]+users[user]["bank"] 
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total,reverse=True)

    embed = discord.Embed(title=f"Top {top} richest People",description="This is decided on the basis of raw money in the bank and wallet",color = discord.Color(0xfa43ee))
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = bot.get_user(id_)
        name = member.name
        embed.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
        if index == top:
            break
        else:
            index += 1
    
    await ctx.send(embed=embed)



DiscordComponents(bot)


@bot.command()
async def help(ctx, commandSent=None):
    if commandSent != None:

        for command in bot.commands:
            if commandSent.lower() == command.name.lower():

                paramString = ""

                for param in command.clean_params:
                    paramString += param + ", "

                paramString = paramString[:-2]

                if len(command.clean_params) == 0:
                    paramString = "None"
                    
                embed=discord.Embed(title=f"HELP - {command.name}", description=command.description)
                embed.add_field(name="Parameters", value=paramString)
                await ctx.message.delete()
                await ctx.author.send(embed=embed)
    else:
        embed = discord.Embed(title=f"Help - {ctx.guild.name}",description=f"These are the available commands for OctoCat")
        embed.add_field(name="General", value="`ping ` `owo` `say`",inline=False)
        embed.add_field(name="Gambling", value="`dice ` `roll` `coin`",inline=False)
        embed.add_field(name="Fun", value="`insult` `reddit` `avatarfusion` `aki` `hack`",inline=False)
        embed.add_field(name="Images", value="`cat` `dog` `fox` `meme`",inline=False)
        embed.add_field(name="Utilities", value="`help` `set_modlog_channel` `serverinfo` `whois` `userinfo`",inline=False)
        embed.add_field(name="Moderation", value="`kick` `rero` `ban` `unban` `mute` ",inline=False)
        embed.add_field(name="Music", value="`play` `stop` `queue` `unqueue` `see_queue` `join` `leave` `loop`",inline=False)
        embed.add_field(name="Economy", value="`search` `balance` `withdraw` `deposit` `rob` `send` `leads`",inline=False)
        embed.add_field(name="Misc", value="`servers` `m8ball` `chat` `vote`",inline=False)
        embed.add_field(name="APIs", value="`wiki` `pypi`",inline=False)
        embed.add_field(name="Anime", value="`animeme` `waifu` `anime` `character` `aninews`",inline=False)
        embed.add_field(name="Social", value="  `hug` `kiss` `pat` `slap` `cuddle` `wink` `kill`",inline=False)
        if ctx.channel.is_nsfw():
            embed.add_field(name="Anime/NSFW", value="`boobs` `hentai` `blowjob` `gif`",inline=False)
        
        await ctx.send(embed=embed)

        

@bot.command()
async def vote(ctx):
    embed = discord.Embed(title=f"Vote for OctoCat!",color=ctx.author.color)
    embed.add_field(name="Vote!",value=f"""**Top.gg isn't related to OctoCat at all and there are no options for the bot owners to disable the ads.**
                                            You may vote right now!
                                            [Vote](https://top.gg/bot/820308868705812491/vote)
                                            """)
    await ctx.send(embed=embed)

        

@tasks.loop(seconds=10)
async def chpr():
    #await bot.change_presence(activity=discord.Activity(name=f"{75-len(bot.guilds)} Servers until Verification! | o!help",type=5))
    
    await bot.change_presence(activity=discord.Streaming(name=f"{bot.shard_count} Shards | {len(bot.guilds)} Guilds | {get_users()} Members",url="http://45.85.219.90:4000"))
    movies = ["tinyurl.com/octosupport | o!help","Over the Mods | o!help", f"{get_users()} People and {len(bot.guilds)} People | o!help"]
    presences = [f"On {len(bot.guilds)} Servers | o!help",f"With {get_users()} People | o!help","With Discord's Bot API | o!help","discord.ly/octocat | o!help"]

    """for i in presences:
        await bot.change_presence(activity=discord.Game(name=i))
        await asyncio.sleep(10)

    for j in movies:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=j))
        await asyncio.sleep(10)"""

@bot.command()
@commands.has_permissions(manage_guild=True)
async def prefix(ctx,_pre="o!"):
	with open("data/config.json","r") as f:
            prefixes = json.load(f)
            prefixes[str(ctx.guild.id)]["prefix"] = _pre
            with open("data/config.json","w+") as f:
                    json.dump(prefixes,f)

            await ctx.send(f"Prefix updated to {_pre}")
from dotenv import load_dotenv
from os import getenv

load_dotenv()

TOKEN=getenv("TOKEN")

# bot.ipc.start()
# ODIwMzA4ODY4NzA1ODEyNDkx.YEzSKg.E40fvmI_bKbjOPRMwBKYVLCSRUE

bot.run("ODIwMzA4ODY4NzA1ODEyNDkx.YEzSKg.uMTT5YCdT-rldeghSeK64NHFJpY")
