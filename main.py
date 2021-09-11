from operator import truediv
from asyncio import sleep
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component, ComponentContext, create_select_option, create_select
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import ButtonStyle, SlashCommandPermissionType

from extra import makestats, addtoinv, changestats, checkmoney, changemoney, getinv, getstats, removefrominv, givehamon, healingitems, functionitems, itemcosts

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

	description = ""
	for x in stats:
		if x == "hp": # for the health, it makes it appear like "current/max"
			description += f"health: **{stats['hp']}/{stats['max hp']}**\n"
			continue
		if x == "max hp": # dont add a max hp stat to the message
			continue
		description += f"{x}: **{stats[x]}**\n" # adds the stat to the message

	embed = discord.Embed(title=f"stats for {ctx.author.display_name}", colour=discord.Colour(0x16eb4), description=description)
	
	await ctx.send(embed=embed, hidden=True)

@slash.slash(permissions={880620607102935091: [create_permission(884220480465305600, SlashCommandPermissionType.ROLE, False)]})
@commands.cooldown(rate=1,per=86400,type=commands.BucketType.user)
async def job(ctx):

	amount = random.randrange(20, 100) # random amount of money to be made

	embed = discord.Embed(title=f"working", colour=discord.Colour(0x16eb4), description=f"you worked and earned ${amount}!")

	try:
		await changemoney(user=ctx.author, mod=amount)
	except KeyError:
		await makestats(ctx.author)
		
		await changemoney(user=ctx.author, mod=amount)

	await ctx.send(embed=embed, hidden=True)

@slash.slash(default_permission=False, permissions={880620607102935091: [create_permission(880620607371345982, SlashCommandPermissionType.ROLE, True)]})
async def give(ctx, user:discord.Member, item):

	embedfail = discord.Embed(title=f"give", colour=discord.Colour(0x16eb4), description=f"something went wrong")
	embedsuccess = discord.Embed(title=f"give", colour=discord.Colour(0x16eb4), description=f"you gave {user.display_name} {item}")
	
	if await addtoinv(user, item):
		await ctx.send(embed=embedsuccess, hidden=True)
	else:
		await ctx.send(embed=embedfail, hidden=True)

@slash.slash(default_permission=False, permissions={880620607102935091: [create_permission(880620607371345982, SlashCommandPermissionType.ROLE, True)]})
async def echo(ctx, message):
	await ctx.send("i said it!", hidden=True)
	await ctx.channel.send(message)

@slash.slash(description="view your inventory")
async def inventory(ctx):

	inv = await getinv(ctx.author)
	if inv == []: 
		embed = discord.Embed(title=f"your inventory", colour=discord.Colour(0x16eb4), description=f"your inventory is empty")
	else: # get the inv and put it into a message
		invamounts = []
		for x in inv: # get a list of the items and the amount the user has
			amount = 0
			for y in inv:
				if y == x: # adds to the amount of that item in the inv
					amount += 1
			if f"{amount} {x}" in invamounts: # dont add the item if it is already in there
				continue
			invamounts.append(f"{amount} {x}")

		message = ""
		for x in invamounts: # put the list of items and the amounts into a message
			message += f"{x}\n"

		embed = discord.Embed(title=f"your inventory", colour=discord.Colour(0x16eb4), description=message)
		
	await ctx.send(embed=embed, hidden=True)

@slash.slash(description="check out your local corner store")
@commands.cooldown(rate=1,per=360,type=commands.BucketType.guild)
async def shop(ctx):
	items = []
	for x in itemcosts: # get all the items that you can buy
		items.append(x)

	inshop = []
	for x in range(-1, random.randrange(len(items))): # make a list of all the items in a shop without having duplicate items
		instock = items[random.randrange(len(items))]
		if instock in inshop:
			continue
		inshop.append(instock)

	options = []
	for x in inshop: # take the above result and put it into a select
		label = f"{x} - ${itemcosts[x]}"
		options.append(create_select_option(label=label, value=x))
	select = create_select(options=options, placeholder="come check out our wares!",min_values=1,custom_id="shop")
	selectionrow = create_actionrow(select)

	embed = discord.Embed(title=f"Dollar General", colour=discord.Colour(0x16eb4), description=f"come check out the random junk we have in stock today")
	await ctx.send(embed=embed, components=[selectionrow])

