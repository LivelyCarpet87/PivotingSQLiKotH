from flask import jsonify, send_file, Blueprint, render_template, abort, request
import data
import os
import scorebot
import creds

info = Blueprint('info', __name__,
                        template_folder='templates')

@info.route('/',methods=['GET'])
def base():
    return render_template("overview.html")

@info.route('/overview',methods=['GET'])
def overview():
    return render_template("overview.html")

@info.route('/aboutUs',methods=['GET'])
def aboutUs():
    return render_template("AboutUs.html")

@info.route("/scoreboard",methods=['GET'])
def scoreboard():
	return render_template("scoreboard.html",
    scores=scorebot.scoreBoard())

@info.route("/mechanicsAndScoring",methods=['GET'])
def mechanicsAndScoring():
	return render_template("mechScoring.html",
	teamOwned=data.points["teamOwned"],
	contested=data.points["contested"],
	special=data.points["special"],
	db=data.points["db"],
	query=data.points["query"],
	products=data.products.keys(),
	modifierDivider=data.modifierDivider,
	scorebotInterval=data.scorebotInterval)

@info.route('/tutorials',methods=['GET'])
def tutorials():
    return render_template("tutorials.html",
	releases=int(data.gameUptime/data.hintReleaseCycle),
	timeLeft=int((data.hintReleaseCycle-data.gameUptime%data.hintReleaseCycle) /60))

@info.route('/hints',methods=['GET'])
def hints():
    return render_template("hints.html",
	releases=int(data.gameUptime/data.hintReleaseCycle),
	timeLeft=int((data.hintReleaseCycle-data.gameUptime%data.hintReleaseCycle) /60))

@info.route("/map",methods=['GET'])
def map():
	return render_template("map.html",
	a1=data.devices["a1"]["controlledBy"] if (data.devices["a1"]["controlledBy"]!="") else "n",
	a2=data.devices["a2"]["controlledBy"] if (data.devices["a2"]["controlledBy"]!="") else "n",
	b1=data.devices["b1"]["controlledBy"] if (data.devices["b1"]["controlledBy"]!="") else "n",
	b2=data.devices["b2"]["controlledBy"] if (data.devices["b2"]["controlledBy"]!="") else "n",
	c1=data.devices["c1"]["controlledBy"] if (data.devices["c1"]["controlledBy"]!="") else "n",
	c2=data.devices["c2"]["controlledBy"] if (data.devices["c2"]["controlledBy"]!="") else "n",
	d1=data.devices["d1"]["controlledBy"] if (data.devices["d1"]["controlledBy"]!="") else "n",
	d2=data.devices["d2"]["controlledBy"] if (data.devices["d2"]["controlledBy"]!="") else "n",

	ab=data.devices["ab"]["controlledBy"] if (data.devices["ab"]["controlledBy"]!="") else "n",
	bc=data.devices["bc"]["controlledBy"] if (data.devices["bc"]["controlledBy"]!="") else "n",
	cd=data.devices["cd"]["controlledBy"] if (data.devices["cd"]["controlledBy"]!="") else "n",
	ac=data.devices["ac"]["controlledBy"] if (data.devices["ac"]["controlledBy"]!="") else "n",
	bd=data.devices["bd"]["controlledBy"] if (data.devices["bd"]["controlledBy"]!="") else "n",
	ad=data.devices["ad"]["controlledBy"] if (data.devices["ad"]["controlledBy"]!="") else "n",

	sp=data.devices["sp"]["controlledBy"] if (data.devices["sp"]["controlledBy"]!="") else "n")
