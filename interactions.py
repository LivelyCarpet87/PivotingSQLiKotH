import scorebot

import data
import sqlite3
import os
import bcrypt
import flask
from flask import abort
import time

def usernameFilter(user,userFilter):
	for pattern in userFilter:
		if str(pattern).lower().replace(" ", "") in str(user).lower().replace(" ", ""):
			return "Username did not pass SQL filter.", "N/A", -1

def passwordFilter(password,passFilter):
	for pattern in passFilter:
		if str(pattern).lower().replace(" ", "") in str(password).lower().replace(" ", ""):
			return "Password did not pass SQL filter.", "N/A", -1

def login(device,username,password,user):
	userFilter = data.devices[device]["usernameFilter"]
	usrFilterRes = usernameFilter(username,userFilter)
	if usrFilterRes:
		return usrFilterRes

	passFilter = data.devices[device]["passwordFilter"]
	passFilterRes = passwordFilter(password,passFilter)
	if passFilterRes:
		return passFilterRes
	command = "SELECT * FROM logins WHERE username ='" + username + "' AND password ='" + password + "'"
	db = sqlite3.connect(":memory:")
	db.create_function("SLEEP", 1, time.sleep)
	db.create_function("WAITFOR", 1, time.sleep)
	c = db.cursor()

	c.execute("CREATE TABLE logins (username text, password text)")
	c.execute("INSERT INTO logins VALUES (?,?)",(data.devices[device]["username"],data.devices[device]["password"]))
	if data.devices[device]["queryEnabled"]:
		c.execute("CREATE TABLE products (item text, price INT)")
		for item, price in data.products.items():
			c.execute("INSERT INTO products VALUES (?,?)",(item,price))
	db.commit()

	c = db.cursor()
	try:
		x = c.execute(command)
		account = x.fetchone()
		if account:
			scorebot.reset(device)
			login = 0
			message = "Login Success."
		else:
			login = 1
			message = "Login Failed."
	except sqlite3.Warning as w:
		login = 2
		message = "Warning: "+repr(w.args[0])
	except sqlite3.Error as e:
		login = 2
		message = "Error: "+repr(e.args[0])
	db.rollback()
	db.close()
	if login == 0:
		if username != data.devices[device]["username"]: #Technically if you bypass this, it is SQL injection
			data.users[user]["LastLogins"][device][0] = username
		if password != data.devices[device]["password"]: #Technically if you bypass this, it is SQL injection
			data.users[user]["LastLogins"][device][1] = password
		return message, "N/A", 0
	elif login == 1:
		return message, command, 1
	else:
		return message, command, -2

def query(device,query):
	if not data.devices[device]["queryEnabled"]:
		return "Query NOT enabled.", "N/A"
	queryFilter = data.devices[device]["queryFilter"]
	for pattern in queryFilter:
		if str(pattern).lower().replace(" ", "") in str(query).lower().replace(" ", ""):
			return "Query did not pass SQL filter.", "N/A"
	command = "SELECT * FROM products WHERE item LIKE '%" + query + "%'"
	db = sqlite3.connect(":memory:")
	db.create_function("SLEEP", 1, time.sleep)
	db.create_function("WAITFOR", 1, time.sleep)
	c = db.cursor()

	c.execute("CREATE TABLE logins (username text, password text)")
	c.execute("INSERT INTO logins VALUES (?,?)",(data.devices[device]["username"],data.devices[device]["password"]))
	if data.devices[device]["queryEnabled"]:
		c.execute("CREATE TABLE products (item text, price INT)")
		for item, price in data.products.items():
			c.execute("INSERT INTO products VALUES (?,?)",(item,price))
	db.commit()

	c = db.cursor()
	items = None
	try:
		x = c.execute(command)
		items = x.fetchall()
		returnObj = items, command
	except sqlite3.Warning as w:
		message = "Warning: "+repr(w.args[0])
		returnObj = message, command
	except sqlite3.Error as e:
		message = "Error: "+repr(e.args[0])
		returnObj = message, command
	db.rollback()
	db.close()
	return returnObj

def shadow(password):
	password = password.encode("utf-8")
	hashed = bcrypt.hashpw(password, bcrypt.gensalt(prefix=b"2b",rounds=4)).decode("utf-8")
	return hashed

def LFI(file):
	rootDir = os.path.join(os.getcwd(),"LFI")
	initDir = os.path.join(os.getcwd(),"LFI/var/www")
	filePath = os.path.join(initDir,file)
	filePath = os.path.realpath(filePath)
	rootDir = os.path.realpath(rootDir)
	if os.path.commonpath([filePath,rootDir]) != '/home/livelycarpet87/PivotingSQLKotH/LFI':
		abort(404,"File does not exist. ")
	elif not os.path.isfile(filePath):
		abort(404,"File does not exist. ")
	else:
		f = open(filePath, "r")
		contents = f.read()
		f.close()
		contents = contents.replace("insert_hash_here",shadow(data.devices["sp"]["password"]))
		return contents
