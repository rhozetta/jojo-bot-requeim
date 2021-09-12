import json
import random

from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType

async def makestats(user):

	id = str(user.id)

	with open("stats.json") as rawstats: # read the file
		stats = json.loads(rawstats.read())

	stats[id] = {} # makes an empty dict
	userstats = stats[id] # makes userstats the same as the empty dict

	userstats["max hp"] = 50 
	userstats["hp"] = 50
	userstats["dp"] = random.randrange(1, 9)
	userstats["ap"] = 10 - userstats["dp"]
	userstats["stand"] = None
	userstats["money"] = 20
	userstats["hamon level"] = None
	userstats["hamon type"] = None

	stats[id] = userstats # makes the empty dict the same as the user stats

	with open("stats.json", "wt") as rawstats: # write to the file
		rawstats.write(json.dumps(stats))

async def addtoinv(user, item):

	id = str(user.id)

	with open("inv.json") as rawinv: # read the file
		inv = json.loads(rawinv.read())
	
	try:
		userinv = inv[id] # sets the userinv to the user's inv
		userinv.append(item) # adds item to the inventory

		inv[id] = userinv # adds the userinv to the list of all inventories 

	except KeyError: # does the same thing but a few changes to add it to the full dict
		userinv = []
		userinv.append(item)

		inv[id] = userinv
	
	with open("inv.json","wt") as invfile: 
		invfile.write(json.dumps(inv))

	return True

async def giveeffect(user, effect):
	effects = await geteffects(user) # get the full list of effects
	id = str(user.id)

	effects[id].append(effect) # adds the effect

	with open("effects.json","wt") as effectsraw:
		effectsraw.write(json.dumps(effects)) # writes to the file

async def changestats(user, change):
	
	id = str(user.id)

	try:
		with open("stats.json") as rawstats: # reads the file
			stats = json.loads(rawstats.read())

		stats[id] = change # sets the stats to the passed change

		with open("stats.json", "wt") as rawstats: # writes to file
			rawstats.write(json.dumps(stats))

	except KeyError:
		await makestats(user) # makes stats

		with open("stats.json") as rawstats: # reads the file
			stats = json.loads(rawstats.read())

		stats[id] = change # sets the stats to the passed change


		with open("stats.json", "wt") as rawstats: # writes to file
			rawstats.write(json.dumps(stats))

async def checkmoney(user, check):
	with open("stats.json") as rawstats: # reads the file
		stats = json.loads(rawstats.read())

	money = stats[str(user.id)]['money'] # gets the user's money

	if money >= check:
		return True
	elif money <= check:
		return False

async def changemoney(user, mod):
	with open("stats.json") as rawstats: # reads the file
		stats = json.loads(rawstats.read())

	money = stats[str(user.id)]['money'] # gets the users money

	money += mod # adds the money

	stats[str(user.id)]['money'] = money # sets the money in the full dict

	statsfile = open("stats.json", "wt") # writes to the file
	statsfile.write(json.dumps(stats))
	statsfile.close()

async def getinv(user):
	try:
		with open("inv.json") as rawinv: # reads the file
			inv = json.load(rawinv)
		
			inv = inv[str(user.id)]

			return inv # returns inventory
	except KeyError:
		return [] # returns this if the user has no items

async def getstats(user):
	try:
		with open("stats.json") as rawstats: # reads the file
			stats = json.loads(rawstats.read())
		
		stats = stats[str(user.id)] # get the stats
	except KeyError:
		await makestats(user) # make stats for the user
		
		with open("stats.json") as rawstats: # read the file
			stats = json.load(rawstats)

		stats = stats[str(user.id)] # get the stats

	return stats

async def geteffects(user):
	with open("effects.json","r") as effectsraw: # reads the file
		effects = json.loads(effectsraw.read())
		try:
			return effects[str(user.id)]
		except KeyError:
			return [] # returns nothing if no effects

async def removefrominv(user, item):

	id = str(user.id)

	with open("inv.json") as rawinv: # reads the file
		inv = json.loads(rawinv.read())
	
	try:
		userinv = inv[id]

		done = False
		for x in range(0, len(userinv)): # finds the item
			if userinv[x] == item:
				userinv.pop(x) # removes the item
				done = True
				break
		
		if done:
			inv[id] = userinv

			invfile = open("inv.json", "wt") # writes to the file
			invfile.write(json.dumps(inv))
			invfile.close()

			return True
	except KeyError:
		return True

async def givehamon(user, hamontype):
	stats = await getstats(user) # gets the stats

	change = stats 
	change["hamon type"] = hamontype
	if hamontype == "defending": # special change to dp for defensive hamon
		change["dp"] += 15
	elif hamontype == "attacking": # special change to ap for offensive hamon
		change["ap"] += 15
	elif hamontype == "healing": # special change to hp for health hamon hamon
		change["max hp"] += 15
		change["hp"] += 15
	change["hamon level"] = 1
	change["max hp"] += 15
	change["hp"] += 15

	await changestats(user=user, change=change)

async def wonderbread(ctx, user, embededit):
	# healing from eating the loaf of bread
	stats = await getstats(user)
	change = stats
	change["hp"] += 15
	if change["hp"] > stats["max hp"]:
		change["hp"] = stats["max hp"]
	await changestats(user, change)

	possibleEffects = ["luck","resistance","strength"] # defines effects the bread can give you

	await giveeffect(user=user, effect=possibleEffects[random.randrange(len(possibleEffects))])

	await ctx.edit_origin(embed=embededit, hidden=True) # edit origin so the "use" select resets
	await ctx.send("wonder bread :yum:", hidden=True)

async def kerosene(ctx, user, target):
	await giveeffect(user=target, effect="flamable") # makes the target flamable
	return f"{user.display_name} doused {target.display_name} in kerosene"

healingitems = {"cheesecake":15,"coffee":5,"healing potion":50,"chug jug":1000000,"cookies":10,"battery acid":-10,"nuts":5,"ground sandwich": 15,"sandwich":20,"macaroon":10}
functionitems = {"wonder bread":wonderbread}
itemcosts = {"cheesecake":5,"coffee":1,"healing potion":50,"chug jug":200,"cookies":10,"battery acid":1,"nuts":5,"sandwich":20,"wonder bread":25,"macaroon":5,"kerosene":10}
combatitems = {"kerosene":kerosene}