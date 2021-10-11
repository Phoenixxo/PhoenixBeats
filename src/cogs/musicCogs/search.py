import datetime
import discord
from discord.ext import commands
from music import Player


class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def search(self, ctx, *, song=None):
        if song is None:
            return await ctx.send("You forgot to include a song.")

        await ctx.send("Searching for song...")

        info = await Player.search_song(self, 5, song)

        embed = discord.Embed(
            title=f"Results for '{song}':",
            description="*You can use these exact URLs to play a song if the one you want isn't the first result.*\n",
            color=discord.Color.red(),
        )

        amount = 0
        i = 1

        for entry in info["entries"]:
            embed.description += f"{i}: [{entry['title']}]({entry['webpage_url']})\n"
            amount += 1
            i += 1

        embed.set_footer(text=f"Displaying the first {amount} results")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)
        print("[ ✓ ] Search command successfully executed!")
