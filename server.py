import data
import validation
import interactions
import filterManipulation
import adminFunc
import scorebot
import info


import flask
from flask import render_template,abort,redirect,request, make_response
import jwt
import os
import random
import string
import datetime


app = flask.Flask(__name__)

def render(templateName,device,message,path,command):
	if templateName == "login.html":
		if message != None:
			message = message.replace(r'"', r'\"').replace(r"'", r"\'")
			if data.devices[device]["queryEnabled"]:
				return render_template("login.html",
				device=device,
				controlledBy=data.devices[device]["controlledBy"],
				username=data.devices[device]["username"],
				usernameFilter=data.devices[device]["usernameFilter"],
				passwordFilter=data.devices[device]["passwordFilter"],
				queryFilter=data.devices[device]["queryFilter"],
				message=message,
				path=path,
				command=command)
			elif device in ["a1","b1","c1","d1"]:
				return render_template("login.html",
				device=device,
				controlledBy=data.devices[device]["controlledBy"],
				username=data.devices[device]["username"],
				message=message,
				path=path,
				command=command)
			else:
				return render_template("login.html",
				device=device,
				controlledBy=data.devices[device]["controlledBy"],
				username=data.devices[device]["username"],
				usernameFilter=data.devices[device]["usernameFilter"],
				passwordFilter=data.devices[device]["passwordFilter"],
				message=message,
				path=path,
				command=command)
		else:
			if data.devices[device]["queryEnabled"]:
				return render_template("login.html",
				device=device,
				controlledBy=data.devices[device]["controlledBy"],
				username=data.devices[device]["username"],
				usernameFilter=data.devices[device]["usernameFilter"],
				passwordFilter=data.devices[device]["passwordFilter"],
				queryFilter=data.devices[device]["queryFilter"],
				path=path,
				command=command)
			else:
				return render_template("login.html",
				device=device,
				controlledBy=data.devices[device]["controlledBy"],
				username=data.devices[device]["username"],
				usernameFilter=data.devices[device]["usernameFilter"],
				passwordFilter=data.devices[device]["passwordFilter"],
				path=path,
				command=command)
	elif templateName == "loggedIn.html":
		if message != None:
			message = message.replace(r'\"', r'\"').replace(r"'", r"\'")
			if device in ["a2","b2","c2","d2"]:
				return render_template("loggedIn.html",
				device=device,
				controlledBy=data.devices[device]["controlledBy"],
				username=data.devices[device]["username"],
				password=data.devices[device]["password"],
				usernameFilter=data.devices[device]["usernameFilter"],
				passwordFilter=data.devices[device]["passwordFilter"],
				queryEnabled=data.devices[device]["queryEnabled"],
				queryFilter=data.devices[device]["queryFilter"],
				pivots=data.devices[device]["canAccess"],
				message=message,
				path=path)
			else:
				return render_template("loggedIn.html",
				device=device,
				controlledBy=data.devices[device]["controlledBy"],
				username=data.devices[device]["username"],
				password=data.devices[device]["password"],
				usernameFilter=data.devices[device]["usernameFilter"],
				passwordFilter=data.devices[device]["passwordFilter"],
				pivots=data.devices[device]["canAccess"],
				message=message,
				path=path)
		else:
			if device in ["a2","b2","c2","d2"]:
				return render_template("loggedIn.html",
				device=device,
				controlledBy=data.devices[device]["controlledBy"],
				username=data.devices[device]["username"],
				password=data.devices[device]["password"],
				usernameFilter=data.devices[device]["usernameFilter"],
				passwordFilter=data.devices[device]["passwordFilter"],
				queryEnabled=data.devices[device]["queryEnabled"],
				queryFilter=data.devices[device]["queryFilter"],
				pivots=data.devices[device]["canAccess"],
				path=path)
			else:
				return render_template("loggedIn.html",
				device=device,
				controlledBy=data.devices[device]["controlledBy"],
				username=data.devices[device]["username"],
				password=data.devices[device]["password"],
				usernameFilter=data.devices[device]["usernameFilter"],
				passwordFilter=data.devices[device]["passwordFilter"],
				pivots=data.devices[device]["canAccess"],
				path=path)
	else:
		abort(500)

app.register_blueprint(adminFunc.adminPanel, url_prefix='/adminPanel')
app.register_blueprint(info.info, url_prefix='/info')

scorebot.init()
scorebot.load()
data.log.debug("JSON Data Loaded")


@app.before_request
def init():
	now = datetime.datetime.now()
	today8am = now.replace(hour=7, minute=45, second=0, microsecond=0)
	midnight = now.replace(hour=23, minute=0, second=0, microsecond=0)
	if now < today8am or now > midnight and request.method=='GET':
		if request.path not in ["/","/register","/adminPanel/"]:
			abort(403)

@app.errorhandler(403)
def sleep(error):
	now = datetime.datetime.now()
	today8am = now.replace(hour=7, minute=45, second=0, microsecond=0)
	midnight = now.replace(hour=23, minute=0, second=0, microsecond=0)
	if now < today8am or now > midnight:
		return render_template("sleep.html")

@app.route("/",methods=['GET'])
def base():
	return render_template("base.html")

@app.route("/register",methods=['GET','POST'])
def register():
	if flask.request.method == 'POST':
		registration = ""
		registration += request.form["user"]+":"
		registration += request.form["name"]+":"
		registration += request.form["wechatID"]+":"
		registration += request.form["password"]+"\n<br>\n"
		f = open("./registration.txt", "a")
		f.write(registration)
		data.log.info("Registration Attempt:"+registration)
		f.close()
		return "Your registration has been recieved. The admins will notify you once it is processed."
	return render_template("register.html")

