import data
import jwt
import datetime
from flask import abort
import datetime

def login(user,password):
	if user not in data.users.keys():
		return None, 2
	if password != data.users[user]["password"]:
		return None, 1
	payload = {
			'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=2, seconds=0),
			'iat': datetime.datetime.utcnow(),
			'team': data.users[user]["team"],
			'user': user,
		}
	jwtToken = jwt.encode(
			payload,
			data.jwtKey,
			algorithm='HS256'
		)
	return jwtToken, 0

def decode_auth_token(auth_token):
	try:
		payload = None
		payload = jwt.decode(auth_token, data.jwtKey)
		return payload
	except jwt.ExpiredSignatureError:
		return payload
	except jwt.InvalidTokenError:
		return payload

def JWTValidate(authToken):
	payload = decode_auth_token(authToken)
	if not payload:
		return None, None, -1
	team = payload["team"]
	user = payload["user"]
	return team, user, 1

def validatePath(team,path):
	if len(path) % 2 != 0:
		abort(400)
	newPath = ""
	if len(path) == 0 or (team+"1") not in path[0:2]:
		return team+"1"
	for i in range(0,int(len(path)/2)):
		device = path[2*i : 2*(i+1)]
		if device[1] not in ["1","2"] and not data.gameStart:
			abort(403,"You are not allowed to attack other devices your team does not own yet. Shore up your defenses.")
		if device not in data.devices.keys():
			abort(400)
		newPath += device
		if i < (int(len(path)/2-1)):
			if data.devices[device]["controlledBy"] != team:
				return newPath
			if path[2*(i+1) : 2*(i+2)] not in data.devices[device]["canAccess"]:
				return newPath
	return newPath
