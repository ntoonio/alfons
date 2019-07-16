import paho.mqtt.client as mqtt
import common as c
import components as comp
import time
import logging

logger = logging.getLogger(__name__)

def on_connect(*args):
	logger.info("MQTT client connected.")

def publish(**kwargs):
	topic = kwargs.get("topic")
	payload = kwargs.get("payload", None)
	qos = kwargs.get("qos", 0)
	retain = kwargs.get("retain", False)

	client.publish(topic, payload=payload, qos=qos, retain=retain)

def start(q):
	global client

	comp.components["automation"].registerAction("mqtt", publish)

	client = mqtt.Client("client-id", transport="tcp")
	client.username_pw_set("server", password=c.MQTT_SERVER_PASSWORD)

	#client.on_message = on_message # def on_message(client, userdata, message):
	client.on_connect = on_connect

	client.connect("0.0.0.0", 27370)
	q.task_done()
	client.loop_start()
			