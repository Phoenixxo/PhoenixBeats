import asyncio
import datetime
from discord.ext.commands import bot
import youtube_dl
import pafy
import discord
from discord.ext import commands


class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song_queue = {}

        self.setup()

    def setup(self):
        for guild in self.bot.guilds:
            self.song_queue[guild.id] = []

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

    @commands.command()
    async def play(self, ctx, *, song=None):
        if song is None:
            return await ctx.send("You must include a song to play.")

        if ctx.voice_client is None:
            return await ctx.send("I must be in a voice channel to play a song.")

        # Song in URL Handling

        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            await ctx.send("Searching for songs, this may take a few seconds.")

            result = await self.search_song(1, song, get_url=True)

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

        await self.play_song(ctx, song)
        await ctx.send(f"Now playing: {song}")

    

    @commands.command()
    async def queue(self, ctx):  # Display the current queue for the guild
        if len(self.song_queue[ctx.guild.id]) == 0:
            return await ctx.send("There are currently no songs in the queue.")

        song = list(self.song_queue[ctx.guild.id])
        info = self.search_song(len(self.song_queue[ctx.guild.id]), song)

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

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client is None:
            ctx.send("I am not currently playing a song.")

        if ctx.author.voice is None:
            ctx.send("I am currently not connected to a voice channel.")

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            ctx.send("I am not playing any songs for you.")

        poll = discord.Embed(
            title=f"Voting to skip song by - {ctx.author.name}#{ctx.author.discriminator}",
            description="**80% of the voice channel must vote to skip to skip the current song.**",
            color=discord.Color.blue(),
        )
        poll.add_field(name="Skip", value=":white_check_mark:")
        poll.add_field(name="Stay", value=":no_entry_sign:")
        poll.set_footer(text="Voting ends in 15 seconds.")

        poll_msg = await ctx.send(embed=poll)
        poll_id = poll_msg.id

        await poll_msg.add_reaction("\u2705")  # yes
        await poll_msg.add_reaction("\U0001F6AB")  # no

        await asyncio.sleep(15)

        poll_msg = await ctx.channel.fetch_message(poll_id)

        votes = {"\u2705": 0, "\U000F16AB": 0}
        reacted = []

        for reaction in poll_msg.reactions:
            if reaction.emoji in ["\u2705", "\U0001F6AB"]:
                async for user in reaction.users():
                    if (
                        user.voice.channel.id == ctx.voice_client.channel.id
                        and user.id not in reacted
                        and not user.bot
                    ):
                        votes[reaction.emoji] += 1

                        reacted.append(user.id)

        skip = False

        if votes["\u2705"] > 0:
            if (
                votes["\U0001F6AB"] == 0
                or votes["\u2705"] / (votes["\u2705"] + votes["\U0001F6AB"]) > 0.79
            ):  # 80% or higher
                skip = True
                embed = discord.Embed(
                    title="Song Skipped",
                    description="***Voting to skip the current song was successful, skipping now.***",
                    color=discord.Color.green(),
                )

            if not skip:
                embed = discord.Embed(
                    title="Skip Failed",
                    description="*Voting to skip the current song has failed.*\n\n**Voting failed, the vote requires at least 80% of the members to skip.**",
                    colour=discord.Colour.red(),
                )

        embed.set_footer(text="Voting has ended.")

        await poll_msg.clear_reactions()
        await poll_msg.edit(embed=embed)

        if skip:
            ctx.voice_client.stop()

    @commands.command()
    async def fskip(self, ctx):
        if ctx.voice_client is None:
            ctx.send("I am not currently playing a song.")

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            ctx.send("I am not playing any songs for you.")

        if ctx.author.voice is None:
            ctx.send("I am currently not connected to a voice channel.")

        if ctx.author.guild_permissions.administrator == True:
            ctx.voice_client.stop()
            message = discord.Embed(
                title="Song Force Skipped",
                description=f"**The current song has been successfully force skipped by: {ctx.author.name}.** :white_check_mark:",
                color=discord.Color.green(),
            )
            message.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=message)
        else:
            await ctx.send("You do not have permission to run this command.")

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client.is_paused():
            return await ctx.send("I am already paused.")

        ctx.voice_client.pause()
        await ctx.send("The current song has been paused.")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I am not connected to a voice channel.")

        if not ctx.voice_client.is_paused():
            return await ctx.send("I am already playing a song.")

        ctx.voice_client.resume()
        await ctx.send("The current song has been resumed.")


async def setup():
    await bot.wait_until_ready()
    bot.add_cog(Player(bot))
