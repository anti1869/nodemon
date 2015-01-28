import re

PACKAGE_NAME = "Nodemon"

def get_version():
	return '0.2.0-beta.2'

__version__ = get_version()
mysql_allowed = re.compile('[0-9a-zA-Z_$]+')

def safe_sql_identifier(string, validation_re = mysql_allowed):
	""" Return injection-free MySQL identifier """
	return "".join(validation_re.findall(string))