@slash.slash(name="search", description="look for someone that is selling stand arrows (cant do that rn) or teaching hamon (good luck)", permissions={880620607102935091: [create_permission(884220480465305600, SlashCommandPermissionType.ROLE, False)]})
@commands.cooldown(rate=1,per=86400,type=commands.BucketType.user)
async def search(ctx):
	# look for luck effect
	with open("effects.json","r") as effectsraw:
		alleffects = json.loads(effectsraw.read())
		try:
			effects = alleffects[str(ctx.author.id)]
		except KeyError:
			effects = []

	if "luck" in effects:
		chance = random.randrange(30, 100)
		for x in range(len(effects)): # look for the the luck effect's location in the list
			if effects[x] == "luck": 
				effects.pop(x) # remove the luck effect
				break
	else:
		chance = random.randrange(1, 100)

	with open("effects.json","wt") as effectsraw: # save changes to the effects list
		alleffects[str(ctx.author.id)] = effects
		effectsraw.write(json.dumps(alleffects))

	if chance in range(81, 90): # found an arrow seller
		
		cost = random.randrange(10, 20) * 100 # get the cost

		embed = discord.Embed(title=f"searching", colour=discord.Color(0x16eb4), description=f"the search was succesful! would you like to buy a stand arrow for {cost}? the seller is very impatient.")
		embedpurchase = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"you bought an arrow for {cost}!")
		embedpoor = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"you do not have sufficient funds")

		await ctx.send(embed=embed, components=[action_row1])	

		bought = False
		while not bought: # a loop because someone could press the button if they are too poor

			button_ctx: ComponentContext = await wait_for_component(client, components=action_row1)

			embedsteal = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"{button_ctx.author.display_name} took the offer before you!")

			if await checkmoney(user=button_ctx.author, check=cost): # check if the user is too poor or not
				if button_ctx.author != ctx.author: # do this if the offer was stolen
					await button_ctx.edit_origin(embed=embedsteal, components=None)
				else: # do this if the offer was taken by the finder
					await button_ctx.origin_message.delete()
					await button_ctx.send(embed=embedpurchase, hidden=True)
				await addtoinv(user=str(button_ctx.author.id), item="stand arrow") # give the user the arrow
				await changemoney(user=ctx.author, mod= -cost) # take away money
				bought = True
			else:
				await button_ctx.send(embed=embedpoor, hidden=True)
	elif chance in range(91, 100): # found a hamon teacher

		stats = await getstats(ctx.author)
		if stats['hamon type'] is not None: # check if the user already knows hamon
			embed = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"you found a hamon teacher but you already know hamon")
			await ctx.send(embed=embed, hidden=True)
			return

		chance = random.randrange(1, 10)

		typchance = random.randrange(1,3) # get the randomly selected type of hamon to be learned
		if typchance == 1:
			hamontype = "healing"
		elif typchance == 2:
			hamontype = "attacking"
		elif typchance == 3:
			hamontype = "defending"

		if chance > 7: # teacher takes money as payment
			
			cost = random.randrange(3, 7) * 150
			embed = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"you found a teacher that takes **money** as payment, would you pay **${cost}**?\n\n this teacher teaches {hamontype} hamon", footer_text="If no, just delete this message")
			embedpoor = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"you do not have sufficient funds")
			embedlearning = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"you have started to learn hamon")

			await ctx.send(embed=embed, hidden=True, components=[action_row2])

			button_ctx: ComponentContext = await wait_for_component(client, components=action_row2)
			
			if await checkmoney(user=button_ctx.author,amount=cost): # checks if the user is a rich bastard
				await button_ctx.send(embed=embedlearning, hidden=True)
				await givehamon(user=ctx.author, hamontype=hamontype)
				await changemoney(user=ctx.author, mod= -cost)
			else: # shames the user for being too poor
				await button_ctx.send(embed=embedpoor)
		elif chance > 3: # teacher needs a valuble item, maybe a stand arrow?
			
			inv = await getinv(ctx.author)

			embed = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"you found a teacher that takes **a stand arrow** as payment, would you give up an arrow for training?\n\n this teacher teaches {hamontype} hamon", footer_text="If no, just delete this message")
			embedpoor = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"you do not have an arrow")
			embedlearning = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"you have started to learn hamon")

			await ctx.send(embed=embed, hidden=True, components=[action_row2])
			button_ctx: ComponentContext = await wait_for_component(client, components=action_row2)

			if "stand arrow" in inv:
				await button_ctx.send(embed=embedlearning, hidden=True)
				await givehamon(user=ctx.author, hamontype=hamontype)
				await removefrominv(user=ctx.author,item="stand arrow")
			else:
				await button_ctx.send(embed=embedpoor, hidden=True)
				return
		else: # teacher will do it for free
			embed = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"you found a teacher that you found a teacher that will teach for **free**?\n\n this teacher teaches {hamontype} hamon", footer_text="If no, just delete this message")
			embedlearning = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"you have started to learn hamon")

			await ctx.send(embed=embed, hidden=True, components=[action_row2])

			button_ctx: ComponentContext = await wait_for_component(client, components=action_row2)

			await button_ctx.send(embed=embedlearning, hidden=True)

			await givehamon(user=ctx.author, hamontype=hamontype)
	elif chance in range(30, 60): # found a sandwich
		await addtoinv(user=ctx.author,item="ground sandwich")
		embed = discord.Embed(title=f"searching", colour=discord.Color(0x16eb4), description=f"you found a sandwich on the ground")
		await ctx.send(embed=embed, hidden=True)	
	else:
		embed = discord.Embed(title=f"searching", colour=discord.Colour(0x16eb4), description=f"the search was unsuccesful! maybe try again later?")
		await ctx.send(embed=embed, hidden=True)

