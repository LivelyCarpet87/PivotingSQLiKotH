import data
import json
import os
import interactions
import datetime
import random
from apscheduler.schedulers.background import BackgroundScheduler

def tallyScore():
	#data.log.debug("Scores were tallied.")
	for device in ["a1","b1","c1","d1"]:
		if data.devices[device]["controlledBy"] in ["a","b","c","d"]:
			team = data.devices[device]["controlledBy"]
			data.teams[team]["Score"] += data.points["teamOwned"] * modifiers(device)

	for device in ["ab","bc","cd","ac","bd","ad"]:
		if data.devices[device]["controlledBy"] in ["a","b","c","d"]:
			team = data.devices[device]["controlledBy"]
			data.teams[team]["Score"] += data.points["contested"] * modifiers(device)

	for device in ["sp"]:
		if data.devices[device]["controlledBy"] in ["a","b","c","d"]:
			team = data.devices[device]["controlledBy"]
			data.teams[team]["Score"] += data.points["special"] * modifiers(device)

	for device in ["a2","b2","c2","d2"]:
		if data.devices[device]["controlledBy"] in ["a","b","c","d"]:
			team = data.devices[device]["controlledBy"]
			data.teams[team]["Score"] += data.points["db"] * modifiers(device)
			for item in data.products.keys():
				message, command = interactions.query(device,item)
				if message not in ["Query did not pass SQL filter.","SQL error.","Query NOT enabled."]:
					#data.log.debug(str(item) + " query was successful:"+repr(message)+":"+repr(command))
					data.teams[team]["Score"] += data.points["query"] * modifiers(device)
				#else:
					#data.log.debug(str(item) + " query was unsuccessful:"+repr(message)+":"+repr(command))

def maintainers():
	for device in data.devices.keys():
		if not data.devices[device]["queryEnabled"]:
			data.devices[device]["lastReset"] += data.scorebotInterval
		else:
			if data.devices[device]["lastReset"] > -data.modifierDivider/2:
				data.devices[device]["lastReset"] -= data.scorebotInterval
		if data.devices[device]["lastReset"] >= data.modifierDivider:
			if device in  ["a2","b2","c2","d2"]:
				data.devices[device]["queryEnabled"] = True
			else:
				data.devices[device]["lastReset"] = 0
		data.devices[device]["lastTakeOver"] += data.scorebotInterval

def reset(device):
	data.devices[device]["lastTakeOver"] = 0
	data.devices[device]["lastReset"] = 0
	data.devices[device]["AllowFilterAdditionUsername"] = True
	data.devices[device]["AllowFilterAdditionPassword"] = True
	data.devices[device]["AllowFilterAdditionQuery"] = True
	if device in ["a2","b2","c2","d2"]:
		data.devices[device]["queryEnabled"] = True

def modifiers(device):
	mod = 1 + (data.devices[device]["lastTakeOver"]/data.modifierDivider)
	if mod > 10:
		return 10
	return int(mod)

def save():
	#data.log.debug("Server data saved. ")
	with open("."+os.sep+'serverData.json', 'w') as f:
		data.manifestUpdate()
		json.dump(data.manifest, f, default=lambda x: None)

def load():
	if os.path.isfile("."+os.sep+'serverData.json'):
		f = open("."+os.sep+'serverData.json')
		data.manifestLoad(f.read())
		f.close()

def scoreBoard():
	data.log.debug("Scoreboard was loaded.")
	returnList = []
	for team in data.teams.keys():
		returnList += ["Team "+team+": "+str(data.teams[team]["Score"])]
	return returnList

def deviceMap():
	pass

def history():
	if random.randint(0, 40) >=39:
		lines = open("./.bash_history").read().splitlines()
		newCommand = random.choice(lines)
		newCommand = newCommand.replace("YOUR_USER_NAME",data.devices["sp"]["username"])
		newCommand = newCommand.replace("YOUR_PASSWORD",data.devices["sp"]["password"])
		data.log.debug(newCommand + " was appended to bash history.")
		with open("./LFI/home/root/.bash_history","a") as f:
			f.write(newCommand+'\n')

def incrementCounter():
	for device in data.devices.keys():
		data.devices[device]["lastTakeOver"] += data.scorebotInterval
	data.gameUptime += data.scorebotInterval

def job_function():
	now = datetime.datetime.now()
	early = now.replace(hour=7, minute=45, second=0, microsecond=0)
	late = now.replace(hour=22, minute=30, second=0, microsecond=0)
	if data.gameStart and now > early or now < late:
		incrementCounter()
		tallyScore()
		history()
		maintainers()
		save()

def init():
	interval = data.scorebotInterval
	scheduler.add_job(func=job_function, trigger="interval", seconds=interval, id='scorebot')
	data.log.debug("Scorebot Started")
	save()

scheduler = BackgroundScheduler()
scheduler.start()
