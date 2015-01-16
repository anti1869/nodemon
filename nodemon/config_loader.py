# -*- coding: utf-8 -*-

#
# Load config file
# Created 30.12.2014
# Author: Dmitry Litvinenko <anti1869@gmail.com>
#


import os
import sys
import json

CONFIG_FILENAME = 'nodemon-conf.json'
CONFIG_OPTIONS = [os.path.join(os.path.expanduser("~"), ".%s" % CONFIG_FILENAME), os.path.join('/etc', CONFIG_FILENAME), os.path.join(os.path.dirname(os.path.realpath(__file__)), CONFIG_FILENAME)]


def get_config_path():
	""" Get config filename: current user or default """	
	for option in CONFIG_OPTIONS:
		if os.path.isfile(option):
			return option	
	return None
	
def load_config():
	""" Load config """
	try:
		with open(get_config_path(), 'r') as f:
			config = json.load(f)		
	except TypeError:
		sys.stderr.write('ERROR loading config file. Make one of this files:\n'+ '\n'.join([o for o in CONFIG_OPTIONS]) + "\nPrint monitor.py --help for help\n")
		sys.exit()
	return config
	