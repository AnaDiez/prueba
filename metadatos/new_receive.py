#!/usr/bin/env python
import pika
import sys
import time
import os
import configparser
import imp
import threading
import subprocess 
import functools
import json
import staticMetadatos as st
import apy_storage as astr

BASE_PATH = None
FILE_LOGS = None
HELPER_JSON_LOGGER = None

RABBIT_PASSWORD = None
RABBIT_USERNAME = None
RABBIT_SERVER = None
RABBIT_PORT = 5672
RABBIT_QUEUE = None
RABBIT_EXCHANGE = None

TESTING_SERVER = None
TESTING_PORT = None
TESTING_LABEL = None

STORAGE_SERVER = None
STORAGE_PORT = None

log = None

def parse_config(config_file):
    global BASE_PATH, FILE_LOGS, HELPER_JSON_LOGGER, logger,log, RABBIT_PASSWORD, RABBIT_USERNAME, RABBIT_EXCHANGE, RABBIT_QUEUE, RABBIT_SERVER, TESTING_SERVER, TESTING_PORT, TESTING_LABEL, STORAGE_SERVER, STORAGE_PORT
    assert os.path.isfile(config_file), '%s is not a valid file or path to file' % config_file

    config = configparser.ConfigParser()
    config.read(config_file)

    assert 'base' in config.sections(), 'Config file %s does not contain an base section' % config_file
    assert 'base_path' in config[
        'base'], 'Config file %s does not have an ADBPath value in the sdk section' % config_file
    BASE_PATH = config['base']['base_path']
    assert os.path.isdir(BASE_PATH), 'directory %s not valid' % BASE_PATH
    FILE_LOGS = os.path.join(BASE_PATH, 'logging/log/metadatos.privapp.log')
    HELPER_JSON_LOGGER = os.path.join(BASE_PATH, 'logging/agent/helper/log.py')
    assert os.path.isfile(HELPER_JSON_LOGGER), '%s  is not a valid file or path to file' % HELPER_JSON_LOGGER
    log = imp.load_source('log', HELPER_JSON_LOGGER)
    logger = log.init_logger(FILE_LOGS)


    assert 'rabbitmq' in config.sections(), 'Config file %s does not contain an rabbitmq section' % config_file
    assert 'username' in config[
        'rabbitmq'], 'Config file %s does not have an username value in the rabbitmq section' % config_file
    assert 'password' in config[
        'rabbitmq'], 'Config file %s does not have an password value in the rabbitmq section' % config_file
    assert 'queue' in config[
        'rabbitmq'], 'Config file %s does not have an queue value in the rabbitmq section' % config_file
    assert 'exchange' in config[
        'rabbitmq'], 'Config file %s does not have an exchange value in the rabbitmq section' % config_file
    assert 'server_ip' in config[
        'rabbitmq'], 'Config file %s does not have an server ip value in the rabbitmq section' % config_file
    assert 'server_ip' in config[
        'testing'], 'Config file %s does not have an server ip value in the testing section' % config_file
    assert 'server_port' in config[
        'testing'], 'Config file %s does not have an server port value in the testing section' % config_file
    assert 'testing_label' in config[
        'testing'], 'Config file %s does not have a testing label value in the testing section' % config_file
    assert 'server_ip' in config[
        'storage'], 'Config file %s does not have a server ip value in the storage section' % config_file
    assert 'server_port' in config[
        'storage'], 'Config file %s does not have a server port value in the storage section' % config_file

    RABBIT_PASSWORD = config['rabbitmq']['password']
    RABBIT_USERNAME = config['rabbitmq']['username']
    RABBIT_QUEUE = config['rabbitmq']['queue']
    RABBIT_EXCHANGE = config['rabbitmq']['exchange']
    RABBIT_SERVER = config['rabbitmq']['server_ip']
    TESTING_SERVER = config['testing']['server_ip']
    TESTING_PORT = config['testing']['server_port']
    TESTING_LABEL = config['testing']['testing_label']
    STORAGE_SERVER = config['storage']['server_ip']
    STORAGE_PORT = config['storage']['server_port']

