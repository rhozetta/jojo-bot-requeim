from operator import truediv
from asyncio import sleep
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext, cog_ext
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component, ComponentContext, create_select_option, create_select
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import ButtonStyle, SlashCommandPermissionType

from extra import makestats, addtoinv, changestats, checkmoney, changemoney, getinv, getstats, removefrominv, givehamon, healingitems, functionitems, itemcosts, combatitems

import random
import json

intents = discord.Intents.all()
client = commands.Bot(intents=intents, command_prefix="eat my nuts")
slash = SlashCommand(client, sync_commands=True,debug_guild=880620607102935091,sync_on_cog_reload = True)

class Hamon(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None

    @cog_ext.cog_slash(description="hamon heal", permissions={880620607102935091: [create_permission(884220480465305600, SlashCommandPermissionType.ROLE, False)]})
    @commands.cooldown(rate=1,per=3600,type=commands.BucketType.user)
    async def heal(self, ctx:SlashContext, user:discord.Member = None):

        authorstats = await getstats(ctx.author)

        if user is None:
            stats = await getstats(ctx.author)
            user = ctx.author
        else:
            stats = await getstats(user)

        if authorstats["hamon type"] == None:
            embed = discord.Embed(title=f"healing", colour=discord.Colour(0x16eb4), description=f"you dont know hamon!")
            await ctx.send(embed=embed, hidden=True)
            return

        if authorstats["hamon type"] != "healing" and ctx.author != user:
            await ctx.send(embed=discord.Embed(title=f"healing", colour=discord.Colour(0x16eb4), description=f"you dont know the right type of hamon to heal someone else"), hidden=True)
        elif authorstats["hamon level"] < 2 and ctx.author != user:
            await ctx.send(embed=discord.Embed(title=f"healing", colour=discord.Colour(0x16eb4), description=f"you arent a high enough level to heal someone else"), hidden=True)
        elif authorstats["hamon level"] >= 2 and ctx.author != user:
            change = stats

            amountmin = stats["hamon level"] * 3
            amountmax = stats["hamon level"] * 6
            amount = random.randrange(amountmin, amountmax)

            change["hp"] += amount

            if change["hp"] > stats["max hp"]:
                change["hp"] = stats["max hp"]

            await changestats(ctx, user, change)

            embed = discord.Embed(title=f"healing", colour=discord.Colour(0x16eb4), description=f"healed **{user.display_name}** for **{amount}**")
            await ctx.send(embed=embed, hidden=True)
        elif ctx.author == user:
            change = stats

            if stats["hamon type"] == "healing":
                amountmin = stats["hamon level"] * 3 + stats["hamon level"] * 2
                amountmax = stats["hamon level"] * 6 + stats["hamon level"] * 3
            else:
                amountmin = stats["hamon level"] * 3
                amountmax = stats["hamon level"] * 6 
        
            amount = random.randrange(amountmin, amountmax)

            change["hp"] += amount

            if change["hp"] > stats["max hp"]:
                change["hp"] = stats["max hp"]

            await changestats(user=ctx.author, change=change)

            embed = discord.Embed(title=f"healing", colour=discord.Colour(0x16eb4), description=f"healed yourself for **{amount}**")
            await ctx.send(embed=embed, hidden=True)
