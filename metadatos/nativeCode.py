#!/usr/bin/python3

import csv
import os
import sys
import imp

# Logging init
FILE_LOGS = '/app/logging/log/metadatos.privapp.log'
HELPER_JSON_LOGGER = '/app/logging/agent/helper/log.py'

# configure json logger
assert os.path.isfile(HELPER_JSON_LOGGER), '%s  is not a valid file or path to file' % HELPER_JSON_LOGGER
log = imp.load_source('log', HELPER_JSON_LOGGER)
logger = log.init_logger(FILE_LOGS)

def nativeCode(app_name, version, testing_label):	
	try:
		logger.info('NativeCode - Searching ', extra={'apk': app_name, 'version': version, 'container': 'metadatos'})
		file = open("results/{}/native_code.csv".format(app_name), 'w')
		w = csv.writer(file)

		w.writerow(["files in /libs"])
		# Escribir en el fichero las librerias dentro de la carpeta libs
		path = "results/{}/filesExtracted/lib".format(app_name)
		if os.path.exists(path):
			nodes = os.listdir(path) 
			files = {}
			for node in nodes:
				if os.path.isdir(join(path, node)):
					files = os.listdir(join(path, node))
					for file in files:
						w.writerow([file])
						logger.info('results',extra={
							'apk': app_name, 
							'version': version, 
							'container': 'metadatos',
							'data':{
								'files in /libs': file
							}})
				elif os.path.isfile(join(path, node)):
					w.writerow([node])
					logger.info('results',extra={
							'apk': app_name, 
							'version': version, 
							'container': 'metadatos',
							'data':{
								'files in /libs': node
							}})
		else:
			w.writerow(["None"])
			logger.info('results',extra={
							'apk': app_name, 
							'version': version, 
							'container': 'metadatos',
							'data':{
								'files in /libs': 'None'
							}})
	except Exception as e:
	 	logger.warn('NativeCode - Error while searching results: {}'.format(e.strerror), extra={'apk': app_name, 'version': version, 'container': 'metadatos'})
	else:
		logger.info('NativeCode - DONE', extra={'apk': app_name, 'version': version, 'container': 'metadatos'})

if __name__ == "__main__":
    nativeCode(sys.argv[1], sys.argv[2], sys.argv[3])
