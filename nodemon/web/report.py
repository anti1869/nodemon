# -*- coding: utf-8 -*-

#
# Define Report view
# Created 29.12.2014
# Author: Dmitry Litvinenko <anti1869@gmail.com>
#

import os
import sys
import web
import json
from datetime import datetime
from nodemon import config_loader

config = config_loader.load_config()


class Report:	
	
	def POST(self):
		report = json.loads(web.data()) # Load report from POST data
		if not os.path.isdir(config['data-dir']): # Check data dir exist
			sys.stderr.write("ERROR no data dir available '%s'" % config['data-dir'])
			return "error"
		try:
			os.makedirs(os.path.join(config['data-dir'],'reports')) # Make dir for reports if necessary
		except OSError:
			pass
		
		report['alive'] = True
		report['external-ip'] = web.ctx['ip']
		report['last-seen'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
		
		# Save modified report file
		with open(os.path.join(config['data-dir'],'reports', "%s.json" % report['nodename']), 'w') as f:
			json.dump(report, f)
		return "ok"