import discord
from discord.ext import commands
from utils import Utils


class Queue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def queue(self, ctx):  # Display the current queue for the guild
        if len(Utils.song_queue[ctx.guild.id]) == 0:
            return await ctx.send("There are currently no songs in the queue.")

        song = list(Utils.song_queue[ctx.guild.id])
        info = Utils.search_song(len(self.song_queue[ctx.guild.id]), song)

        embed = discord.Embed(
            title="Song Queue", description="", color=discord.Color.dark_gold()
        )

        info = await info.get("title", None)
        i = 1
        for url in self.song_queue[ctx.guild.id]:
            embed.description += f"{i}) {info}\n"
            i += 1

        embed.set_footer(text="Thanks for using my bot! - <3Phoenix#9996")
        await ctx.send(embed=embed)
