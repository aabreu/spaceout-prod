from django.core.files.storage import Storage
from django.core.files import File
from django.conf import settings
from django.utils.deconstruct import deconstructible

import requests

@deconstructible
class IBMObjectStorage(Storage):

    token_url = 'https://identity.open.softlayer.com/v3/auth/tokens'
    token = ''
    api_url = "https://dal.objectstorage.open.softlayer.com/v1/AUTH_%s/%s/%s"
    # https://<access point>/<API version>/AUTH_<project ID>/<container namespace>/<object namespace>

    def __init__(self, option=None):
        pass
        # self.token = self.get_token()
        # self.config_container()

    def _open(self, name, mode='rb'):
        assert mode == 'rb', "You've tried to open binary file without specifying binary mode! You specified: %s"%mode

    def _save(self, name, content):
        url = self.url(name)
        headers = {'X-Auth-Token':self.token, 'Content-Type':'application/octet-stream'}
        r = requests.put(url, data=content, headers=headers)
        return name

    def exists(self, name):
        url = self.url(name)
        headers = {'X-Auth-Token':self.token}
        r = requests.get(url, headers=headers)
        return r.status_code == 200

    def delete(self, name):
        url = self.url(name)
        headers = {'X-Auth-Token':self.token}
        r = requests.delete(url, headers=headers)

    def url(self, name):
        return self.api_url % (settings.OBJECT_STORAGE_PROJECT_ID, settings.OBJECT_STORAGE_CONTAINER, name)

    def get_token(self):
        data = """
            {"auth":
                {
                    "identity":{
                        "methods":["password"],
                        "password":{
                            "user":{
                                "id":"%s",
                                "password":"%s"
                            }
                        }
                    },
                    "scope":{
                        "project":{
                            "id":"%s"
                        }
                    }
                }
            }"""

        data = data % (settings.OBJECT_STORAGE_USER_ID, settings.OBJECT_STORAGE_PASSWORD, settings.OBJECT_STORAGE_PROJECT_ID)
        headers = {'Content-Type': 'application/json'}
        r = requests.post(self.token_url, data=data, headers=headers)
        return r.headers['X-Subject-Token']

    def config_container(self):
        headers = {'X-Container-Read':'.r:*', 'X-Auth-Token':self.token}
        url = self.api_url % (settings.OBJECT_STORAGE_PROJECT_ID, settings.OBJECT_STORAGE_CONTAINER, "")
        r = requests.post(url, headers=headers)
