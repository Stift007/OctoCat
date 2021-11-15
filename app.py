from quart import Quart,render_template,redirect, request
from discord.ext import ipc	
import json
from captcha.image import ImageCaptcha
import os
print(os.getcwd())

app = Quart(__name__)

ipc_client = ipc.Client(
    secret_key="d."
)  # secret_key must be the same as your server

@app.route("/")
async def index():
	return await render_template("index.html")

@app.route("/api")
@app.route("/api/intro")
async def api_intro():
	return """
	<!DOCTYPE html>
	<html>
	<head>
	<title>OctoCat API</title>
	</head>
	<body>
		<h1>OctoCat API - Introduction</h1>
		the OctoCat API was added after many People begged me to do it. It contains Statistics about:
		<ul>
		The Economy <br>
		The Moderation Stats <br>
		The Minecraft Command Stats <br>
		</ul>

		<a href="/docs/api" style="color: crimson;">Docs</a>
	</body>
	</html>
	"""

@app.route("/dashboard")
async def dashboard():
	return await render_template("dashboard.html")

@app.route("/execute/sendmsg")
async def executeSendMessage():
	guild = request.args.get("guildid")
	channel = request.args.get("channelid")
	msg = request.args.get("message")
	await ipc_client.request(
		"sendmsg",
		guildid = guild,
		channel_id=channel,
		msg=msg
	)
	return redirect("/dashboard")

@app.route("/invite")
async def invite():
    return await redirect("https://discord.com/api/oauth2/authorize?client_id=820308868705812491&permissions=2620845175&redirect_uri=http%3A%2F%2F45.85.219.90%3A4000%2Fauth%2Fredirect&response_type=code&scope=bot%20applications.commands%20applications.store.update")

@app.route("/docs/api")
@app.route("/docs/api/")
async def api_docs():
	return """
	<!DOCTYPE html>
	<html>
	<head>
	<title>OctoCat Documentation</title>
	</head>
	<body>
		<h1>OctoCat Documentation - API</h1>
		
		<h2>Getting Started</h2>
		The easiest way to get going, is using the Requests Module from Python.
		<br>
		If you, for example, wanted to access the Minecraft Command Stats, the  route to use is <ascii>/api/mcstats</ascii>
		<br><br><code>
		import requests
		<br><br>
		BASE_URL = "http://45.85.219.90:4000/api"
		<br><br>
		resp = requests.get(BASE_URL+'/mcstats').json()
		</code>
		<br>

		This will return a JSON-Object:
		<br>
		<code>

		{<br>
			"minehut":79,<br>
			"hypixel":{<br>
				"stats":913,<br>
				"rateLimits":212,<br>
				"bedwars":582,<br>
				"skyblock":80,<br>
				"requestsPosted":1575<br>
			},<br>
			"totalRequestsPosted":1654<br>
		}<br>
		</code>
		<br><br>
		<a href="/api" style="color: crimson;">API Intro</a>
	</body>
	</html>
	"""

@app.route("/auth/redirect")
async def authenticate():
	return redirect("/dashboard")

@app.route("/api/economy")
async def econ():
	with open("data/mainBank.json","r") as f:
		users = f.read()
	return json.dumps(users,indent=4)

@app.route("/api/modlog")
async def modlog():
	with open("data/modlog.json","r") as f:
		users = f.read()
	return json.dumps(users,indent=4)

@app.route("/api/mcstats")
async def minestat():
	with open("data/minestats.json","r") as f:
		users = f.read()
	return json.dumps(users,indent=4)

