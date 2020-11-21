import data
import interactions
import datetime

def userFilter(device,user,item,action):
	item = str(item).lower().replace(" ", "")
	teamDevice = device == (data.users[user]["team"]+"1") or device == (data.users[user]["team"]+"2")
	if data.users[user]["LastLogins"][device] == ["",""] and not teamDevice:
		data.log.info(user+" on team "+data.users[user]["team"]+" failed to add "+item+" to usernameFilter"+" of device "+device)
		return "You must have bypassed the filters for this device to edit."
	if action == 1:
		if item not in data.devices[device]["usernameFilter"]:
			if not data.devices[device]["AllowFilterAdditionUsername"]:
				return "You may only add one item per takeover."
			elif ( (not interactions.usernameFilter(data.users[user]["LastLogins"][device][0],[item])) or teamDevice) and not interactions.usernameFilter(data.devices[device]["username"],[item]):
				data.devices[device]["usernameFilter"].append(item)
				data.log.info(user+" on team "+data.users[user]["team"]+" added "+item+" to usernameFilter"+" of device "+device)
				if not teamDevice:
					data.devices[device]["AllowFilterAdditionUsername"] = False
				return "Item added."
			else:
				data.log.info(user+" on team "+data.users[user]["team"]+" failed to add "+item+" to usernameFilter"+" of device "+device)
				return "You and the legitimate owner must pass your own filters for this device."
		else:
			return "Item already exists."
	elif action == -1:
		if item in data.devices[device]["usernameFilter"]:
			data.log.info(user+" on team "+data.users[user]["team"]+" removed "+item+" to usernameFilter"+" of device "+device)
			data.devices[device]["usernameFilter"].remove(item)
			return "Item removed."
		else:
			return "Item does not exist."

def passFilter(device,user,item,action):
	item = str(item).lower().replace(" ", "")
	teamDevice = device == (data.users[user]["team"]+"1") or device == (data.users[user]["team"]+"2")
	if data.users[user]["LastLogins"][device] == ["",""] and not teamDevice:
		data.log.info(user+" on team "+data.users[user]["team"]+" failed to add "+item+" to passwordFilter"+" of device "+device)
		return "You must have bypassed the filters for this device to edit."
	if action == 1:
		if item not in data.devices[device]["passwordFilter"]:
			if not data.devices[device]["AllowFilterAdditionPassword"]:
				return "You may only add one item per takeover."
			elif ( (not interactions.passwordFilter(data.users[user]["LastLogins"][device][1],[item])) or teamDevice) and not interactions.passwordFilter(data.devices[device]["password"],[item]):
				data.devices[device]["passwordFilter"].append(item)
				data.log.info(user+" on team "+data.users[user]["team"]+" added "+item+" to passwordFilter"+" of device "+device)
				if not teamDevice:
					data.devices[device]["AllowFilterAdditionPassword"] = False
				return "Item added."
			else:
				data.log.info(user+" on team "+data.users[user]["team"]+" failed to add "+item+" to passwordFilter"+" of device "+device)
				return "You and the legitimate owner must pass your own filters for this device. "

		else:
			return "Item already exists."
	elif action == -1:
		if item in data.devices[device]["passwordFilter"]:
			data.devices[device]["passwordFilter"].remove(item)
			data.log.info(user+" on team "+data.users[user]["team"]+" removed "+item+" to passwordFilter"+" of device "+device)
			return "Item removed."
		else:
			return "Item does not exist."

def queryFilter(device,user,item,action):
	item = str(item).lower().replace(" ", "")
	if len(item)<=2:
		return "Filter must be 2 characters or longer (excluding spaces)."
	if len(data.devices[device]["queryFilter"])> 13:
		return "Filter is capped at 13 items. "
	if action == 1:
		teamDevice = device == (data.users[user]["team"]+"1") or device == (data.users[user]["team"]+"2")
		if item not in data.devices[device]["queryFilter"]:
			if not data.devices[device]["AllowFilterAdditionQuery"]:
				return "You may only add one item per takeover."
			else:
				data.log.info(user+" on team "+data.users[user]["team"]+" added "+item+" to queryFilter"+" of device "+device)
				data.devices[device]["queryFilter"].append(item)
				if not teamDevice:
					data.devices[device]["AllowFilterAdditionQuery"] = False
				return "Item added."
		else:
			return "Item already exists."
	elif action == -1:
		if item in data.devices[device]["queryFilter"]:
			data.devices[device]["queryFilter"].remove(item)
			data.log.info(user+" on team "+data.users[user]["team"]+" removed "+item+" to queryFilter"+" of device "+device)
			return "Item removed."
		else:
			return "Item does not exist."

def whittlePasswordFilter(device):
	newFilter = []
	for item in data.devices[device]["passwordFilter"]:
		if not interactions.passwordFilter(data.devices[device]["password"],[item]):
			newFilter.append(item)
	data.devices[device]["passwordFilter"] = newFilter
