import json
import random

from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType

async def makestats(user):

	id = str(user.id)

	with open("stats.json") as rawstats:
		stats = json.loads(rawstats.read())

	stats[id] = {}
	userstats = stats[id]

	userstats["max hp"] = 50
	userstats["hp"] = 50
	userstats["dp"] = random.randrange(1, 9)
	userstats["ap"] = 10 - userstats["dp"]
	userstats["stand"] = None
	userstats["money"] = 20
	userstats["hamon level"] = None
	userstats["hamon type"] = None

	stats[id] = userstats

	with open("stats.json", "wt") as rawstats: 
		rawstats.write(json.dumps(stats))

async def addtoinv(user, item):

	id = str(user.id)

	with open("inv.json") as rawinv: 
		inv = json.loads(rawinv.read())
	
	try:
		userinv = inv[id]
		userinv.append(item)

		inv[id] = userinv

	except KeyError:
		userinv = []
		userinv.append(item)

		inv[id] = userinv
	
	with open("inv.json","wt") as invfile: 
		invfile.write(json.dumps(inv))

	return True

async def changestats(user, change):
	
	id = str(user.id)

	try:
		with open("stats.json") as rawstats:
			stats = json.loads(rawstats.read())
		
		userstats = stats[id]

		for x in userstats:
			userstats[x] = change[x]

		stats[id] = userstats

		with open("stats.json", "wt") as rawstats:
			rawstats.write(json.dumps(stats))

	except KeyError:
		await makestats(user)

		with open("stats.json") as rawstats:
			stats = json.loads(rawstats.read())

		userstats = stats[id]

		for x in userstats:
			userstats[x] = change[x]

		stats[id] = userstats

		with open("stats.json", "wt") as rawstats:
			rawstats.write(json.dumps(stats))

async def checkmoney(user, check):
	with open("stats.json") as rawstats:
		stats = json.loads(rawstats.read())

	money = stats[str(user.id)]['money']

	if money >= check:
		return True
	elif money <= check:
		return False

async def changemoney(user, mod):
	with open("stats.json") as rawstats:
		stats = json.loads(rawstats.read())

	money = stats[str(user.id)]['money']

	money += mod

	stats[str(user.id)]['money'] = money

	statsfile = open("stats.json", "wt")
	statsfile.write(json.dumps(stats))
	statsfile.close()

async def getinv(user):
	try:
		with open("inv.json") as rawinv:
			inv = json.load(rawinv)
		
			inv = inv[str(user.id)]

			return inv
	except KeyError:
		return []

async def getstats(user):
	try:
		with open("stats.json") as rawstats:
			stats = json.loads(rawstats.read())
		
		stats = stats[str(user.id)]
	except KeyError:
		await makestats(user)
		
		with open("stats.json") as rawstats:
			stats = json.load(rawstats)

		stats = stats[str(user.id)]

	return stats

async def geteffects(user):
	with open("effects.json","r") as effectsraw:
		effects = json.loads(effectsraw.read())
		return effects[str(user.id)]

async def removefrominv(user, item):

	id = str(user.id)

	with open("inv.json") as rawinv:
		inv = json.loads(rawinv.read())
	
	try:
		userinv = inv[id]

		done = False
		for x in range(0, len(userinv)):
			if userinv[x] == item:
				userinv.pop(x)
				done = True
				break
		
		if done:
			inv[id] = userinv

			invfile = open("inv.json", "wt")
			invfile.write(json.dumps(inv))
			invfile.close()

			return True
	except KeyError:
		return True

async def givehamon(user, hamontype):
	stats = await getstats(user)

	change = stats
	change["hamon type"] = hamontype
	if hamontype == "defending":
		change["dp"] += 15
	elif hamontype == "attacking":
		change["ap"] += 15
	elif hamontype == "healing":
		change["max hp"] += 15
		change["hp"] += 15
	change["hamon level"] = 1
	change["max hp"] += 15
	change["hp"] += 15

	await changestats(user=user, change=change)

async def wonderbread(ctx, user):
	# healing from eating the loaf of bread
	stats = await getstats(user)
	change = stats
	change["hp"] += 15
	if change["hp"] > stats["max hp"]:
		change["hp"] = stats["max hp"]
	await changestats(user, change)

	# get effects
	possibleEffects = ["luck","resistance","strength"]
	effects = await geteffects(user)

	id = str(user.id)
	effects[id].append(possibleEffects[random.randrange(len(possibleEffects))])

	with open("effects.json","wt") as effectsraw:
		effectsraw.write(json.dumps(effects))

	await ctx.edit_origin(embed=embededit, hidden=True)
	await ctx.send("wonder bread :yum:", hidden=True)

healingitems = {"cheesecake":15,"coffee":5,"healing potion":50,"chug jug":1000000,"cookies":10,"battery acid":-10,"nuts":5,"ground sandwich": 15,"sandwich":20}
functionitems = {"wonder bread":wonderbread}
itemcosts = {"cheesecake":5,"coffee":1,"healing potion":50,"chug jug":200,"cookies":10,"battery acid":1,"nuts":5,"ground sandwich": None,"sandwich":20,"wonder bread":25}