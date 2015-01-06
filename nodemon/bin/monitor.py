#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Nodemon main node loop file
# Created 29.12.2014
# Author: Dmitry Litvinenko <anti1869@gmail.com>
#


import os
import sys
import json
import MySQLdb
import urllib2
from datetime import datetime
from nodemon import config_loader

def import_module(name):
	""" Dynamically import module """
	mod = __import__(name)
	components = name.split('.')
	for comp in components[1:]:
		mod = getattr(mod, comp)
	return mod

	
def json_serial(obj):
	"""JSON serializer for objects not serializable by default json code
	From here http://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable-in-python """
	if isinstance(obj, datetime):
		serial = obj.isoformat()
		return serial	

def ping():
	""" Run main loop """	

	config = config_loader.load_config()
		
	# Connect to MySQL if needed
	args = {'connection' :None}
	if 'mysql' in config:
		args['connection'] = MySQLdb.connect(**config['mysql'])
	
	# What groups are in config
	supported_groups = {}
	for group_name in set([g['group'] for g in config['groups']]):
		try:
			supported_groups[group_name] = import_module('nodemon.groups.%s' % group_name) # Import support module for that group
		except ImportError:
			sys.stderr.write('WARNING no support for group "%s"\n' % group_name)
			
	# Cycle all groups
	results = []
	for group in config['groups']:
		try:
			results.append(getattr(supported_groups[group['group']], "process")(group, args)) # Get result JSON from this group
		except KeyError: # Unsupported group
			continue
	config['groups'] = results
	
	# Prepare to report
	try:
		config.pop('mysql')
	except KeyError:
		pass
		
	# Report to central
	
	request = urllib2.Request("http://%s/report/" % config['report-host'], json.dumps(config, default=json_serial), {'Content-Type': 'application/json'}) 
	try:
		f = urllib2.urlopen(request, timeout = 15)
	except urllib2.URLError:
		sys.stderr.write("ERROR connecting to report host '%s'\n" % config['report-host'])
		sys.exit()
	response = f.read()
	f.close()
	print response



if __name__ == "__main__":
	ping()