import datetime
import discord
from discord import colour
from discord.ext import commands


class DJ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def dj(self, ctx, member):
        role = discord.utils.find(lambda r: r.name == "DJ", ctx.guild.roles)
        member = ctx.message.mentions[0]

        if role in member.roles:
            return await ctx.send(f"This user already has the `{role}` role.")

        if role is None:
            await ctx.guild.create_role(name="DJ", colour=discord.Colour(0x1ABC9C))

        embed = discord.Embed(
            title="Success!",
            color=discord.Color.dark_green(),
            timestamp=datetime.datetime.utcnow(),
        )
        embed.add_field(name="Role added: ", value=f"{role}", inline=True)
        embed.add_field(name="User: ", value=f"{member}", inline=True)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        await member.add_roles(role)
        await ctx.send(embed=embed)
        print(f"Successfully added the DJ Role to {member}")