@app.route("/login",methods=['GET','POST'])
def login():
	if flask.request.method == 'POST':
		user = request.form["user"]
		password = request.form["password"]
		jwtToken, success, team = validation.login(user,password)
		if success == 2:
			data.log.debug("Nonexistent user "+str(user)+" tried logging in.")
			return render_template("userLogin.html",message="No such user created. Please sign up from the home page.")
		elif success == 1:
			data.log.debug("User "+str(user)+" tried logging in with password '"+str(password)+"'.")
			return render_template("userLogin.html",message="Invalid username or password")
		else:
			response = make_response( render_template("userLogin.html",message="Logged in as member of Team "+team+".",redirect=True) )
			response.set_cookie('jwtToken', jwtToken)
			data.log.debug("User "+str(user)+" logged in.")
			return response
	else:
		return render_template("userLogin.html")

@app.route("/game",methods=['GET','POST'])
def game():
	team = ""
	user = ""
	authToken = request.cookies.get('jwtToken')
	team, user, jwtCode = validation.JWTValidate(authToken)
	if jwtCode == -1:
		return redirect("/login")
	if flask.request.method == 'GET':
		path = request.args.get("path","")
	else:
		path = request.form["path"]

	newPath = validation.validatePath(team,path)
	if path != newPath:
		data.log.debug(str(user)+" on team "+str(team)+" redirected to "+newPath)
		return redirect("/game?path="+newPath)
	else:
		device = path[len(path)-2: len(path)]
	data.log.debug(str(user)+" on team "+str(team)+" went to "+newPath)
	if data.devices[device]["controlledBy"] != team and flask.request.method == 'GET':

		if device == 'sp' and request.args.get("file"):
			data.log.info(str(user)+" on team "+str(team)+" tried LFI "+request.args.get("file"))
			return interactions.LFI(request.args.get("file"))

		return render("login.html",device,None,path,None)
	elif data.devices[device]["controlledBy"] != team and flask.request.method == 'POST':
		if request.form["action"] == "login":

			message, command, res = interactions.login(device,request.form["user"],request.form["pass"],user)

			if res == 0:
				data.log.info(str(user)+" on team "+str(team)+" took over server "+device
				+" with creds: "+request.form["user"]+":"+request.form["pass"] )
				data.devices[device]["controlledBy"] = team
				return redirect("/game?path="+path)

			else:
				data.log.debug(str(user)+" on team "+str(team)+" failed to take over server "+device
				+" with creds: "+request.form["user"]+":"+request.form["pass"] )
				return render("login.html",device,message,path,command),500
		elif request.form["action"] == "query":
			message, command = interactions.query(device,request.form["query"])
			data.log.debug(str(user)+" on team "+str(team)+" tried to query "+device
			+" with query: "+str(request.form["query"])+":"+str(message))
			return render_template("query.html",message=message,command=command),500
		else:
			return render("login.html",device,None,path,None),500

	elif data.devices[device]["controlledBy"] == team and flask.request.method == 'GET':
		data.log.debug(str(user)+" on team "+str(team)+" returned to "+device)
		return render("loggedIn.html",device,None,path,None)
	elif data.devices[device]["controlledBy"] == team and flask.request.method == 'POST':
		if request.form["action"] == "addUserFilter":
			item = request.form["item"]
			return render_template("filterEdit.html",path=path,message=filterManipulation.userFilter(device,user,item,1))
		elif request.form["action"] == "rmUserFilter":
			item = request.form["item"]
			return render_template("filterEdit.html",path=path,message=filterManipulation.userFilter(device,user,item,-1))
		elif request.form["action"] == "addPassFilter":
			item = request.form["item"]
			return render_template("filterEdit.html",path=path,message=filterManipulation.passFilter(device,user,item,1))
		elif request.form["action"] == "rmPassFilter":
			item = request.form["item"]
			return render_template("filterEdit.html",path=path,message=filterManipulation.passFilter(device,user,item,-1))
		elif request.form["action"] == "addQueryFilter":
			item = request.form["item"]
			return render_template("filterEdit.html",path=path,message=filterManipulation.queryFilter(device,user,item,1))
		elif request.form["action"] == "rmQueryFilter":
			item = request.form["item"]
			return render_template("filterEdit.html",path=path,message=filterManipulation.queryFilter(device,user,item,-1))
		elif request.form["action"] == "toggleQuery":
			if device in ["a2","b2","c2","d2"]:
				if data.devices[device]["queryEnabled"]:
					data.log.info(str(user)+" on team "+str(team)+" disabled query for "+device)
					data.devices[device]["queryEnabled"] = False
					return render_template("filterEdit.html",path=path,message="Query disabled.")
				else:
					data.log.info(str(user)+" on team "+str(team)+" enabled query for "+device)
					data.devices[device]["queryEnabled"] = True
					return render_template("filterEdit.html",path=path,message="Query enabled.")
			else:
				abort(400)
		elif request.form["action"] == "pivot":
			if request.form["pivotTo"] in data.devices[device]["canAccess"]:
				return redirect("/game?path="+str(path+request.form["pivotTo"]))
			else:
				abort(403)
		elif request.form["action"] == "regenPassword":
			data.log.info(str(user)+" on team "+str(team)+" regenerated password for "+device)
			data.devices[device]["password"] = "".join(random.choice(string.ascii_uppercase) for _ in range(4))
			filterManipulation.whittlePasswordFilter(device)
			return render("loggedIn.html",device,"Password Regenerated",path,None)
		else:
			return render("loggedIn.html",device,"Invalid Action",path,None)

@app.route("/game/forum",methods=['GET'])
def forum():
	data.log.info("Forums was loaded.")
	forums = open("forums.txt", "r")
	return forums.read()


port = int(os.getenv('PORT', 8000))
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port)
