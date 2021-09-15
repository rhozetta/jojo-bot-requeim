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

class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None

    @cog_ext.cog_slash(default_permission=False, permissions={880620607102935091: [create_permission(880620607371345982, SlashCommandPermissionType.ROLE, True)]})
    async def economy(self, ctx, user:discord.Member, amount:int):
        await changemoney(user=user, mod=amount)

        if amount > 0:
            embed = discord.Embed(title=f"Economy", colour=discord.Colour(0x16eb4), description=f"gave {user.display_name} ${amount}")
        elif amount < 0:
            embed = discord.Embed(title=f"Economy", colour=discord.Colour(0x16eb4), description=f"took ${amount * -1} from {user.display_name}")
        elif amount == 0:
            embed = discord.Embed(title=f"Economy", colour=discord.Colour(0x16eb4), description=f"nothing happened!")
        await ctx.send(embed=embed, hidden=True)

    @cog_ext.cog_slash(default_permission=False, permissions={880620607102935091: [create_permission(880620607371345982, SlashCommandPermissionType.ROLE, True)]})
    async def echo(self, ctx, message):
        await ctx.send("i said it!", hidden=True)
        await ctx.channel.send(message)

    @cog_ext.cog_slash(default_permission=False, permissions={880620607102935091: [create_permission(880620607371345982, SlashCommandPermissionType.ROLE, True)]})
    async def give(self, ctx, user:discord.Member, item):

        embedfail = discord.Embed(title=f"give", colour=discord.Colour(0x16eb4), description=f"something went wrong")
        embedsuccess = discord.Embed(title=f"give", colour=discord.Colour(0x16eb4), description=f"you gave {user.display_name} {item}")
    
        if await addtoinv(user, item):
            await ctx.send(embed=embedsuccess, hidden=True)
        else:
            await ctx.send(embed=embedfail, hidden=True)

