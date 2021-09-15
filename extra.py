import json
import random

from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType

async def makestats(user):

	id = str(user.id)

	with open("info.json") as rawinfo: # read the file
		info = json.loads(rawinfo.read())

	info[id] = {}
	info[id]["stats"] = {} # makes an empty dict
	userstats = info[id]["stats"] # makes userstats the same as the empty dict

	userstats["max hp"] = 50 
	userstats["hp"] = 50
	userstats["dp"] = random.randrange(1, 9)
	userstats["ap"] = 10 - userstats["dp"]
	userstats["stand"] = None
	userstats["money"] = 20
	userstats["hamon level"] = None
	userstats["hamon type"] = None

	info[id]["stats"] = userstats # makes the empty dict the same as the user stats

	with open("info.json", "wt") as rawinfo: # write to the file
		rawinfo.write(json.dumps(info))

async def addtoinv(user, item):

	id = str(user.id)

	with open("info.json") as rawinfo: # read the file
		info = json.loads(rawinfo.read())
	
	try:
		userinv = info[id]["inv"] # sets the userinv to the user's inv
		userinv.append(item) # adds item to the inventory

		info[id]["inv"] = userinv # adds the userinv to the list of all inventories 

	except KeyError: # does the same thing but a few changes to add it to the full dict
		userinv = []
		userinv.append(item)

		info[id] = {}
		info[id]["inv"] = userinv
	
	with open("info.json","wt") as rawinfo: 
		rawinfo.write(json.dumps(info))

	return True

async def giveeffect(user, effect):
	with open("info.json","r") as rawinfo:
		info = json.loads(rawinfo.read()) # get the full list of effects
	id = str(user.id)

	try:
		info[id]['effects'].append(effect) # adds the effect
	except KeyError:
		info[id]['effects'] = []
		info[id]['effects'].append(effect) # adds the effect

	with open("info.json","wt") as inforaw:
		inforaw.write(json.dumps(info)) # writes to the file

async def changestats(user, change):
	
	id = str(user.id)

	try:
		with open("info.json") as rawinfo: # reads the file
			info = json.loads(rawinfo.read())

		info[id]['stats'] = change # sets the stats to the passed change

		with open("info.json", "wt") as rawinfo: # writes to file
			rawinfo.write(json.dumps(info))

	except KeyError:
		await makestats(user) # makes stats

		with open("info.json") as rawinfo: # reads the file
			info = json.loads(rawinfo.read())

		info[id]['stats'] = change # sets the stats to the passed change


		with open("info.json", "wt") as rawinfo: # writes to file
			rawinfo.write(json.dumps(info))

async def checkmoney(user, check):
	money = await getstats(user)['money']
	return money >= check

async def changemoney(user, mod):
	with open("info.json") as rawinfo: # reads the file
		info = json.loads(rawinfo.read())

	info[str(user.id)]['stats']['money'] += mod # set the money of the user

	rawinfo = open("info.json", "wt") # writes to the file
	rawinfo.write(json.dumps(info))
	rawinfo.close()

async def getinv(user):
	try:
		with open("info.json") as rawinfo: # reads the file
			info = json.loads(rawinfo.read())
		
			inv = info[str(user.id)]["inv"]

			return inv # returns inventory
	except KeyError:
		return [] # returns this if the user has no items

async def getstats(user):
	try:
		with open("info.json") as rawinfo: # reads the file
			info = json.loads(rawinfo.read())
		
		stats = info[str(user.id)]["stats"] # get the stats
	except KeyError:
		await makestats(user) # make stats for the user
		
		with open("info.json") as rawinfo: # read the file
			info = json.load(rawinfo)

		stats = info[str(user.id)]["stats"] # get the stats

	return stats

async def geteffects(user):
	with open("info.json","r") as rawinfo: # reads the file
		info = json.loads(rawinfo.read())
		try:
			return info[str(user.id)]["effects"]
		except KeyError:
			return [] # returns nothing if no effects

async def removefrominv(user, item):

	id = str(user.id)

	with open("info.json") as rawinfo: # reads the file
		info = json.loads(rawinfo.read())
	
	try:
		userinv = info[id]["inv"]

		done = False
		for x in range(0, len(userinv)): # finds the item
			if userinv[x] == item:
				userinv.pop(x) # removes the item
				done = True
				break
		
		if done:
			info[id]["inv"] = userinv

			infofile = open("info.json", "wt") # writes to the file
			infofile.write(json.dumps(info))
			infofile.close()

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

async def wonderbread(ctx, user):
	# healing from eating the loaf of bread
	stats = await getstats(user)
	change = stats
	change["hp"] += 15
	if change["hp"] > stats["max hp"]:
		change["hp"] = stats["max hp"]
	await changestats(user, change)

	possibleEffects = ["luck","resistance","strength"] # defines effects the bread can give you

	await giveeffect(user=user, effect=possibleEffects[random.randrange(len(possibleEffects))])

	await ctx.send("wonder bread :yum:", hidden=True)

async def kerosene(ctx, user, target):
	await giveeffect(user=target, effect="flamable") # makes the target flamable
	return f"{user.display_name} doused {target.display_name} in kerosene"

healingitems = {"cheesecake":15,"coffee":5,"healing potion":50,"chug jug":1000000,"cookies":10,"battery acid":-10,"nuts":5,"ground sandwich": 15,"sandwich":20,"macaroon":10}
functionitems = {"wonder bread":wonderbread}
itemcosts = {"cheesecake":5,"coffee":1,"healing potion":50,"chug jug":200,"cookies":10,"battery acid":1,"nuts":5,"sandwich":20,"wonder bread":25,"macaroon":5,"kerosene":10}
combatitems = {"kerosene":kerosene}