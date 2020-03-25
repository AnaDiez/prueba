#!/usr/bin/python3

import sys
import os
import imp


# Logging init
FILE_LOGS = '/app/logging/log/metadatos.privapp.log'
HELPER_JSON_LOGGER = '/app/logging/agent/helper/log.py'

# configure json logger
assert os.path.isfile(HELPER_JSON_LOGGER), '%s  is not a valid file or path to file' % HELPER_JSON_LOGGER
log = imp.load_source('log', HELPER_JSON_LOGGER)
logger = log.init_logger(FILE_LOGS)


def extractApk(apk_path, app_name, version, testing_label):
    try:
        logger.info('Apktool - Extracting apk', extra={'apk': app_name, 'version':version, 'testing_label': testing_label})
        os.system('apktool d -f -s {} -o results/{}/filesExtracted'.format(apk_path, app_name))
    except Exception as e:
        logger.warn('Apktool - Error while extracting apk: {}'.format(e.strerror), extra={'apk': app_name, 'version':version, 'testing_label': testing_label})
        print("Error while extracting apk")
    else:
        logger.info('Apktool - Apk extracted', extra={'apk': app_name, 'version':version, 'testing_label': testing_label})
        print("Apk extracted")

if __name__ == "__main__":
    extractApk(sys.argv[1],sys.argv[2], sys.argv[3], sys.argv[4])