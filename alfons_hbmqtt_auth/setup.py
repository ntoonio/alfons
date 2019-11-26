import setuptools

setuptools.setup(
    name="alfons_hbmqtt_auth",
    version="1.0.0",
    description="HBMQTT Authentication for Alfons",
    author="Anton Lindroth",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License"
    ],
    entry_points={
        "hbmqtt.broker.plugins": [
            "auth_alfons = alfons_hbmqtt_auth:AlfonsHBMQTTAuthPlugin"
        ]
    }
)
