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

def apiInfoHandle(request):
	with open(c.config["ssl"]["cert_file"]) as f:
		mqttCert = f.read()

	data = {
		"external_ip": common.EXT_IP,
		"ip": common.IP,
		"cert": mqttCert
	}

	return web.json_response(data=data)

# This has to be created in the main loop

loop = asyncio.get_event_loop()

app = web.Application(middlewares=[IndexMiddleware()])

# API endpoints
app.router.add_get("/api/v1/info/", apiInfoHandle)

app.router.add_static("/", common.PATH + "components/web/")

sslContext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
sslContext.load_cert_chain(c.config["ssl"]["cert_file"], c.config["ssl"]["key_file"])

handler = app.make_handler(ssl_context=sslContext)
server = loop.create_server(handler, host="0.0.0.0", port=c.config["web_port"])

def start(q):
	q.task_done()

	loop.run_until_complete(server)
	loop.run_forever()
