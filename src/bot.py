import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from cogs.musicCogs.join import Join
from cogs.musicCogs.leave import Leave
from cogs.musicCogs.search import Search
from cogs.musicCogs.play import Play
from cogs.musicCogs.pause import Pause
from cogs.musicCogs.skip import Skip
from cogs.musicCogs.queue import Queue
from cogs.misc.dj import DJ
from utils import ErrorHandler, Utils


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="p!")


@bot.event
async def on_ready():
    print(f"{bot.user} is now online!")
    game = discord.Game("p!help")
    await bot.change_presence(status=discord.Status.online, activity=game)


def run():
    async def setup():
        await bot.wait_until_ready()
        bot.add_cog(Join(bot))
        bot.add_cog(Leave(bot))
        bot.add_cog(Search(bot))
        bot.add_cog(Pause(bot))
        bot.add_cog(Play(bot, song_queue={}))
        bot.add_cog(Skip(bot))
        bot.add_cog(Queue(bot))
        bot.add_cog(DJ(bot))
        bot.add_cog(ErrorHandler(bot))

    bot.loop.create_task(setup())
    bot.run(TOKEN)


if __name__ == "__main__":
    run()
