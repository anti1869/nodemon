# -*- coding: utf-8 -*-


#
# Nodemon web interface
# Created 29.12.2014
# Author: Dmitry Litvinenko <anti1869@gmail.com>
#

import sys, os
import web
from nodemon.web.report import Report
from nodemon.web.mainpage import Mainpage

abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)

urls = ( # Set url handlers
	'/', 'Mainpage',
	'/report/', 'Report',
)

# Template globals
t_globals = {
    "request_uri": ""
}

render = web.template.render('templates', base = "base", globals = t_globals)


# Run app
#if __name__ == "__main__": 
#	app = web.application(urls, globals())
#	app.run()
#	
#app = web.application(urls, globals(), autoreload=False)
#application = app.wsgifunc()	

def run_webserver():
	app = web.application(urls, globals())
	app.run()

def get_wsgi_application():
	app = web.application(urls, globals(), autoreload=False)
	return app.wsgifunc()	
	