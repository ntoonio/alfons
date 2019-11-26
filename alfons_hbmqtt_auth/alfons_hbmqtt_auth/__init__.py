from hbmqtt.plugins.authentication import BaseAuthPlugin
from passlib.hash import pbkdf2_sha256

class AlfonsHBMQTTAuthPlugin(BaseAuthPlugin):
	def __init__(self, context):
		super().__init__(context)

		self.alfonsDb = self.auth_config["alfons-db"]
		self.serverPassword = self.auth_config["server-password"]

	async def authenticate(self, *args, **kwargs):
		session = kwargs.get("session", None)

		username = session.username
		password = session.password

		if username.startswith("iot-"):
			if password == "iot":
				return True
			else:
				return False
		elif username == "server":
			if password == self.serverPassword:
				return True
			else:
				return False

		with self.alfonsDb as db:
			fetch = db.cursor.execute("SELECT password FROM users WHERE username = ?", [username]).fetchone()

			if fetch != None and len(fetch) == 1:

				if pbkdf2_sha256.verify(password, fetch[0]):
					return True

		return False
