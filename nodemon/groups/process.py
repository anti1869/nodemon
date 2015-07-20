# -*- coding: utf-8 -*-

#
# Process availability group support
# Created 06.01.2014
# Author: Dmitry Litvinenko <anti1869@gmail.com>
#

import os


def process(config, args):
    """
    Check that process is running
    """
    processes = []
    processoutput = os.popen("ps -Af").read()
    for title, pattern in config['processes']:
        # It's a simple substring check
        processes.append([title, pattern, pattern in processoutput.decode('utf-8')])
    config['processes'] = processes
    return config