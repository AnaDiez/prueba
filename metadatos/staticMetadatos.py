
import os 
import sys
import requests
import json


class Static_Testing:
    def __init__(self, server, port, apk_path, version, testing_label):
        self.server = server
        self.port = port
        self.apk_path= apk_path
        self.version = version
        self.testing_label = testing_label
         

    def extractApk(self):
        data = {}
        i = self.apk_path.rfind("/")
        l = len(self.apk_path)
        app = self.apk_path[i+1:l-4]
        print("app name:", app)
        print("apk_path:", self.apk_path)
        print("Servidor:", self.server)
        print("Puerto:", self.port)
        try:
            res = requests.get('http://{}:{}/extractApk'.format(self.server, self.port), params={'app':app, 'apk_path':self.apk_path, 'version':self.version,'testing_label':self.testing_label})
            data = json.loads(res.text)
        except Exception as e:
            data['Ok'] = False
            data['Msg'] = str(e)
        finally:
            return (data['Ok'], data['Msg'])
    
    def hashes(self):
        data = {}
        i = self.apk_path.rfind("/")
        l = len(self.apk_path)
        app = self.apk_path[i+1:l-4]
        try:
            res = requests.get('http://{}:{}/hashes'.format(self.server, self.port), params={'app':app, 'apk_path':self.apk_path, 'version':self.version,'testing_label':self.testing_label})
            data = json.loads(res.text)
        except Exception as e:
            data['Ok'] = False
            data['Msg'] = str(e)
        finally:
            return (data['Ok'], data['Msg'])

    def certInfo(self):
        data = {}
        i = self.apk_path.rfind("/")
        l = len(self.apk_path)
        app = self.apk_path[i+1:l-4]
        try:
            res = requests.get('http://{}:{}/certInfo'.format(self.server, self.port), params={'app':app, 'apk_path':self.apk_path, 'version':self.version, 'testing_label':self.testing_label})
            data = json.loads(res.text)
        except Exception as e:
            data['Ok'] = False
            data['Msg'] = str(e)
        finally:
            return (data['Ok'], data['Msg'])


    def nativeCode(self):
        data = {}
        i = self.apk_path.rfind("/")
        l = len(self.apk_path)
        app = self.apk_path[i+1:l-4]
        try:
            res = requests.get('http://{}:{}/nativeCode'.format(self.server, self.port), params={'app':app, 'apk_path':self.apk_path, 'version':self.version, 'testing_label':self.testing_label})
            data = json.loads(res.text)
        except Exception as e:
            data['Ok'] = False
            data['Msg'] = str(e)
        finally:
            return (data['Ok'], data['Msg'])

    def extractPermissions(self):
        data = {}
        i = self.apk_path.rfind("/")
        l = len(self.apk_path)
        app = self.apk_path[i+1:l-4]
        try:
            res = requests.get('http://{}:{}/extractPermissions'.format(self.server, self.port), params={'app':app, 'apk_path':self.apk_path,'version':self.version, 'testing_label':self.testing_label})
            data = json.loads(res.text)
        except Exception as e:
            data['Ok'] = False
            data['Msg'] = str(e)
        finally:
            return (data['Ok'], data['Msg'])








