from setuptools import setup

setup(name='nodemon',
	version = '0.2.0-alpha',
	description = 'Webservice node monitoring tool',
	url = 'https://github.com/anti1869/nodemon',
	author = 'Dmitry Litvinenko',
	author_email = 'anti1869@gmail.com',
	packages = ['nodemon', 'nodemon.groups', 'nodemon.web'],
	requires = ['web.py'],
	zip_safe = False)