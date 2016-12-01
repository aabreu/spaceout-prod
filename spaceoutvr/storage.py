from django.core.files.storage import Storage
from django.core.files import File
from django.conf import settings
from django.utils.deconstruct import deconstructible

import requests

from datetime import datetime, timedelta

@deconstructible
class IBMObjectStorage(Storage):

    container = ''
    container_ready = False
    token_url = 'https://identity.open.softlayer.com/v3/auth/tokens'
    token = None
    api_url = "https://dal.objectstorage.open.softlayer.com/v1/AUTH_%s/%s/%s"
    # https://<access point>/<API version>/AUTH_<project ID>/<container namespace>/<object namespace>

    # def __init__(self, option=None):
    #     if settings.SPACEOUT_STORE_COMMENTS:
    #         if not self.container_ready:
    #             self.get_token()
    #             self.config_container()
    #             self.check_token()

    def _open(self, name, mode='rb'):
        pass
        # assert mode == 'rb', "You've tried to open binary file without specifying binary mode! You specified: %s"%mode

    def _save(self, name, content):
        if settings.SPACEOUT_STORE_COMMENTS:
            self.check_token()
            url = self.url(name)
            headers = {'X-Auth-Token':self.token, 'Content-Type':'application/octet-stream'}
            r = requests.put(url, data=content, headers=headers)
        return name

    def exists(self, name):
        if settings.SPACEOUT_STORE_COMMENTS:
            self.check_token()
            url = self.url(name)
            headers = {'X-Auth-Token':self.token}
            r = requests.get(url, headers=headers)
            return r.status_code == 200
        return False

    def delete(self, name):
        if settings.SPACEOUT_STORE_COMMENTS:
            self.check_token()
            url = self.url(name)
            headers = {'X-Auth-Token':self.token}
            r = requests.delete(url, headers=headers)

    def url(self, name):
        if settings.SPACEOUT_STORE_COMMENTS:
            return self.api_url % (settings.OBJECT_STORAGE_PROJECT_ID, self.container, name)
        return ""

    def get_token(self):
        if settings.SPACEOUT_STORE_COMMENTS:
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
            d = r.json()
            self.expires_at = datetime.strptime(d['token']['expires_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
            self.token = r.headers['X-Subject-Token']

    def check_token(self):
        # get token
        if self.token == None:
            self.get_token()
        # config container
        if not self.container_ready:
            self.config_container()
        # renew token
        if self.expires_at - datetime.now() < timedelta(minutes = 1):
            print("REGENERATING TOKEN %s " % (self.expires_at - datetime.now()))
            self.get_token()

    def config_container(self):
        if self.container_ready:
            return
        if self.container == None:
            return
        if settings.SPACEOUT_STORE_COMMENTS:
            # self.check_token()
            print("INITIALIZING CONTAINER %s" % self.container)
            headers = {'X-Container-Read':'.r:*', 'X-Auth-Token':self.token}
            url = self.api_url % (settings.OBJECT_STORAGE_PROJECT_ID, self.container, "")
            r = requests.post(url, headers=headers)
            self.container_ready = r.status_code == 200 or r.status_code == 204


@deconstructible
class CommentsStorage(IBMObjectStorage):
    def config_container(self):
        self.container = settings.OBJECT_STORAGE_COMMENTS_CONTAINER
        super(CommentsStorage, self).config_container()

@deconstructible
class WatsonStorage(IBMObjectStorage):
    def config_container(self):
        self.container = settings.OBJECT_STORAGE_WATSON_CONTAINER
        super(WatsonStorage, self).config_container()
