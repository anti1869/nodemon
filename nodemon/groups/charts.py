# -*- coding: utf-8 -*-

#
# Charts group support
# Created 06.01.2014
# Author: Dmitry Litvinenko <anti1869@gmail.com>
#

import os, sys
from datetime import datetime, timedelta

def load_chartvalues(args, chart_id):
	""" Load chart values for previous days or runs """
	n = 'chart_values_%s' % chart_id
	if not n in args['db']:
		args['db'][n] = []
	return args['db'][n]	
		

def chart_dbtablecount(chart, args):
	""" Get count of items in some database table """	
	chart['values'] = load_chartvalues(args, chart['id'])
	if not 'last_dbtablecount' in args['db'] or datetime.strptime(args["db"]['last_dbtablecount'].split('.')[0], '%Y-%m-%dT%H:%M:%S') < datetime.today() - timedelta(**chart['update']): # Skip this update if it is too early
		args['db']['last_dbtablecount'] = datetime.today()
		cursor = args['connection'].cursor()
		dbtable = chart['dbtable'].split('/')			
		cursor.execute("use %s" % dbtable[0]) # Switch to specified mysql database	
		cursor.execute("select count(*) from %s" % dbtable[1])
		chart['values'].append(cursor.fetchone()[0])
	return chart

def process(config, args):
	""" Gather data for all charts """
	charts = []
	if 'connection' in args:		
		cursor = args['connection'].cursor() # Prepare mysql cursor
	for chart in config['charts']:	
		try:			
			charts.append(getattr(sys.modules[__name__], "chart_%s" % chart['type'])(chart, args))
		except AttributeError:
			sys.stderr.write('WARNING no support for "%s" chart\n' % chart['type'])
			continue
	config['charts'] = charts
	return config