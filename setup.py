import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="Alfons",
	version="0.0.1",
	author="Anton Lindroth",
	author_email="ntoonio@gmail.com",
	description="A home automation system",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/ntoonio/Alfons",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License"
	]
)