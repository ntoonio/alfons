import os
import logging
import datetime
import string
import secrets

DEBUG = True
PATH = os.path.dirname(os.path.abspath(__file__)) + "/"

class CustomFormatter(logging.Formatter):
	def format(self, record):

		t = datetime.datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")

		# 8 is the longest logging livel name, "CRITICAL"
		header = "[{} {} {}{}] ".format(t, record.levelname, " "*(8 - len(record.levelname)), record.name)
		
		try:
			message = record.msg % record.args
		except:
			message = record.msg

		if record.levelno >= 40:
			return header + "{}:{} {} {}".format(record.pathname, record.lineno, message, self.formatException(record.exc_info) or "")
		elif record.levelno >= 30:
			return header + "{} {}".format(record.pathname, message)
		elif record.levelno >= 20:
			return header + "{}".format(message)
		else:
			fileName = os.path.basename(record.pathname)
			return header + "{}".format(message)

fh = logging.FileHandler(PATH + "/Alfons.log")
ch = logging.StreamHandler()
fmt = CustomFormatter()
fh.setFormatter(fmt)
ch.setFormatter(fmt)
fh.level = 10 if DEBUG else 30
ch.level = 20
logging.basicConfig(handlers=[fh, ch], level=0)

config = {}

def generateId(length, onlyHex = False, noPunctation = True):
	return "".join(secrets.choice(string.digits + "abcdef" if onlyHex else string.ascii_letters + string.digits + ("" if noPunctation else string.punctuation)) for _ in range(length))

IP = None
EXT_IP = None

MQTT_SERVER_PASSWORD = generateId(20, False)