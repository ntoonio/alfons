import asyncio
from hbmqtt.broker import Broker
from hbmqtt.plugins.authentication import BaseAuthPlugin
import common as c
import components as comp
import logging
import common as c

logging.getLogger("transitions.core").setLevel(100)

@asyncio.coroutine
def broker_coro():
	brokerConfig = {
		"listeners": {
			"default": {
				"bind": "0.0.0.0:" + str(c.config["broker"]["tcp_port"]),
				"type": "tcp",
				"ssl": True,
				"certfile": c.config["ssl"]["cert_file"],
				"keyfile": c.config["ssl"]["key_file"]
			},
			"ws": {
				"bind": "0.0.0.0:" + str(c.config["broker"]["ws_port"]),
				"type": "ws",
				"ssl": True,
				"certfile": c.config["ssl"]["cert_file"],
				"keyfile": c.config["ssl"]["key_file"]
			}
		},
		"timeout-disconnect-delay": 2,
		"topic-check": {
			"enabled": False
		},
		"auth": {
			"plugins": ["auth_alfons"],
			"alfons-db": comp.components["database"].db,
			"server-password": c.MQTT_SERVER_PASSWORD,
			"debugging": c.DEBUG
		}
	}

	broker = Broker(brokerConfig, None)
	yield from broker.start()

def start(q):
	asyncio.set_event_loop(asyncio.new_event_loop())
	asyncio.get_event_loop().run_until_complete(broker_coro())
	q.task_done()
	asyncio.get_event_loop().run_forever()
