import socket
import threading
import json
import os
import imp
import common as c
import components as comp
import logging
import yaml
import time
import requests
from queue import Queue

logger = logging.getLogger("Alfons")

def main():
	logger.info("Starting Alfons!")

	with open(c.PATH + "config/alfons.yaml") as f:
		c.config = yaml.safe_load(f)

	# Find IP
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	c.IP = s.getsockname()[0]
	s.close()

	r = requests.get(url="https://api.ipify.org?format=json")
	c.EXT_IP = r.json()["ip"]

	addrConfig = {
		"ip": c.IP,
		"ext": c.EXT_IP
	}

	# Start discover socket
	discoverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	discoverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	discoverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	discoverSocket.bind(("", 27369))

	def discoverSocketHandler():
		while True:
			data, addr = discoverSocket.recvfrom(1024)
			discoverSocket.sendto(json.dumps(addrConfig).encode("ascii"), addr)
		
	discoverThread = threading.Thread(target=discoverSocketHandler)
	discoverThread.start()

	with open(c.PATH + "/components/manifest.json") as manifestFile:
		componentsList = json.load(manifestFile)["load_order"]

		for component in componentsList:
			fileName = component + ".py"
			module = imp.load_source(fileName[:-3], c.PATH + "/components/" + fileName)
			comp.components[fileName[:-3]] = module

	startCompQueue = Queue()

	for name in comp.components:
		def moduleThread(q, module, **kwargs):
			try:
				module.start(q, **kwargs)
			except Exception as e:
				logger.exception(e)

		startCompQueue.put(1)

		thread = threading.Thread(target=moduleThread, args=(startCompQueue, comp.components[name], ))
		thread.daemon = True
		thread.start()
		
		startCompQueue.join()

		logger.info("Set up component %s" % name)

if __name__ == "__main__":
	try:
		main()
	except Exception:
		print("KEYEYEY")