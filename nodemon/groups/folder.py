# -*- coding: utf-8 -*-

#
# Folder group support
# Created 29.12.2014
# Author: Dmitry Litvinenko <anti1869@gmail.com>
#

import sys
import os.path
import time
from datetime import datetime, timedelta, date
import MySQLdb

def signal_freshfile(config, args):
	""" Check file or last updated file in dir fresh or rotten """
	if os.path.isfile(config['path']): # Path is a file
		config["last-update"] = datetime.fromtimestamp(os.path.getmtime(config['path']))
	else: # Path is a dir, get last modified file in there
		entries = [os.path.join(config['path'], fn) for fn in os.listdir(config['path']) if os.path.isfile(os.path.join(config['path'], fn))] # List files in dir
		entries = [(os.path.getmtime(path), path) for path in entries]
		config["last-update"] = datetime.fromtimestamp(entries[0][0])
	config["status"] = False if config["last-update"] < datetime.today() - timedelta(**config['rotten']) else True # True = fresh, False = rotten
	return config


def signal_freshdbrecord(config, args):
	""" Check last db record is fresh or rotten """
	cursor = args['connection'].cursor()
	try:
		cursor.execute("select %s from %s order by %s desc limit 1" % (config['field'], config['table'], config['field']))
	except: # Some MySQL error
		return config
	try:
		config['last-update'] = cursor.fetchone()[0]	
	except TypeError: # No records
		config['status'] = False
		config['last-update'] = None
		return config
	
	if type(config["last-update"]) is date:
		config['last-update'] = datetime.combine(config["last-update"],datetime.min.time()) # Convert date to datetime
	config["status"] = False if config["last-update"] < datetime.today() - timedelta(**config['rotten']) else True # True = fresh, False = rotten
	return config
	
	

def process(config, args):
	""" Process all signals in this group """
	signals_output = []
	if 'connection' in args and 'mysql-db' in config:		
		cursor = args['connection'].cursor()
		cursor.execute("use %s" % config['mysql-db']) # Switch to specified mysql database
	for signal in config['signals']:
		try:			
			signals_output.append(getattr(sys.modules[__name__], "signal_%s" % signal['type'])(signal, args))
		except AttributeError:
			sys.stderr.write('WARNING no support for "%s" signal in "folder" group\n' % signal['type'])
			continue
	config['signals'] = signals_output
	return config