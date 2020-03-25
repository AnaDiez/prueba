#!/usr/bin/python3

import sys
import hashlib
import csv
import os
import imp

# Logging init
FILE_LOGS = '/app/logging/log/metadatos.privapp.log'
HELPER_JSON_LOGGER = '/app/logging/agent/helper/log.py'

# configure json logger
assert os.path.isfile(HELPER_JSON_LOGGER), '%s  is not a valid file or path to file' % HELPER_JSON_LOGGER
log = imp.load_source('log', HELPER_JSON_LOGGER)
logger = log.init_logger(FILE_LOGS)

def extractHashes(apk_path,app_name, version, testing_label):
    try:
        logger.info('Hases - Generating hashes', extra={'apk': app_name, 'version': version, 'container':'metadatos'})
        hash_md5 = hashlib.md5()
        with open(apk_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                        hash_md5.update(chunk)
        md5 = hash_md5.hexdigest()
        
        hash_sha1 = hashlib.sha1()
        with open(apk_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                        hash_sha1.update(chunk)
        sha1 = hash_sha1.hexdigest()

        hash_sha256 = hashlib.sha256()
        with open(apk_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                        hash_sha256.update(chunk)
        sha256 = hash_sha256.hexdigest()
        
        w = open('results/{}/hashes.csv'.format(app_name),"w")
        file = csv.writer(w)
        file.writerow(["md5", "sha1", "sha256"])
        file.writerow([md5, sha1, sha256])
        logger.info('results', extra={
            'apk': app_name,
            'version': version, 
            'container':'metadatos',
            'data':{
                'md5': md5,
                'sha1':sha1,
                'sha256': sha256
                }
            })
    except Exception as e:
        logger.warn('Hases - Error while generating hashes: {}'.format(e.strerror), extra={'apk': app_name, 'version': version, 'container':'metadatos'})
    else:
        logger.info('Hashes - Generating DONE', extra={'apk': app_name,'version': version, 'container':'metadatos'})

if __name__ == "__main__":
    extractHashes(sys.argv[1], sys.argv[2], sys.argv[3],sys.argv[4])
