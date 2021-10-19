import discord
from discord.ext import commands
from utils import Utils


class Play(commands.Cog):
    def __init__(self, bot, song_queue):
        self.bot = bot

        self.song_queue = {}
        super().__init__(song_queue)

    @commands.command()
    async def play(self, ctx, *, song=None):
        if song is None:
            return await ctx.send("You must include a song to play.")

        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()

        # Song in URL Handling

        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            await ctx.send("Searching for songs, this may take a few seconds.")

            result = await Utils.search_song(self, 1, song, get_url=True)

            if result is None:
                return await ctx.send(
                    "Sorry I could not find the song you have requested."
                )

            song = result[0]

        if ctx.voice_client.source is not None:
            queue_len = len(self.song_queue[ctx.guild.id])

            if queue_len < 10:
                self.song_queue[ctx.guild.id].append(song)
                return await ctx.send(
                    f"A song is currently playing, your song has been added into queue. Position: {queue_len+1}."
                )
            else:
                return await ctx.send("Sorry, I can only hold up to 10 songs at max.")

        await Utils.play_song(self, ctx, song)
        await ctx.send(f"Now playing: {song}")
