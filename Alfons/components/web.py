from flask import Flask, request, send_from_directory
import common
import os
import logging

logger = logging.getLogger(__name__)
# Silences of werkzeug logging
logging.getLogger("werkzeug").setLevel(1000)

app = Flask(__name__)

@app.route("/")
@app.route("/<path:reqPath>")
def startPage(reqPath = ""):
	if reqPath.endswith("/") or reqPath == "":
		reqPath += "index.html"
	
	return send_from_directory(common.PATH + "/components/web", reqPath)

@app.route("/apps/<path:reqPath>")
def appPage(reqPath):
	if reqPath.endswith("/"):
		reqPath += "index.html"
	
	if not os.path.isdir(common.PATH + "/apps/" + reqPath.split("/")[0]):
		return "That app doesn't exists"

	return send_from_directory(common.PATH + "/apps/", reqPath)

def start():
	logger.info("Starting Flask")
	app.run(host="0.0.0.0", port=81)