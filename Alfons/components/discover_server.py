import socket
import json

import common as c

def start(q):
	# Start discover socket
	discoverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	discoverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	discoverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	discoverSocket.bind(("", 27369))

	addrConfig = {
		"ip": c.config["ip"],
		"domain": c.config["domain"] if "domain" in c.config else None,
		"ssl": c.config["ssl"]["enabled"]
	}

	q.put(0)

	while True:
		data, addr = discoverSocket.recvfrom(128)
		discoverSocket.sendto(json.dumps(addrConfig).encode("ascii"), addr)
