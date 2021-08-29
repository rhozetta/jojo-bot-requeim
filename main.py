import discord
from discord.ext import commands
import random
import json

intents = discord.Intents.all()
client = commands.Bot(command_prefix="j!", intents=intents)

@client.event
async def on_ready():
	print("hello world!")

with open("tokenfile", "r") as tokenfile:
		token=tokenfile.read()

async def makestats(user):

	id = str(user.id)

	with open("stats.json") as rawstats:
		stats = json.loads(rawstats.read())

	stats[id] = {}
	userstats = stats[id]

	userstats["hp"] = 50
	userstats["dp"] = random.randrange(1, 9)
	userstats["ap"] = 10 - userstats["dp"]
	userstats["stand"] = None

	stats[id] = userstats

	statsfile = open("stats.json", "wt")
	statsfile.write(json.dumps(stats))
	statsfile.close()

# VVVVVV commands VVVVVV'

@client.command()
async def stats(ctx, *user):

	if user == [] or ctx.message.mentions == []:
		user = ctx.author
	elif ctx.message.mentions != []:
		user = ctx.message.mentions[0]

	with open("stats.json") as rawstats:
		stats = json.loads(rawstats.read())

	try:
		stats = stats[str(user.id)]

		embed = discord.Embed(title=f"stats for {user.display_name}", colour=discord.Colour(0x16eb4), description=f"health: **{stats['hp']}**\ndefense: **{stats['dp']}**\nattack: **{stats['ap']}**\nstand: **{stats['stand']}**")
	
		await ctx.send(embed=embed)
	except KeyError:
		await makestats(user)
		with open("stats.json") as rawstats:
			stats = json.loads(rawstats.read())

		stats = stats[str(user.id)]

		embed = discord.Embed(title=f"stats for {user.display_name}", colour=discord.Colour(0x16eb4), description=f"health: **{stats['hp']}**\ndefense: **{stats['dp']}**\nattack: **{stats['ap']}**\nstand: **{stats['stand']}**")
		
		await ctx.send(embed=embed)

client.run(token)
