import json as JSON
import os
import discord
import random
from discord import ActivityType
from discord.ext.buttons import Paginator

class Pag(Paginator):
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except discord.HTTPException:
            pass


def clean_code(content):
    if(content.startswith("```") and content.endswith("```")):
        return "\n".join(content.split("\n")[1:][:-3])

    return content

async def open_account(user):
    users = await get_bank_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open('data/mainBank.json','w') as f:
        JSON.dump(users,f)
    return True

async def get_bank_data():
    with open('data/mainBank.json','r') as f:
        users = JSON.load(f)
    return users

def handle_custom(self, user):
        print(user.activities)
        a = [c for c in user.activities if c.type == ActivityType.custom]
        if not a:
            return None, ActivityType.custom
        a = a[0]
        c_status = None
        if not a.name:
            c_status = self.bot.get_emoji(a.emoji.id)
        if c_status:
            pass
        if a.name and a.emoji:
            c_status = f"{a.emoji} {a.name}"
        elif a.emoji and not c_status:
            c_status = f"{a.emoji}"
        elif a.name:
            c_status = a.name
        else:
            c_status = None
        return c_status, ActivityType.custom

def handle_playing(self, user):
        p_acts = [c for c in user.activities if c.type == ActivityType.playing]
        p_act = p_acts[0] if p_acts else None
        act = p_act.name if p_act and p_act.name else None
        return act, ActivityType.playing

def handle_streaming(self, user):
        s_acts = [c for c in user.activities if c.type == ActivityType.streaming]
        s_act = s_acts[0] if s_acts else None
        act = f"{s_act.name}{' | ' if s_act.game else ''}{s_act.game or ''}" if s_act and s_act.name and hasattr(s_act, "game") else s_act.name if s_act and s_act.name else None
        return act, ActivityType.streaming

def handle_listening(self, user):
        l_acts = [c for c in user.activities if c.type == ActivityType.listening]
        l_act = l_acts[0] if l_acts else None
        act = f"{l_act.title}{' | ' if l_act.artists[0] else ''}{l_act.artists[0] or ''}" if l_act and hasattr(l_act, "title") else l_act.name if l_act and l_act.name else None
        return act, ActivityType.listening

def handle_watching(self, user):
        w_acts = [c for c in user.activities if c.type == ActivityType.watching]
        w_act = w_acts[0] if w_acts else None
        act = w_act.name if w_act else None
        return act, ActivityType.watching


def convertTime(time):
    """ 
    Converts any entered time to seconds
    """
    pos = ["s","m","h","d","mth","y"]
    
    time_dict = {"s":1,"m":60,"h":3600,"d":3600*24,"mth":3600*24*30,"y":3600*24*30*365}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -1

    return val * time_dict[unit]

def get_short_link(link):
    shortener=pyshorteners.Shortener()

    x = shortener.tinyurl.short(link)
    return x

async def get_momma_jokes():
    with open("data/jokes.json","r+") as jokes:
        jokes = JSON.load(jokes)
    random_category = random.choice(list(jokes.keys()))
    insult = random.choice(list(jokes[random_category]))
    return insult

vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']

def last_replace(s, old, new):
    li = s.rsplit(old, 1)
    return new.join(li)

def text_to_owo(text):
    """ Converts your text to OwO """
    smileys = [';;w;;', '^w^', '>w<', 'UwU', '(・`ω\´・)', '(´・ω・\`)']

    text = text.replace('L', 'W').replace('l', 'w')
    text = text.replace('R', 'W').replace('r', 'w')

    text = last_replace(text, '!', '! {}'.format(random.choice(smileys)))
    text = last_replace(text, '?', '? owo')
    text = last_replace(text, '.', '. {}'.format(random.choice(smileys)))

    for v in vowels:
        if 'n{}'.format(v) in text:
            text = text.replace('n{}'.format(v), 'ny{}'.format(v))
        if 'N{}'.format(v) in text:
            text = text.replace('N{}'.format(v), 'N{}{}'.format('Y' if v.isupper() else 'y', v))

    newtext = text.replace('o!owo','')
    return newtext

class eco:
    @staticmethod
    async def developerCashAdd(amount:int):
        pass

class channel:
    @staticmethod
    async def setRateLimitPerUser(channel,s:int):
        await channel.edit(slowmode_delay=s)


