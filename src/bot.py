import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from music import Player
from cogs.musicCogs.join import Join
from cogs.musicCogs.leave import Leave
from cogs.musicCogs.search import Search


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="p!")


@bot.event
async def on_ready():
    print(f"{bot.user} is now online!")


async def setup():
    await bot.wait_until_ready()
    bot.add_cog(Player(bot))
    bot.add_cog(Join(bot))
    bot.add_cog(Leave(bot))
    bot.add_cog(Search(bot))


bot.loop.create_task(setup())
bot.run(TOKEN)
