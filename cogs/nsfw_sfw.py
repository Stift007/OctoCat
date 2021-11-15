from discord.ext import commands
import requests
from datetime import datetime
import discord


class nsfwimages(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.attachments:
            for a in message.attachments:
                r = requests.post(
                        "https://api.deepai.org/api/nsfw-detector",
                        data={
                            'image':a
                            },
                        headers={
                            'api-key':'8a3b6bb2-0934-468e-aad7-7e8bd9ce2d8c'
                            }).json()
                print(r)
                if r["output"]["detections"]:
                    if message.channel.is_nsfw():
                        pass
                    else:
                        await message.delete()
                        
                        embed = discord.Embed(title="Message Deleted!", description=message.content, color=0xFF0000, timestamp=datetime.utcnow(),)
                        embed.add_field(name="Reason",value="NSFW Image (In Non-NSFW Channel)")
                        embed.add_field(name="False Positive?",value="[[Report False Positives]](http://github.com/Stift007/octocat/issues)")
                        await message.channel.send(embed=embed)
                        

    

def setup(bot):
    bot.add_cog(nsfwimages(bot))


# config = {"token":configData[token],"prefix":"o!","categories": {"General":{"ping":"None","owo":"text","say":"*,args"},"Gambling":{"dice":"None","roll":"None","coin":"None"},"FUN/NSFW":{"insult":"Member","reddit":"subreddit"}}}
