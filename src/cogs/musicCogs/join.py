import discord
from discord.ext import commands
from discord.ext.commands import bot


class Join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice == None:
            return await ctx.send(
                "You are not connected to a voice channel, please connect and try again."
            )

        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

        await ctx.author.voice.channel.connect()
