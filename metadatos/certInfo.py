#!/usr/bin/python3

import subprocess
import sys
import glob
import imp
import os

# Logging init
FILE_LOGS = '/app/logging/log/metadatos.privapp.log'
HELPER_JSON_LOGGER = '/app/logging/agent/helper/log.py'

# configure json logger
assert os.path.isfile(HELPER_JSON_LOGGER), '%s  is not a valid file or path to file' % HELPER_JSON_LOGGER
log = imp.load_source('log', HELPER_JSON_LOGGER)
logger = log.init_logger(FILE_LOGS)

def extractCertInfo(app_name, version, testing_label):
    result = None
    propietario = None
    emisor = None
    numSerie = None
    validez = None
    sha1 = None
    sha256 = None
    algFirma = None
    algClavePub = None
    versionCert = None

    pattern_ = "results/{}/filesExtracted/original/META-INF/".format(app_name) + "*.RSA"
    cert = glob.glob(pattern_)
    try:
        logger.info('Keytool - Extracting cert info', extra={'apk': app_name, 'version':version, 'container': 'metadatos'})

        with open("results/{}/certInfo.txt".format(app_name), 'w') as f:
			result = subprocess.call("keytool -printcert -v -file {}".format(cert[0]), stdout=f, shell = True)

        with open("results/{}/certInfo.txt".format(app_name), 'r') as c:
            for l in c.readlines():
                if "Propietario:" in l:
                    propietario = l[15:]
                if "Owner:" in l:
                    propietario = l[7:]
                if "Emisor:" in l:
                    emisor = l[10:]
                if "Issuer:" in l:
                    emisor = l[8:]
                if "mero de serie:" in l:
                    numSerie = l[18:]
                if "Serial number:" in l:
                    numSerie = l[15:]
                if "lido desde:" in l:
                    validez = l[15:42]+" -"+l[51:]
                if "Valid from:" in l:
                    validez = l[12:40]+" -"+l[48:]
                if "SHA1:" in l:
                    sha1 = l[15:]
                if "SHA256:" in l:
                    sha256 = l[17:]
                if "Nombre del algoritmo de firma:" in l:
                    algFirma = l[31:]
                if "Signature algorithm name:" in l:
                    algFirma = l[26:]
                if "Subject Public Key Algorithm:" in l:
                    algClavePub =l[30:]
                if "Version:" in l:
                    versionCert =l[9:]
        logger.info('results', extra={
            'apk': app_name, 
            'version':version, 
            'data': {
                'propietario': propietario.replace("\n", ""),
                'emisor': emisor.replace("\n", ""),
                'numSerie': numSerie.replace("\n", ""),
                'validez': validez.replace("\n", ""),
                'sha1': sha1.replace("\n", ""),
                'sha256': sha256.replace("\n", ""),
                'algFirma': algFirma.replace("\n", ""),
                'algClavePub': algClavePub.replace("\n", ""),
                'version': versionCert.replace("\n", ""),
                }
            })
    except Exception as e:
        result = str(e)
        logger.warn('Keytool - Error while exctracting cert info: {}'.format(result), extra={'apk': app_name, 'version':version, 'container':'metadatos'})
    else:
		logger.info('Keytool - Cert info extracted', extra={'apk': app_name, 'version':version, 'container':'metadatos'})

if __name__ == "__main__":
    extractCertInfo(sys.argv[1], sys.argv[2], sys.argv[3])
