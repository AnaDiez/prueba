# ############################################################################
#                            STORAGE API APPERS
#############################################################################

import requests
import json
class Storage:
    def __init__(self, server, port, app, version):
        self.server = server
        self.port = port
        self.app = app
        self.version = version

    def version(self):
        data = {}
        try:
            res = requests.get('http://{}:{}/app/versioncode/{}'.format(self.server, self.port, self.app))
            data = res.text
            data = data[data.find("[")+1:data.find("]")]
        except Exception as e:
            data = "-1"
        finally:
            return data

    def apk(self, folder=None):
        #version = self.version()
        res = requests.get('http://{}:{}/app/apk/{}/{}'.format(self.server, self.port, self.app, self.version), stream=True)
        if folder is not None:
                with open('{}/{}.apk'.format(folder, self.app), 'wb') as f:
                    for chunk in res.iter_content(chunk_size=128):
                        f.write(chunk)
        return '{}/{}.apk'.format(folder, self.app, self.app)
# tests

#t = Storage("192.168.1.201", "5000", "com.baselayoutsforcoc")
#print(t.version())
#t.apk(".")