import paho.mqtt.client as mqtt
import common as c
import components as comp
import time
import logging
import ssl
from ssl import PROTOCOL_TLSv1_1

logger = logging.getLogger(__name__)

def on_connect(*args):
	logger.info("MQTT client connected.")

def on_disconnect(*args):
	logger.warn("Couldn't connect")

def publish(**kwargs):
	topic = kwargs.get("topic")
	payload = kwargs.get("payload", None)
	qos = kwargs.get("qos", 0)
	retain = kwargs.get("retain", False)

	logger.debug("Publishing '{}' to {} with qos set to {}. retain={}".format(payload, topic, qos, retain))

	client.publish(topic, payload=payload, qos=qos, retain=retain)

def start(q):
	global client

	comp.components["automation"].registerAction("mqtt", publish)

	client = mqtt.Client("client-id", transport="tcp")
	client.username_pw_set("server", password=c.MQTT_SERVER_PASSWORD)

	#client.on_message = on_message # def on_message(client, userdata, message):
	client.on_connect = on_connect
	client.on_disconnect = on_disconnect

	sslContext = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

	# curl https://curl.haxx.se/ca/cacert.pem > trusted_file
	sslContext.load_verify_locations(cafile=c.config["ssl"]["trusted_file"])

	client.tls_set_context(sslContext)

	# TODO: REMOVE - FOR DEBUGGING ONLY
	client.tls_insecure_set(True)

	client.connect("localhost", c.config["broker"]["tcp_port"])
	q.task_done()
	client.loop_start()
