import json

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
	userstats["money"] = 20

	stats[id] = userstats

	statsfile = open("stats.json", "wt")
	statsfile.write(json.dumps(stats))
	statsfile.close()
async def addtoinv(ctx, user, item):

	id = str(user.id)

	with open("inv.json") as rawinv:
		inv = json.loads(rawinv.read())
	
	try:
		userinv = inv[id]
		userinv.append(item)

		inv[id] = userinv

		invfile = open("inv.json", "wt")
		invfile.write(json.dumps(inv))
		invfile.close()
	except KeyError:
		userinv = []
		userinv.append(item)

		inv[id] = userinv

		invfile = open("inv.json", "wt")
		invfile.write(json.dumps(inv))
		invfile.close()

	return True
async def changestats(ctx, user, change):
	
	id = str(user.id)

	try:
		with open("stats.json") as rawstats:
			stats = json.loads(rawstats.read())
		
		stats = stats[id]

		for x in stats:
			stats[x] = change[x]
	except KeyError:
		await makestats(user)

		with open("stats.json") as rawstats:
			stats = json.loads(rawstats.read())

		for x in stats:
			stats[x] = change[x]
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
	print("aaaaaaaaaaaaaAAAAAAAAAAAA")

	stats[str(user.id)]['money'] = money

	statsfile = open("stats.json", "wt")
	statsfile.write(json.dumps(stats))
	statsfile.close()
async def getinv(user):
	try:
		with open("inv.json") as rawinv:
			inv = json.loads(rawinv.read())
		
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
			stats = json.loads(rawstats.read())

		stats = stats[str(user)]

	return stats
async def removefrominv(ctx, user, item):

	id = str(user.id)

	with open("inv.json") as rawinv:
		inv = json.loads(rawinv.read())
	
	try:
		userinv = inv[id]

		done = False
		for x in range(0, len(userinv)-1):
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