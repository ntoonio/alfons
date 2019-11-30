import common
import os
import json
import logging
import asyncio
from aiohttp import web
from aiohttp_index import IndexMiddleware
import ssl

import common as c

logger = logging.getLogger(__name__)

aiohttoAccessLogger = logging.getLogger("aiohttp.access")
aiohttoAccessLogger.setLevel(logging.WARN)

loadedData = {}

def apiInfoHandle(request):
	data = {
		"external_ip": common.EXT_IP,
		"ip": common.IP,
		"ssl": c.config["web"]["ssl"]
	}

	if c.config["web"]["ssl"]:
		data["ssl_cert"] = loadedData["ssl_cert"]
		data["ssl_chain"] = loadedData["ssl_chain"]

	return web.json_response(data=data)

# Preload some data so the files won't have to be read for every page visit
def loadData():
	global loadedData

	with open(c.config["ssl"]["cert_file"]) as f:
		loadedData["ssl_cert"] = f.read()

	with open(c.config["ssl"]["chain_file"]) as f:
		loadedData["ssl_chain"] = f.read()

def start(q):
	loadData()

	app = web.Application(middlewares=[IndexMiddleware()])

	app.router.add_static("/", common.PATH + "components/web/")

	# API endpoints
	app.router.add_get("/api/v1/info/", apiInfoHandle)

	sslContext = None
	if c.config["ssl"]["enabled"]:
		sslContext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile=c.config["ssl"]["chain_file"])
		sslContext.load_cert_chain(c.config["ssl"]["cert_file"], c.config["ssl"]["key_file"])

	asyncio.set_event_loop(asyncio.new_event_loop())
	server = asyncio.get_event_loop().create_server(app.make_handler(), host="0.0.0.0", port=c.config["web"]["port"], ssl=sslContext)
	asyncio.get_event_loop().run_until_complete(server)

	q.put(0)

	asyncio.get_event_loop().run_forever()