@slash.slash(description="use an item", permissions={880620607102935091: [create_permission(884220480465305600, SlashCommandPermissionType.ROLE, False)]})
async def use(ctx):
	
	inv = await getinv(ctx.author)

	embedempty = discord.Embed(title=f"use item", colour=discord.Colour(0x16eb4), description=f"you dont have have any items")
	embed = discord.Embed(title=f"use item", colour=discord.Colour(0x16eb4), description=f"what item do you want to use?")

	if inv == []:
		await ctx.send(embed=embedempty, hidden=True)
		return
	else:
		options = []
		for x in inv:
			amount = 0
			for y in inv:
				if y == x: # adds to the amount of that item in the inv
					amount += 1
			if create_select_option(f"{x} - {amount}", value=x) in options: # dont add the item if it is already in there
				continue
			options.append(create_select_option(f"{x} - {amount}", value=x)) # add the option to the list of options
		select = create_select(options, placeholder="choose and item", min_values=1,custom_id="use")
		selectionrow = create_actionrow(select)
		await ctx.send(embed=embed, components=[selectionrow], hidden=True)

@slash.slash(description="hamon heal", permissions={880620607102935091: [create_permission(884220480465305600, SlashCommandPermissionType.ROLE, False)]})
@commands.cooldown(rate=1,per=3600,type=commands.BucketType.user)
async def heal(ctx, user:discord.Member = None):

	authorstats = await getstats(ctx.author)

	if user is None:
		stats = await getstats(ctx.author)
		user = ctx.author
	else:
		stats = await getstats(user)

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

		await changestats(user=ctx.author, change=change)

		embed = discord.Embed(title=f"healing", colour=discord.Colour(0x16eb4), description=f"healed yourself for **{amount}**")
		await ctx.send(embed=embed, hidden=True)

@slash.component_callback(components=["shop"])
async def shopcallback(ctx): # code called when a user buys something from a shop
	item = ctx.selected_options[0]
	cost = itemcosts[item]

	embededit = discord.Embed(title=f"Dollar General", colour=discord.Colour(0x16eb4), description=f"come check out the random junk we have in stock today")

	if await checkmoney(user=ctx.author,check=cost): # check if the user is too poor
		await changemoney(user=ctx.author, mod= -cost)
		await addtoinv(user=ctx.author, item=item)

		embed = discord.Embed(title=f"Dollar General", colour=discord.Colour(0x16eb4), description=f"you bought 1 {item} for {cost}")
		await ctx.edit_origin(embed=embededit) # edit the message so the select resets
		await ctx.send(embed=embed, hidden=True)
	else: # shuns the user for being of the lower class and unable to buy a fucking sandwich
		embed = discord.Embed(title=f"Dollar General", colour=discord.Colour(0x16eb4), description=f"sorry, but you are too poor for this")
		await ctx.edit_origin(embed=embededit)
		await ctx.send(embed=embed, hidden=True)

@slash.component_callback(components=["use"])
async def usecallback(ctx): # code called when a user uses an item
	item = ctx.selected_options[0] # get item

	embededit = discord.Embed(title=f"use item", colour=discord.Colour(0x16eb4), description=f"what item do you want to use?")
	embedusless = discord.Embed(title=f"use item", colour=discord.Colour(0x16eb4), description=f"{item} doesnt have a use")

	used = False

	if item in healingitems:

		stats = await getstats(ctx.author)
		change = stats

		amount = healingitems[item] # get the amount that the item heals
		change["hp"] += amount # add the amount to the change list
			
		if change["hp"] > stats["max hp"]: # set the hp to the max hp if it cose over
			change["hp"] = stats["max hp"]

		await changestats(user=ctx.author, change=change) # submit the changes to the file

		embedused = discord.Embed(title=f"use item", colour=discord.Colour(0x16eb4), description=f"you used {item} and healed for {amount}")
		await ctx.edit_origin(embed=embededit, hidden=True) # edit so the select is reset
		await ctx.send(embed=embedused, hidden=True)

		await removefrominv(user=ctx.author, item=item)
		used = True
	if item in functionitems:
		itemfunc = functionitems[item]
		await itemfunc(ctx=ctx,user=ctx.author,embededit=embededit)

		await removefrominv(user=ctx.author, item=item)
		used = True
	if not used:
		await ctx.edit_origin(embed=embededit, hidden=True) # edit so the select is reset
		await ctx.send(embed=embedusless, hidden=True)

client.run(token)