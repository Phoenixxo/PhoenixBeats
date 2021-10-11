import discord
from discord.ext import commands


class Leave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            print("[ ✓ ] Leave command successfully executed!")
            return await ctx.voice_client.disconnect()
        else:
            print("[ ✕ ] Leave command failed!")
            await ctx.send("I am not in a voice channel.")
