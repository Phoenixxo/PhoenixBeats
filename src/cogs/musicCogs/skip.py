import asyncio
import datetime
import discord
from discord.ext import commands


class Skip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

        if (
            ctx.author.guild_permissions.administrator == True
            or ctx.author.id == "192046673306976257"
        ):
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
