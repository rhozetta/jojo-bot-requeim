from operator import truediv
from asyncio import sleep
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
client = commands.Bot(intents=intents, command_prefix="eat my nuts")
slash = SlashCommand(client, sync_commands=True,debug_guild=880620607102935091)

print("Installing wannacry...")

@client.event
async def on_ready():
	for i in range(10):
		string = "[          ]"
		print(string.replace(" ","#",i + 1))
		await sleep(0.2)
	print("Have fun!!!!!!!")

with open("tokenfile", "r") as tokenfile:
		token=tokenfile.read()

buttons1 = [create_button(style=ButtonStyle.green, label="Yes"), create_button(style=ButtonStyle.blue, label="No")]
action_row1 = create_actionrow(*buttons1)

buttons2 = [create_button(style=ButtonStyle.green, label="Yes")]
action_row2 = create_actionrow(*buttons2)

# VVVVVV commands VVVVVV'

@slash.slash()
async def stats(ctx):

	stats = await getstats(ctx.author)	

	embed = discord.Embed(title=f"stats for {ctx.author.display_name}", colour=discord.Colour(0x16eb4), description=f"health: **{stats['hp']}/{stats['max hp']}**\ndefense: **{stats['dp']}**\nattack: **{stats['ap']}**\nstand: **{stats['stand']}**\nmoney: **{stats['money']}**")
	
	await ctx.send(embed=embed, hidden=True)

@slash.slash(permissions={880620607102935091: [create_permission(884220480465305600, SlashCommandPermissionType.ROLE, False)]})
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

@slash.slash(default_permission=False, permissions={880620607102935091: [create_permission(880620607371345982, SlashCommandPermissionType.ROLE, True)]})
async def give(ctx, user:discord.Member, item):

	embedfail = discord.Embed(title=f"give", colour=discord.Colour(0x16eb4), description=f"you need to ping someone")
	embedsuccess = discord.Embed(title=f"give", colour=discord.Colour(0x16eb4), description=f"you gave {user.display_name} {item}")
	
	if await addtoinv(ctx, user, item):
		await ctx.send(embed=embedsuccess, hidden=True)
	else:
		await ctx.send(embed=embedfail, hidden=True)

@slash.slash()
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

@slash.slash(name="search", description="look for someone that is selling stand arrows or teaching hamon (good luck)", permissions={880620607102935091: [create_permission(884220480465305600, SlashCommandPermissionType.ROLE, False)]})
async def search(ctx):
	chance = random.randrange(1, 100)

	if chance in range(150, 160): # change to 81, 90
		
		cost = random.randrange(10, 20) * 100

		embed = discord.Embed(title=f"searching", colour=discord.Color(0x16eb4), description=f"the search was succesful! would you like to buy a stand arrow for {cost}? the seller is very impatient.")
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
	if chance in range(91, 100):

		stats = await getstats(ctx.author)
		if stats['hamon type'] is not None:
			embed = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"you found a hamon teacher but you already know hamon", footer_text="If no, just delete this message")
			await ctx.send(embed=embed, hidden=True)
			return

		chance = random.randrange(1, 10)

		typchance = random.randrange(1,3)
		if typchance == 1:
			hamontype = "healing"
		elif typchance == 2:
			hamontype = "attacking"
		elif typchance == 3:
			hamontype = "defending"

		if True: # chance > 7: # teacher takes money as payment
			
			cost = random.randrange(3, 7) * 150
			embed = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"you found a teacher that takes **money** as payment, would you pay **${cost}**?\n\n this teacher teaches {hamontype} hamon", footer_text="If no, just delete this message")
			embedpoor = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"you do not have sufficient funds")
			embedlearning = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"you have started to learn hamon")

			await ctx.send(embed=embed, hidden=True, components=[action_row2])

			button_ctx: ComponentContext = await wait_for_component(client, components=action_row2)

			await button_ctx.send(embed=embedlearning, hidden=True)

			stats = await getstats(button_ctx.author)

			change = stats
			change["hamon type"] = hamontype
			change["hamon level"] = 1
			change["health"] += 15

			await changestats(ctx=ctx, user=button_ctx.author, change=change)
		elif chance > 3: # teacher needs a valuble item, maybe a stand arrow?
			
			inv = await getinv(ctx.author)

			embed = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"you found a teacher that takes **a stand arrow** as payment, would you give up an arrow for training?\n\n this teacher teaches {hamontype} hamon", footer_text="If no, just delete this message")
			embedpoor = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"you do not have an arrow")
			embedlearning = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"you have started to learn hamon")

			await ctx.send(embed=embed, hidden=True, components=[action_row2])
			button_ctx: ComponentContext = await wait_for_component(client, components=action_row2)

			if "stand arrow" in inv:
				await button_ctx.send(embed=embedlearning, hidden=True)

				stats = await getstats(button_ctx.author)

				change = stats
				change["hamon type"] = hamontype
				change["hamon level"] = 1
				change["health"] += 15

				await changestats(ctx=ctx, user=button_ctx.author, change=change)
			else:
				await button_ctx.send(embed=embedpoor, hidden=True)
				return
		else: # teacher will do it for free
			embed = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"you found a teacher that you found a teacher that will teach for **free**?\n\n this teacher teaches {hamontype} hamon", footer_text="If no, just delete this message")
			embedlearning = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"you have started to learn hamon")

			await ctx.send(embed=embed, hidden=True, components=[action_row2])

			button_ctx: ComponentContext = await wait_for_component(client, components=action_row2)

			await button_ctx.send(embed=embedlearning, hidden=True)

			stats = await getstats(button_ctx.author)

			change = stats
			change["hamon type"] = hamontype
			change["hamon level"] = 1
			change["health"] += 15

			await changestats(ctx=ctx, user=button_ctx.author, change=change)
	else:
		embed = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"the search was unsuccesful! maybe try again later?")
		await ctx.send(embed=embed, hidden=True)

@slash.slash(description="use an item", permissions={880620607102935091: [create_permission(884220480465305600, SlashCommandPermissionType.ROLE, False)]})
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

#@slash.slash(permissions={880620607102935091: [create_permission(884220480465305600, SlashCommandPermissionType.ROLE, False)]})
async def stand(ctx):
	stats = await getstats(ctx.author)
	embednone = discord.Embed(title=f"stand", colour=discord.Colour(0x16eb4), description=f"you dont have a stand")
	embednone = discord.Embed(title=f"stand", colour=discord.Colour(0x16eb4), description=f"")

@slash.slash(description="hamon heal", permissions={880620607102935091: [create_permission(884220480465305600, SlashCommandPermissionType.ROLE, False)]})
async def heal(ctx, user:discord.Member = None):

	authorstats = await getstats(ctx.author)

	if user is None:
		stats = await getstats(ctx.author)
		user = ctx.author
	else:
		stats = await getstats(user)
		print(stats)

	if authorstats["hamon type"] == None:
		await ctx.send(embed=discord.Embed(title=f"healing", colour=discord.Colour(0x16eb4), description=f"you dont know hamon!"), hidden=True)
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

		await changestats(ctx=ctx, user=ctx.author, change=change)

		embed = discord.Embed(title=f"healing", colour=discord.Colour(0x16eb4), description=f"healed yourself for **{amount}**")
		await ctx.send(embed=embed, hidden=True)

client.run(token)