def ack_message(channel, delivery_tag):
    if channel.is_open:
        channel.basic_ack(delivery_tag)
    else:
        logger.warn('Ack cannot be delivered')

def testing(connection, channel, delivery_tag, body):
    print(" [x] Received {}".format(body.decode('utf-8')))
    print(" [x] Started app analysis {}".format(body.decode('utf-8')))

    # #Con modulo de almacenamiento
    # try:
    #     storage_server_ip = STORAGE_SERVER
    #     storage_server_port = STORAGE_PORT
    #     body_json = json.loads(body)
    #     print(type(body_json))
    #     app = body_json['apk']
    #     print('app:{}'.format(app))
    #     version = body_json['version']
    #     print('version:{}'.format(version))
    #     t = astr.Storage(STORAGE_SERVER, STORAGE_PORT, app, version)
    #     apk_path = t.apk('files')
    #     i = self.apk_path.rfind("/")
    #     l = len(self.apk_path)
    #     app_name = self.apk_path[i+1:l-4]
    # except Exception as e:
    #     logger.warn("Couldn't get the apk", extra={'apk': body})
    # else:
    #     logger.info("Apk recovered", extra={'apk': app_name, 'version': version})


    #Sin modulo de almacenamiento
    body_json = json.loads(body)
    try:
        body_json = json.loads(body)
    except Exception as e:
        print(e)
    else:
        app = body_json['apk']
        version = body_json['version']
        apk_path = "files/{}".format(app)
        print(apk_path)
  

    server_port = TESTING_PORT
    server_ip = TESTING_SERVER
    testing_label = TESTING_LABEL
    s = st.Static_Testing(server_ip, server_port, apk_path, version, testing_label)
    s.extractApk()
    s.certInfo()
    s.extractPermissions()
    s.hashes()
    s.nativeCode()

    log.stop_logger()
    cb = functools.partial(ack_message, channel, delivery_tag)
    connection.add_callback_threadsafe(cb)    
    print(" [x] Removed app from queue {}".format(body.decode('utf-8')))

def on_message(channel, method_frame, header_frame, body, args):
    (connection, threads) = args
    delivery_tag = method_frame.delivery_tag
    th = threading.Thread(target=testing, args=(connection, channel, delivery_tag, body))
    th.start()
    threads.append(th)

def main():
        receive()

def receive():
    cwd = os.path.dirname(os.path.abspath(sys.argv[0]))
    parse_config(os.path.join(cwd, 'metadatos.config'))
    
    (success, result) = call_sh('service filebeat start')
    if not success:
        logger.error('Filebeat start failed: {}'.format(result)) 
    else: 
        logger.debug('Filebeat agent started successfully')
    
    credentials = pika.PlainCredentials(RABBIT_USERNAME, RABBIT_PASSWORD)
    parameters = pika.ConnectionParameters(RABBIT_SERVER, RABBIT_PORT, credentials=credentials, heartbeat=5)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.exchange_declare(exchange=RABBIT_EXCHANGE, exchange_type="fanout", passive=False, durable=True, auto_delete=False)
    result = channel.queue_declare(queue='', exclusive=True)
    channel.queue_bind(queue=result.method.queue, exchange=RABBIT_EXCHANGE)
    channel.basic_qos(prefetch_count=1)
    threads = []
    on_message_callback = functools.partial(on_message, args=(connection, threads))
    channel.basic_consume(on_message_callback=on_message_callback, queue=result.method.queue)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

    for thread in threads:
        thread.join()

    connection.close()

def call_sh(command, timeout_secs=10):
    result = None
    success = True
    try:
        #result = subprocess.run(command, timeout=timeout_secs, shell=True, check=True, stderr=subprocess.STDOUT)
        result = subprocess.call(command, shell=True)
        print(result)
    except Exception as e:
        result = str(e)
        success = False
    return (success, result)

if __name__== "__main__":
        main()
