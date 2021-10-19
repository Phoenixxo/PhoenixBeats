import discord
from discord.ext import commands


class Pause(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client.is_paused():
            return ctx.send("I am already paused")

        ctx.voice_client.pause()
        await ctx.send("The current song has been paused.")
