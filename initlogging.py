'''
Created on Nov 12, 2010

@author: jtk
'''

import logging

def initFileLogger(logfile):
    logging.basicConfig(filename=logfile, filemode='w',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='[%d-%m-%Y %H:%M:%S]',
                        level=logging.DEBUG)

    # create console handler and add it to the existing handler
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s %(name)s: %(levelname)s - %(message)s", '[%d/%b/%Y %H:%M:%S]')
    console.setFormatter(formatter)

    logging.getLogger('').addHandler(console)
