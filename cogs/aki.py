from discord.ext import commands
import akinator as ak
import discord

class Test(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(aliases=["aki"])
    async def akinator(self,ctx):
        await ctx.send("Akinator is here to guess!")
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["y", "n","p","b"]
        try:
            aki = ak.Akinator()
            q = aki.start_game()
            while aki.progression <= 80:
                await ctx.send(q)
                await ctx.send("Your answer:(y/n/p/b)")
                msg = await self.bot.wait_for("message", check=check)
                if msg.content.lower() == "b":
                    try:
                        q=aki.back()
                    except ak.CantGoBackAnyFurther:
                        await ctx.send("Cannot go back any further!")
                        continue
                else:
                    try:
                        q = aki.answer(msg.content.lower())
                    except ak.InvalidAnswerError as e:
                        await ctx.send(e)
                        continue
            aki.win()

            embed = discord.Embed(title=f"Is it {aki.first_guess['name']}?",description=aki.first_guess['description'])
            embed.set_image(url=aki.first_guess['absolute_picture_path'])
            embed.set_footer(text="Was I correct? Y/N?")
            await ctx.send(embed=embed)
            correct = await self.bot.wait_for("message", check=check)
            if correct.content.lower() == "y":
                await ctx.send("Yay! Guessed right one more Time!\n")
            else:
                await ctx.send("Oof\n")
        except Exception as e:
            await ctx.send(e)

    

def setup(bot):
    bot.add_cog(Test(bot))


# config = {"token":configData[token],"prefix":"o!","categories": {"General":{"ping":"None","owo":"text","say":"*,args"},"Gambling":{"dice":"None","roll":"None","coin":"None"},"FUN/NSFW":{"insult":"Member","reddit":"subreddit"}}}