import setuptools
import os.path
import re

PATH = os.path.dirname(os.path.abspath(__file__)) + "/"

installRequires = []

with open(PATH + "requirements.txt", "r") as f:
	for l in f.readlines():
		l = re.sub("#.*$", "", l) # Removed comments
		l = l.rstrip().lstrip()

		if not l == "": # Empty lines (and commented lines which now are empty) will be removed
			installRequires.append(l)

with open(PATH + "README.md", "r") as f:
	long_description = f.read()

setuptools.setup(
	name="Alfons",
	version="0.0.1",
	author="Anton Lindroth",
	author_email="ntoonio@gmail.com",
	license="MIT",
	description="A home automation system",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/ntoonio/Alfons",
	packages=setuptools.find_packages(),
	install_requires=installRequires,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License"
	],
    entry_points={
        "hbmqtt.broker.plugins": [
			"mqtt_plugin_alfons_auth = Alfons.mqtt_plugin.auth:AlfonsHBMQTTAuthPlugin",
			"mqtt_plugin_alfons_topic = Alfons.mqtt_plugin.topic:AlfonsHBMQTTTopicPlugin"
		]
	}
)
