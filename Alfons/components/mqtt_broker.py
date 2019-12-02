import asyncio
from hbmqtt.broker import Broker
from hbmqtt.plugins.authentication import BaseAuthPlugin
import common as c
import components as comp
import logging

logging.getLogger("transitions.core").setLevel(100)

@asyncio.coroutine
def broker_coro():
	print("starting broker", c.config["ssl"]["enabled"],)
	brokerConfig = {
		"listeners": {
			"default": {
				"bind": "0.0.0.0:" + str(c.config["mqtt"]["tcp_port"]),
				"type": "tcp",
				"ssl": c.config["ssl"]["enabled"],
				"cafile": c.config["ssl"]["chain_file"],
				"certfile": c.config["ssl"]["cert_file"],
				"keyfile": c.config["ssl"]["key_file"]
			},
			"ws": {
				"bind": "0.0.0.0:" + str(c.config["mqtt"]["ws_port"]),
				"type": "ws",
				"ssl": c.config["ssl"]["enabled"],
				"cafile": c.config["ssl"]["chain_file"],
				"certfile": c.config["ssl"]["cert_file"],
				"keyfile": c.config["ssl"]["key_file"]
			}
		},
		"timeout-disconnect-delay": 2,
		"topic-check": {
			"enabled": True,
			"plugins": ["mqtt_plugin_alfons_topic"]
		},
		"auth": {
			"plugins": ["mqtt_plugin_alfons_auth"],
			"alfons-db": comp.components["database"].db,
			"server-password": c.MQTT_SERVER_PASSWORD
		}
	}

	broker = Broker(brokerConfig, None)
	yield from broker.start()

def start(q):
	asyncio.set_event_loop(asyncio.new_event_loop())
	asyncio.get_event_loop().run_until_complete(broker_coro())

	q.put(0)
	asyncio.get_event_loop().run_forever()
