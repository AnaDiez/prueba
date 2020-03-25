#!/usr/bin/python3

import subprocess
import sys
import json
import csv
import imp
import os
from xml.dom.minidom import parseString

# Logging init
FILE_LOGS = '/app/logging/log/metadatos.privapp.log'
HELPER_JSON_LOGGER = '/app/logging/agent/helper/log.py'

# configure json logger
assert os.path.isfile(HELPER_JSON_LOGGER), '%s  is not a valid file or path to file' % HELPER_JSON_LOGGER
log = imp.load_source('log', HELPER_JSON_LOGGER)
logger = log.init_logger(FILE_LOGS)

def extractPermissions(app_name, version, testing_label):
	try:
		logger.info('Permissions - Extracting', extra={'apk': app_name, 'version': version, 'container': 'metadatos'})
		data = ''
		w = open('results/{}/filePermissions.csv'.format(app_name),"w")
		with open('permissions-es.json') as file_object:
			permisos = json.load(file_object)
			
		with open('results/{}/filesExtracted/AndroidManifest.xml'.format(app_name),'r') as f:
		    data = f.read()

		dom = parseString(data)

		file = csv.writer(w)

		requiredPermissions = dom.getElementsByTagName('uses-permission')
		file.writerow(["type_permission", "permission_name", "protection_level"])
		for permission in requiredPermissions:
			if permisos["permissions"].get(permission.getAttribute('android:name')) != None and permisos["permissions"][permission.getAttribute('android:name')].get("protection_level") != None:
				file.writerow(["required", permission.getAttribute('android:name'),permisos["permissions"][permission.getAttribute('android:name')]["protection_level"]])
				logger.info('results', extra={
					'apk': app_name, 
					'version': version, 
					'container': 'metadatos',
					'data':{
						'type_permission':'required',
						'permission_name': permission.getAttribute('android:name'),
						'protection_level': permisos["permissions"][permission.getAttribute('android:name')]["protection_level"]
						}
					})
			else:
				file.writerow(["required", permission.getAttribute('android:name'), '-'])
				logger.info('results', extra={
					'apk': app_name, 
					'version': version, 
					'container': 'metadatos',
					'data':{
						'type_permission':'required',
						'permission_name': permission.getAttribute('android:name'),
						'protection_level': '-'
						}
					})

		declaredPermissions = dom.getElementsByTagName('permission')
		for permission in declaredPermissions:
			file.writerow(["declared", permission.getAttribute('android:name'), permission.getAttribute('android:protectionLevel')])
			logger.info('results', extra={
					'apk': app_name, 
					'version': version, 
					'container': 'metadatos',
					'data':{
						'type_permission':'declared',
						'permission_name': permission.getAttribute('android:name'),
						'protection_level': permission.getAttribute('android:protectionLevel')
						}
					})
	except Exception as e:
		logger.warn('Permissions - Error while extracting results from manifest:{}'.format(e.strerror),extra={'apk': app_name, 'version': version, 'container': 'metadatos'})
		print("Permissions - Error while extracting results from manifest")
	else:
		logger.info('Permissions - Extracting DONE', extra={'apk': app_name, 'version': version, 'container': 'metadatos'})
		print("Permissions - Extracting DONE")

if __name__ == "__main__":
    extractPermissions(sys.argv[1], sys.argv[2], sys.argv[3])