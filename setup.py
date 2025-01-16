import setuptools

long_description = \
	"This tool integrates Facebook Ads Library to Python code."

setuptools.setup(
	name = "adslibrary",
	version = "1.0.0",
	description = "A Facebook Ads Library integration for Python",
	long_description = long_description,
	author = "Miguel Caparróz",
	author_email = "miguelpicolocaparroz@gmail.com",
	url = "https://github.com/0xM1gu3l/python-adslibrary",
	license = "MIT",
    package_dir = {"": "src"},
	packages = [
		"adslibrary"
	],
	package_data = {},
	install_requires = [
		"requests",
	]
)