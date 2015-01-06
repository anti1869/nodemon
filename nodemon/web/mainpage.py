# -*- coding: utf-8 -*-

#
# Mainpage view
# Created 30.12.2014
# Author: Dmitry Litvinenko <anti1869@gmail.com>
#

import os
import sys
import web
import json
from datetime import datetime, timedelta

from nodemon import config_loader
config = config_loader.load_config()

t_globals = {
	'title':'Nodemon Web Interface',
}

class Mainpage:		

	def GET(self):
		render = web.template.render('templates', base = "base", globals = t_globals)
		
		report_dir = os.path.join(config['web']['data-dir'], 'reports')
		
		if not os.path.isdir(report_dir): # Check data dir exist			
			return render.error("No reports dir at '%s'" % report_dir)
		
		# Generate one big report from all reports in datadir
		report_list = []
		for report_filename in os.listdir(report_dir):			
			if not os.path.isfile(os.path.join(report_dir, report_filename)) or os.path.splitext(report_filename)[1] != '.json':
				continue
			with open(os.path.join(report_dir, report_filename), 'r') as f: # Load report and append it to full report list
				report = json.load(f)
				node_last_seen = datetime.strptime(report['last-seen'], '%Y-%m-%d %H:%M:%S')
				report["alive"] = False if node_last_seen < datetime.today() - timedelta(hours = 1) else True # Check node last seen boundary
				report_list.append(report)
		
		return render.mainpage(report_list)