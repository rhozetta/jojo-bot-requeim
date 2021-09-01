from operator import truediv
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component, ComponentContext
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import ButtonStyle, SlashCommandPermissionType

from extra import makestats, addtoinv, changestats, checkmoney, changemoney, getinv, getstats, removefrominv

import random
import json

intents = discord.Intents.all()
client = commands.Bot(command_prefix="j!", intents=intents)
slash = SlashCommand(client, sync_commands=True)


@client.event
async def on_ready():
	print("hello world!")

with open("tokenfile", "r") as tokenfile:
		token=tokenfile.read()

# VVVVVV commands VVVVVV'

@slash.slash(guild_ids=[880620607102935091])
async def stats(ctx):

	stats = await getstats(ctx.author)	

	embed = discord.Embed(title=f"stats for {ctx.author.display_name}", colour=discord.Colour(0x16eb4), description=f"health: **{stats['hp']}**\ndefense: **{stats['dp']}**\nattack: **{stats['ap']}**\nstand: **{stats['stand']}**\nmoney: **{stats['money']}**")
	
	await ctx.send(embed=embed, hidden=True)

@slash.slash(guild_ids=[880620607102935091])
@commands.cooldown(rate=1,per=86400,type=commands.BucketType.user)
async def job(ctx):

	amount = random.randrange(20, 100)

	embed = discord.Embed(title=f"working", colour=discord.Colour(0x16eb4), description=f"you worked and earned ${amount}!")

	try:
		await changemoney(user=ctx.author, mod=amount)
	except KeyError:
		await makestats(ctx.author)
		
		await changemoney(user=ctx.author, mod=amount)

	await ctx.send(embed=embed, hidden=True)

@slash.slash(guild_ids=[880620607102935091], default_permission=False, permissions={880620607102935091: [create_permission(880620607371345982, SlashCommandPermissionType.ROLE, True)]})
async def give(ctx, user, item):

	user = user.replace("<@!", "")
	user = user.replace(">", "")
	user = int(user)
	user = client.get_user(user)
	
	embedfail = discord.Embed(title=f"give", colour=discord.Colour(0x16eb4), description=f"you need to ping someone")
	embedsuccess = discord.Embed(title=f"give", colour=discord.Colour(0x16eb4), description=f"you gave {user.display_name} {item}")
	
	if await addtoinv(ctx, user, item):
		await ctx.send(embed=embedsuccess, hidden=True)
	else:
		await ctx.send(embed=embedfail, hidden=True)

@slash.slash(guild_ids=[880620607102935091])
async def inventory(ctx):

	inv = await getinv(ctx.author)
	if inv == []:
		embed = discord.Embed(title=f"your inventory", colour=discord.Colour(0x16eb4), description=f"your inventory is empty")
	else:
		message = ""
		for x in inv:
			message += f"**{x}**\n"

		embed = discord.Embed(title=f"your inventory", colour=discord.Colour(0x16eb4), description=message)
		
	await ctx.send(embed=embed, hidden=True)

buttons1 = [create_button(style=ButtonStyle.green, label="Yes"), create_button(style=ButtonStyle.blue, label="No")]
action_row1 = create_actionrow(*buttons1)

#@slash.slash(name="search", description="look for someone that is selling stand arrows", guild_ids=[880620607102935091])
async def search(ctx):
	if random.randrange(1, 100) > 90:
		
		cost = random.randrange(10, 20) * 100

		embed = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"the search was succesful! would you like to buy a stand arrow for {cost}? the seller is very impatient.")
		embedpurchase = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"you bought an arrow for {cost}!")
		embedpoor = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"you do not have sufficient funds")

		await ctx.send(embed=embed, components=[action_row1])	

		bought = False
		while not bought:

			button_ctx: ComponentContext = await wait_for_component(client, components=action_row1)

			embedsteal = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"{button_ctx.author.display_name} took the offer before you!")

			if await checkmoney(user=button_ctx.author, check=cost):
				if button_ctx.author != ctx.author:
					await button_ctx.edit_origin(embed=embedsteal, components=None)
				else:
					await button_ctx.origin_message.delete()
					await button_ctx.send(embed=embedpurchase, hidden=True)
				await addtoinv(ctx=ctx, user=str(button_ctx.author.id), item="stand arrow")
				await changemoney(user=ctx.author, mod= -cost)
				bought = True
			else:
				await button_ctx.send(embed=embedpoor, hidden=True)
	else:
		embed = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"the search was unsuccesful! maybe try again later?")
		await ctx.send(embed=embed)

buttons2 = [create_button(style=ButtonStyle.green, label="Yes"), create_button(style=ButtonStyle.blue, label="No")]
action_row2 = create_actionrow(*buttons1)

@slash.slash(guild_ids=[880620607102935091], description="use an item")
async def use(ctx, item):
	
	inv = await getinv(ctx.author)

	embedfail = discord.Embed(title=f"use item", colour=discord.Colour(0x16eb4), description=f"you dont have *{item}*!")
	embeduseless = discord.Embed(title=f"use item", colour=discord.Colour(0x16eb4), description=f"*{item}* doesnt have a use!")
	embedarrow = discord.Embed(title=f"use item", colour=discord.Colour(0x16eb4), description=f"do you want to use an arrow? (if you dont just delete this message)")

	if item not in inv:
		await ctx.send(embed=embedfail, hidden=True)
	#elif "arrow" in item:
	#	await ctx.send(embed=embedarrow, hidden=True, action_row=action_row2)
	#	button_ctx: ComponentContext = await wait_for_component(client, components=action_row2)

	#	await removefrominv(ctx=ctx, user=ctx.author, item=item)

		# do what ever would happen when you use an arrow #
	else:
		await ctx.send(embed=embeduseless, hidden=True)

client.run(token)