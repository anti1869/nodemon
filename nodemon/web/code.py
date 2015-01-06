# -*- coding: utf-8 -*-


#
# Nodemon web interface
# Created 29.12.2014
# Author: Dmitry Litvinenko <anti1869@gmail.com>
#

import sys, os
import web
from report import Report
from mainpage import Mainpage


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
if __name__ == "__main__": 
	app = web.application(urls, globals())
	app.run()
	
	