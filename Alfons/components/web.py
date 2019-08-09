import common
import os
import json
import logging
import asyncio
from aiohttp import web
from aiohttp_index import IndexMiddleware

logger = logging.getLogger(__name__)

aiohttoAccessLogger = logging.getLogger("aiohttp.access")
aiohttoAccessLogger.setLevel(logging.WARN)

def apiInfoHandle(request):	
	data = {
		"external_ip": common.EXT_IP,
		"ip": common.IP
	}

	return web.json_response(data=data)

# This has to be created in the main loop

loop = asyncio.get_event_loop()

app = web.Application(middlewares=[IndexMiddleware()])

# API endpoints
app.router.add_get("/api/v1/info/", apiInfoHandle)

app.router.add_static("/", common.PATH + "components/web/")

handler = app.make_handler()
server = loop.create_server(handler, host="0.0.0.0", port=8080)

def start(q):
	q.task_done()

	loop.run_until_complete(server)
	loop.run_forever()