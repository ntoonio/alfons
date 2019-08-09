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

async def apiInfoHandle(request):	
	data = {
		"external_ip": common.EXT_IP,
		"ip": common.IP
	}

	return web.json_response(data=data)

def start(q):
	asyncio.set_event_loop(asyncio.new_event_loop())
	
	app = web.Application(middlewares=[IndexMiddleware()])

	# API endpoints
	app.router.add_get("/api/v1/info/", apiInfoHandle)

	app.router.add_static("/", common.PATH + "components/web/")
	
	q.task_done()

	web.run_app(app)