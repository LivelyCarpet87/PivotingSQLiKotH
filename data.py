import scorebot
import creds

import logging
import json
import os

log = logging.getLogger('KingOfTheHill')
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh = logging.FileHandler(os.getcwd() + os.sep + 'history.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
log.addHandler(fh)
fh = logging.FileHandler(os.getcwd() + os.sep + 'historyINFO.log')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
log.addHandler(fh)

devices={
"a1": {
        "controlledBy": "a",
        "canAccess": ["ab","a2","ad","ac"],
        "lastReset": 0,
        "lastTakeOver":0,
        "username": "TeamA",
        "password": "ilovepico",
        "usernameFilter": ["drop","--","<",">","/*","true"],
        "passwordFilter": ["drop","--","<",">","/*","true","=","'1","'2","'3","'4","'5","'6","'7","'8","'9"],
        "queryFilter": ["N/A"],
        "AllowFilterAdditionUsername": True,
        "AllowFilterAdditionPassword": True,
        "AllowFilterAdditionQuery": True,
        "queryEnabled": False
        },
"b1": {
        "controlledBy": "b",
        "canAccess": ["ab","b2","bd","bc"],
        "lastReset": 0,
        "lastTakeOver":0,
        "username": "TeamB",
        "password": "ilovepico",
        "usernameFilter": ["drop","--","<",">","/*","true"],
        "passwordFilter": ["drop","--","<",">","/*","true","=","'1","'2","'3","'4","'5","'6","'7","'8","'9"],
        "queryFilter": ["N/A"],
        "AllowFilterAdditionUsername": True,
        "AllowFilterAdditionPassword": True,
        "AllowFilterAdditionQuery": True,
        "queryEnabled": False
        },
"c1": {
        "controlledBy": "c",
        "canAccess": ["ac","c2","bc","cd"],
        "lastReset": 0,
        "lastTakeOver":0,
        "username": "TeamC",
        "password": "ilovepico",
        "usernameFilter": ["drop","--","<",">","/*","true"],
        "passwordFilter": ["drop","--","<",">","/*","true","=","'1","'2","'3","'4","'5","'6","'7","'8","'9"],
        "queryFilter": ["N/A"],
        "AllowFilterAdditionUsername": True,
        "AllowFilterAdditionPassword": True,
        "AllowFilterAdditionQuery": True,
        "queryEnabled": False
        },
"d1": {
        "controlledBy": "d",
        "canAccess": ["cd","d2","ad","bd"],
        "lastReset": 0,
        "lastTakeOver":0,
        "username": "TeamD",
        "password": "ilovepico",
        "usernameFilter": ["drop","--","<",">","/*","true"],
        "passwordFilter": ["drop","--","<",">","/*","true","=","'1","'2","'3","'4","'5","'6","'7","'8","'9"],
        "queryFilter": ["N/A"],
        "AllowFilterAdditionUsername": True,
        "AllowFilterAdditionPassword": True,
        "AllowFilterAdditionQuery": True,
        "queryEnabled": False
        },

# Commerce DB
"a2": {
        "controlledBy": "a",
        "canAccess": ["a1","ad","ab"],
        "lastReset": 0,
        "lastTakeOver":0,
        "username": "TeamA",
        "password": "ilovepico",
        "usernameFilter": ["drop","--","<",">","/*","true"],
        "passwordFilter": ["drop","--","<",">","/*","true","=","'1","'2","'3","'4","'5","'6","'7","'8","'9"],
        "queryFilter": ["drop"],
        "AllowFilterAdditionUsername": True,
        "AllowFilterAdditionPassword": True,
        "AllowFilterAdditionQuery": True,
        "queryEnabled": True
        },
"b2": {
        "controlledBy": "b",
        "canAccess": ["b1","ab","bc"],
        "lastReset": 0,
        "lastTakeOver":0,
        "username": "TeamB",
        "password": "ilovepico",
        "usernameFilter": ["drop","--","<",">","/*","true"],
        "passwordFilter": ["drop","--","<",">","/*","true","=","'1","'2","'3","'4","'5","'6","'7","'8","'9"],
        "queryFilter": ["drop"],
        "AllowFilterAdditionUsername": True,
        "AllowFilterAdditionPassword": True,
        "AllowFilterAdditionQuery": True,
        "queryEnabled": True
        },
"c2": {
        "controlledBy": "c",
        "canAccess": ["c1","cd","bc"],
        "lastReset": 0,
        "lastTakeOver":0,
        "username": "TeamC",
        "password": "ilovepico",
        "usernameFilter": ["drop","--","<",">","/*","true"],
        "passwordFilter": ["drop","--","<",">","/*","true","=","'1","'2","'3","'4","'5","'6","'7","'8","'9"],
        "queryFilter": ["drop"],
        "AllowFilterAdditionUsername": True,
        "AllowFilterAdditionPassword": True,
        "AllowFilterAdditionQuery": True,
        "queryEnabled": True
        },
"d2": {
        "controlledBy": "d",
        "canAccess": ["d1","cd","ad"],
        "lastReset": 0,
        "lastTakeOver":0,
        "username": "TeamD",
        "password": "ilovepico",
        "usernameFilter": ["drop","--","<",">","/*","true"],
        "passwordFilter": ["drop","--","<",">","/*","true","=","'1","'2","'3","'4","'5","'6","'7","'8","'9"],
        "queryFilter": ["drop"],
        "AllowFilterAdditionUsername": True,
        "AllowFilterAdditionPassword": True,
        "AllowFilterAdditionQuery": True,
        "queryEnabled": True
        },

#sides
"ad": {
        "controlledBy": "",
        "canAccess": ["a1","d1","sp"],
        "lastReset": 0,
        "lastTakeOver":0,
        "username": "ad",
        "password": "ilovepico",
        "usernameFilter": ["drop","--","<",">","/*","true"],
        "passwordFilter": ["drop","--","<",">","/*","true","=","'1","'2","'3","'4","'5","'6","'7","'8","'9"],
        "queryFilter": ["N/A"],
        "AllowFilterAdditionUsername": True,
        "AllowFilterAdditionPassword": True,
        "AllowFilterAdditionQuery": True,
        "queryEnabled": False
        },
"ab": {
        "controlledBy": "",
        "canAccess": ["a1","b1","sp"],
        "lastReset": 0,
        "lastTakeOver":0,
        "username": "ab",
        "password": "ilovepico",
        "usernameFilter": ["drop","--","<",">","/*","true"],
        "passwordFilter": ["drop","--","<",">","/*","true","=","'1","'2","'3","'4","'5","'6","'7","'8","'9"],
        "queryFilter": ["N/A"],
        "AllowFilterAdditionUsername": True,
        "AllowFilterAdditionPassword": True,
        "AllowFilterAdditionQuery": True,
        "queryEnabled": False
        },
"bc": {
        "controlledBy": "",
        "canAccess": ["b1","c1","sp"],
        "lastReset": 0,
        "lastTakeOver":0,
        "username": "bc",
        "password": "ilovepico",
        "usernameFilter": ["drop","--","<",">","/*","true"],
        "passwordFilter": ["drop","--","<",">","/*","true","=","'1","'2","'3","'4","'5","'6","'7","'8","'9"],
        "queryFilter": ["N/A"],
        "AllowFilterAdditionUsername": True,
        "AllowFilterAdditionPassword": True,
        "AllowFilterAdditionQuery": True,
        "queryEnabled": False
        },
"cd": {
        "controlledBy": "",
        "canAccess": ["c1","d1","sp"],
        "lastReset": 0,
        "lastTakeOver":0,
        "username": "cd",
        "password": "ilovepico",
        "usernameFilter": ["drop","--","<",">","/*","true"],
        "passwordFilter": ["drop","--","<",">","/*","true","=","'1","'2","'3","'4","'5","'6","'7","'8","'9"],
        "queryFilter": ["N/A"],
        "AllowFilterAdditionUsername": True,
        "AllowFilterAdditionPassword": True,
        "AllowFilterAdditionQuery": True,
        "queryEnabled": False
        },

# Across
"bd": {
        "controlledBy": "",
        "canAccess": ["b1","d1"],
        "lastReset": 0,
        "lastTakeOver":0,
        "username": "bd",
        "password": "ilovepico",
        "usernameFilter": ["drop","--","<",">","/*","true"],
        "passwordFilter": ["drop","--","<",">","/*","true","=","'1","'2","'3","'4","'5","'6","'7","'8","'9"],
        "queryFilter": ["N/A"],
        "AllowFilterAdditionUsername": True,
        "AllowFilterAdditionPassword": True,
        "AllowFilterAdditionQuery": True,
        "queryEnabled": False
        },
"ac": {
        "controlledBy": "",
        "canAccess": ["c1","a1"],
        "lastReset": 0,
        "lastTakeOver":0,
        "username": "ac",
        "password": "ilovepico",
        "usernameFilter": ["drop","--","<",">","/*","true"],
        "passwordFilter": ["drop","--","<",">","/*","true","=","'1","'2","'3","'4","'5","'6","'7","'8","'9"],
        "queryFilter": ["N/A"],
        "AllowFilterAdditionUsername": True,
        "AllowFilterAdditionPassword": True,
        "AllowFilterAdditionQuery": True,
        "queryEnabled": False
        },

# special
"sp": {
        "controlledBy": "",
        "canAccess": ["a2","b2","c2","d2"],
        "lastReset": 0,
        "lastTakeOver":0,
        "username": "sp",
        "password": "ilovepico",
        "usernameFilter": ["drop","--","<",">","/*","true"],
        "passwordFilter": ["drop","--","<",">","/*","true","=","'1","'2","'3","'4","'5","'6","'7","'8","'9"],
        "queryFilter": ["N/A"],
        "AllowFilterAdditionUsername": True,
        "AllowFilterAdditionPassword": True,
        "AllowFilterAdditionQuery": True,
        "queryEnabled": False
        }
}

users = {
}

sampleUser={
    "Name":"",
    "password":"",
    "team":"",
    "LastLogins":{
        "a1": ["",""],
        "b1": ["",""],
        "c1": ["",""],
        "d1": ["",""],

        "a2": ["",""],
        "b2": ["",""],
        "c2": ["",""],
        "d2": ["",""],

        "ab": ["",""],
        "bc": ["",""],
        "cd": ["",""],
        "ac": ["",""],
        "bd": ["",""],
        "ad": ["",""],

        "sp": ["",""]
    }
}

teams={
    "a":{
        "Members":["",""],
        "Score":0
    },
    "b":{
        "Members":["",""],
        "Score":0
    },
    "c":{
        "Members":["",""],
        "Score":0
    },
    "d":{
        "Members":["",""],
        "Score":0
    },
}

products = {
    "Union Stickers": 1.00, #union
    "Pineapples": 12.10, # nothing
    "Communion Decor": 1.00, #union
    "Andersite Bricks": 100.00, #and
    "Anti-Union Posters for Factory Owners": 1.00, #union
    "Ripe Oranges": 5.00, #or
    "Family Reunion Presents": 100.00, #union
    "True Tales by Some Author": 7.00, #True
    "Wild Grunion": 100.00, #union
    "Story of John and Blike": 5.00, #like
    "Family Reunion Escape Plans": 10.00, #union
    "Tabletop Games": 37.00, #table
    "French Fromage": 100.00, #from
    "Bunion Medication": 100.00, #union
    "Hinge Insertion Devices": 17.00, #Insert
    "From Log In Speedboats To Dogs Orbiting the Moon": 7.00 #Logins, OR, IN
}

jwtKey=creds.jwtKey
gameStart=False

points={
"teamOwned": 20,
"contested": 15,
"special": 25,
"db": 5,
"query": 1
}

scorebotInterval = 60
modifierDivider = 3600
gameUptime = 0
hintReleaseCycle = 4*60*60

manifest = {
"devices": devices,
"users": users,
"teams": teams,
"products":products,
"jwtKey":jwtKey,
"gameStart":gameStart,
"points":points,
"modifierDivider":modifierDivider,
"gameUptime":gameUptime,
"hintReleaseCycle":hintReleaseCycle
}

def manifestUpdate():
    global manifest,devices,users,teams,products,jwtKey,gameStart,points,modifierDivider,scorebotInterval,gameUptime,hintReleaseCycle
    manifest = {
    "devices": devices,
    "users": users,
    "teams": teams,
    "products":products,
    "jwtKey":jwtKey,
    "gameStart":gameStart,
    "points":points,
    "modifierDivider":modifierDivider,
    "scorebotInterval":scorebotInterval,
    "gameUptime":gameUptime,
    "hintReleaseCycle":hintReleaseCycle
    }

def manifestLoad(manifest):
    global devices,users,teams,products,jwtKey,gameStart,points,modifierDivider,scorebotInterval,gameUptime,hintReleaseCycle
    manifest = json.loads(manifest)
    devices = manifest.get("devices",devices)
    users = manifest.get("users",users)
    teams = manifest.get("teams",teams)
    products = manifest.get("products",products)
    jwtKey = manifest.get("jwtKey",jwtKey)
    gameStart = manifest.get("gameStart",gameStart)
    points = manifest.get("points",points)
    modifierDivider = manifest.get("modifierDivider",modifierDivider)
    scorebotInterval = manifest.get("scorebotInterval",scorebotInterval)
    gameUptime = manifest.get("gameUptime",gameUptime)
    hintReleaseCycle = manifest.get("hintReleaseCycle",hintReleaseCycle)
    scorebot.scheduler.reschedule_job('scorebot',trigger="interval", seconds=scorebotInterval)
