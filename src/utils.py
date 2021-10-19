import asyncio
import youtube_dl
import pafy
import discord
from discord.ext import commands
from discord.ext.commands import bot


class Utils:
    def __init__(self, bot):
        self.bot = bot

        self.song_queue = {}

    def setup(self):
        for guild in self.bot.guilds:
            self.song_queue[guild.id] = []

    @classmethod
    async def check_queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) > 0:
            ctx.voice_client.stop()
            await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
            self.song_queue[ctx.guild.id].pop(0)

    async def search_song(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(
            None,
            lambda: youtube_dl.YoutubeDL(
                {
                    "format": "bestaudio",
                    "quiet": True,
                }
            ).extract_info(
                f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"
            ),
        )

        if len(info["entries"]) == 0:
            return None

        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

    async def play_song(self, ctx, song):
        url = pafy.new(song).getbestaudio().url
        ctx.voice_client.play(
            discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)),
            after=lambda error: self.bot.loop.create_task(self.check_queue(ctx)),
        )
        ctx.voice_client.source.volume = 0.5


class ErrorHandler(commands.Cog):
    """A cog for global error handling."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """A global error handler cog"""

        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            message = f"You are misssing the following arguments: {error.param}"

        await ctx.send(message, delete_after=5)
