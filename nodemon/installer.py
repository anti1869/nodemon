# -*- coding: utf-8 -*-

#
# First time installation and configuration script
# Created 16.01.2015
# Author: Dmitry Litvinenko <anti1869@gmail.com>
#

import nodemon
import os
from nodemon import config_loader
import re
import crypt # Windows does not have that one
import random


def make_htpasswd(password):
	""" This one is from here https://gist.github.com/eculver/1420227 """
	letters = 'abcdefghijklmnopqrstuvwxyz' \
				'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
				'0123456789/.'
	salt = random.choice(letters) + random.choice(letters)    
	return crypt.crypt(password, salt)

def get_option(min_value, max_value):
	""" Return one of the available options """
	answer = 0
	while answer < min_value or answer > max_value:
		try:
			answer = int(raw_input("Please, decide: "))
		except ValueError:
			answer = 0	
	return answer
	
def yes_or_no(message, default = "y"):
	""" Retun yes or no answer """
	answer = "dunno, dude"
	while answer.lower() not in ['', 'y', 'n']:
		answer = raw_input('%s [%s / %s] ' % (message, 'Y' if default == 'y' else 'y', 'N' if default == 'n' else 'n'))
	if answer == '': answer = default
	return answer
	
def patterned_answer(message, pattern, default = ""):
	""" Get answer matching characters """
	p = re.compile(pattern)
	answer = ""
	while answer == "" or not p.match(answer):		 
		answer = raw_input(message + " ")
		if answer == "": answer = default
	return answer
	
def install_webinterface_files(data_dir = None, report_host_auth_username = None, report_host_auth_password = None):
	""" Init webinterface directory. This could be run either from --install or --install-web entrypoints """
	if data_dir == None:		
		data_dir = os.getcwd()		
	print "\nInstalling web interface files to %s" % data_dir
	
	if os.path.exists(os.path.join(data_dir, 'webinterface.py')):
		print "This directory have webinterface already installed."
		if yes_or_no('Erase it and continue with new installation?', default = 'n') == 'n':
			return
	
	webscript = 'from nodemon.web import code\nif __name__ == "__main__":\n\tcode.run_webserver()\napplication = code.get_wsgi_application()'
	try:
		with open(os.path.join(data_dir, 'webinterface.py'), 'w') as f:
			f.write(webscript)	
	except IOError:
		print "ERROR you don't have WRITE permission to %s" % data_dir
	try:
		os.makedirs(os.path.join(data_dir, 'static'))
	except OSError:
		pass
		
	if report_host_auth_username is None:
		if yes_or_no("Do you want to protect web interface with password?") == 'y':
			report_host_auth_username = raw_input("Set username (blank for cancel): ")
			report_host_auth_password = raw_input("And password (blank for cancel): ")
		else:
			report_host_auth_username, report_host_auth_password = ('','')
	if report_host_auth_username != '' and report_host_auth_password != '':
		htpasswd = "%s:%s" % (report_host_auth_username,make_htpasswd(report_host_auth_password))
		with open(os.path.join(data_dir, '.htpasswd'), 'w') as f:
			f.write(htpasswd)	
	else:
		try:
			os.remove(os.path.join(data_dir, '.htpasswd')) # Unprotect dir if there was previous installation
		except OSError:
			pass
	print "%s webinterface installed. See docs for details what to do next" % nodemon.PACKAGE_NAME
	
					

def run_installer():
	print "Hello, let's install %s data dir, and basic config" % nodemon.PACKAGE_NAME

	print "\n[1 of 5]"
	print "Tell me, where do you want your node configuration file to be installed."
	print "You need to have WRITE permission to that directory. Options are:"
	print "\n".join("%s. %s" % (i + 1, p) for i, p in enumerate(config_loader.CONFIG_OPTIONS[:-1]))	
	config_filename = config_loader.CONFIG_OPTIONS[get_option(1, len(config_loader.CONFIG_OPTIONS) - 1) - 1] # Last option is excluded from available list
	if os.path.isfile(config_filename):
		print "I've found existing %s" % config_filename
		print "If you will continue with this installer, it will be completely erased!"
		if yes_or_no('Erase old config and continue with the new one?', default = 'n') == 'n':
			return	
	try:
		with open(config_filename, 'w') as f: # Test selected dir for writing
			f.write("{}")
		os.remove(config_filename) # We don't need it now
	except IOError:
		print "ERROR can't write to %s" % config_filename
		print "Check your permissions and come again, or rerun this script as root or sudo"
		return
	
	system_hostname = __import__('socket').gethostname()
	print "\n[2 of 5]"	
	print "Name your node (may be '%s'?)" % system_hostname
	node_name = patterned_answer("Only latin letters, numbers and ._-, please:", '[a-zA-Z0-9\._\-]+', system_hostname)	
	
	print "\n[3 of 5]"
	install_web = True if yes_or_no("Will '%s' host a report web interface?" % node_name, default = 'n') == 'y' else False
	
	print "\n[4 of 5]"
	print "What is the url of report web interface this node should report to?"
	report_host = patterned_answer("Example: %s" % ("localhost" if install_web else "webinterface.nodemon.com:8080"), '[a-zA-Z0-9\._\-]+', "localhost" if install_web else "")
	report_host_auth_username = raw_input("Report interface username (blank for none): ")
	report_host_auth_password = raw_input("That user password (blank for none): ")
	
	print "\n[5 of 5]"
	print "Decide where to put %s data dir" % nodemon.PACKAGE_NAME
	while True:
		data_dir = raw_input("Default is %s: " % os.path.join(os.path.expanduser("~"), nodemon.PACKAGE_NAME.lower()))
		if data_dir == "": data_dir = os.path.join(os.path.expanduser("~"), nodemon.PACKAGE_NAME.lower())
		data_dir = data_dir.rstrip(nodemon.PACKAGE_NAME.lower()).rstrip('/')
		data_dir = os.path.join(data_dir, nodemon.PACKAGE_NAME.lower()) # Now we are sure that we have only one /nodemon on the end of the path
		if os.path.isdir(data_dir):
			print "That directory already exist. I will not delete any reports there"
			break
		else:
			try:
				os.makedirs(data_dir)
				break
			except OSError:
				print "I'm sorry, but you do not have WRITE permissions to %s" % data_dir
				print "Choose another directory for data files."
				
	if install_web:
		install_webinterface_files(data_dir, report_host_auth_username, report_host_auth_password)

	print '\n\nInstalling config file...'
	print config_filename
	# Construct and write pretty config file
	config = '{\n\t"comment":"Check out detailed instructions at http://github.com/anti1869/%s",\n\t"nodename":"%s",\n\t"report-host":"%s",\n\t"data-dir":"%s",\n\t"groups":[]\n}' % (nodemon.PACKAGE_NAME.lower(), node_name, report_host, data_dir)
	if report_host_auth_username != '':
		config = config.replace('"data-dir"','"report-host-auth":["%s","%s"],\n\t"data-dir"' % (report_host_auth_username, report_host_auth_password))
	with open(config_filename, 'w') as f:
			f.write(config)	
			
	print "\nOK. Hey, listen. You need to set up what you want to monitor in that config file."
	print "Check out detailed instructions at http://github.com/anti1869/%s" % (nodemon.PACKAGE_NAME.lower())
	if install_web:
		print "\nYou also need to configure your webserver to host %s web interface" % nodemon.PACKAGE_NAME
		print "The instructions are on the same page."
	