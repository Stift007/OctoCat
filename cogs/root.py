import os
import discord
from discord.ext import commands
import utils
import traceback
import shutil
from traceback import format_exception
import io
import textwrap
import contextlib


class Root(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.group()
    async def dev(self,ctx):
        pass

    @dev.command(name="commands")
    async def devcmds(self,ctx):
        embed = discord.Embed(title="Command List - Developers")
        print(self.bot.commands)
        for com in self.bot.commands:
            embed.add_field(name=com.name,value=com.usage)

        await ctx.send(embed=embed)

    @dev.command(name="eval",aliases=["exec"])
    @commands.is_owner()
    async def eval(self,ctx,*,code):
        code = utils.clean_code(code)

        local_variables = {
            "discord":discord,
            "commands":commands,
            "bot":self.bot,
            "ctx":ctx,
            "channel":ctx.channel,
            "author":ctx.author,
            "guild":ctx.guild,
            "message":ctx.message,
        }

        stdout = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f"async def func():\n{textwrap.indent(code,'    ')}",local_variables
                )

                obj = await local_variables["func"]()
                result = f"{stdout.getvalue()}\n--{obj}\n"
        except Exception as e:
            result = "".join(format_exception(e,e,e.__traceback__))

        pager = utils.Pag(
            timeout=100,
            use_defaults=True,
            entries=[result[i : i+2000] for i in range(0, len(result),2000)],
            prefix="```py\n",
            suffix="```"
        )

        await pager.start(ctx)

    @dev.command(name="deployto",aliases=["depl"])
    async def deployto(self,ctx,mode,*,file):
        if mode.lower() == "debug":
            shutil.move(f"{file}","debug")
        elif mode.lower() == "test":
            shutil.move(f"{file}","test")
        elif mode.lower() == "production":
            shutil.move(f"{file}","cogs")
        else:
            await ctx.send(f"{mode} isn't a valid Mode")

def setup(bot):
    bot.add_cog(Root(bot))


# config = {"token":configData[token],"prefix":"o!","categories": {"General":{"ping":"None","owo":"text","say":"*,args"},"Gambling":{"dice":"None","roll":"None","coin":"None"},"FUN/NSFW":{"insult":"Member","reddit":"subreddit"}}}