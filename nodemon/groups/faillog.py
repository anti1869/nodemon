# -*- coding: utf-8 -*-

#
# Faillog group support
# Created 30.12.2014
# Author: Dmitry Litvinenko <anti1869@gmail.com>
#

import os, sys
import glob
from datetime import datetime, timedelta


def tail(f, lines=20 ):
	""" http://stackoverflow.com/questions/136168/get-last-n-lines-of-a-file-with-python-similar-to-tail  """
	total_lines_wanted = lines
	BLOCK_SIZE = 1024
	f.seek(0, 2)
	block_end_byte = f.tell()
	lines_to_go = total_lines_wanted
	block_number = -1
	blocks = [] # blocks of size BLOCK_SIZE, in reverse order starting
				# from the end of the file
	while lines_to_go > 0 and block_end_byte > 0:
		if (block_end_byte - BLOCK_SIZE > 0):
			# read the last block we haven't yet read
			f.seek(block_number*BLOCK_SIZE, 2)
			blocks.append(f.read(BLOCK_SIZE))
		else:
			# file too small, start from begining
			f.seek(0,0)
			# only read what was not read
			blocks.append(f.read(block_end_byte))
		lines_found = blocks[-1].count('\n')
		lines_to_go -= lines_found
		block_end_byte -= BLOCK_SIZE
		block_number -= 1
	all_read_text = ''.join(reversed(blocks))
	return '\n'.join(all_read_text.splitlines()[-total_lines_wanted:])

def process(config, args):
	""" Get last lines of all faillogs and print them if they are not match success stamp """
	config['fails'] = []
	for faillog_dir in config['dirs']:
		for faillog_file in glob.glob('%s/*.log' % faillog_dir):
			with open(faillog_file, 'r') as f:
				last_update = datetime.fromtimestamp(os.path.getmtime(faillog_file))
				if config['success_stamp'] not in tail(f, 1) or ('rotten' in config and last_update < datetime.today() - timedelta(**config['rotten'])):
					config['fails'].append({"file":faillog_file, "last-update":last_update, "tail":tail(f,20)})
	return config