from pyftpdlib.authorizers import DummyAuthorizer, AuthenticationFailed
from pyftpdlib.handlers import TLS_FTPHandler
from pyftpdlib.servers import FTPServer
from passlib.hash import pbkdf2_sha256
import common as c
import components as comp
import logging
import os

logger = logging.getLogger(__name__)
# Silence pyftpdlib
logging.getLogger("pyftpdlib").setLevel(100)

def createPaths(ground, path):
	if os.path.exists(ground + "/" + path):
		return True

	p = path.rstrip("/").lstrip("/").split("/")

	if not os.path.exists(ground):
		return False

	if not os.path.exists(ground + "/" + p[0]):
		os.mkdir(ground + "/" + p[0])

	if not os.path.exists(ground + "/" + path):
		return createPaths(ground + p.pop(0) + "/", "/".join(p) + "/")
	
	return True

class Authorizer(DummyAuthorizer):
	def validate_authentication(self, username, password, handler):
		with comp.components["database"].db as db:
			fetch = db.cursor.execute("SELECT password FROM users WHERE username = ?", [username]).fetchone()
			if len(fetch) == 1:
				if not pbkdf2_sha256.verify(password, fetch[0]):
					raise AuthenticationFailed
			else:
				raise AuthenticationFailed

	def get_home_dir(self, username):
		path = "users/" + username + "/data/"
		createPaths(c.config["data_path"], path)

		return c.config["data_path"] + path
	
	def get_perms(self, username):
		return "elradfmwMT"
	
	def has_perm(self, username, perm, path=None):
		return True
	
	def get_msg_login(self, username):
		return "Hi, {}!".format(username)

	def get_msg_quit(self, username):
		return "Good bye, {}".format(username)

handler = TLS_FTPHandler
del handler.proto_cmds["PASV"]
del handler.proto_cmds["EPSV"]
handler.certfile = c.PATH + "config/alfons.crt" # /etc/letsencrypt/live/antoon.io/fullchain.pem"
handler.keyfile = c.PATH + "config/alfons.pem" # /etc/letsencrypt/live/antoon.io/privkey.pem
handler.tls_control_required = True
handler.tls_data_required = True
handler.passive_ports = range(60000, 60200 + 1)
handler.masquerade_address = c.EXT_IP # kommenterad
handler.authorizer = Authorizer()

def start(q):
	server = FTPServer(("", 21), handler)
	q.task_done()
	server.serve_forever()