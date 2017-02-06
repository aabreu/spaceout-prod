from spaceoutvr.models import SpaceoutUser

from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

import hashlib
import hmac
import json
import requests
import random
import time


class TwitterBackend(object):
    def authenticate(self, access_token=None, access_token_verif=None):

        print("twitter login token(%s) secret(%s)" % (access_token, access_token_verif))

        headers = {
            "oauth_token":access_token,
            "oauth_token_secret": access_token_verif,
            "oauth_consumer_key": "cHPRQDwbhBrIe08Q3JXgRMOks",
            "oauth_consumer_key_secret":"lu1VmkykWA6taqiRbybRbzDKsYYhx7CIeSb8lxrkUlnzlr10o0",
            "oauth_version": "1.0",
            #  Just a simple implementation of a random number between 123400 and 9999999
            "oauth_nonce": "%s" % random.randrange(123400, 9999999),
            "oauth_timestamp": "%s" % time.time(),
            "oauth_signature_method": "HMAC-SHA1"
            "oauth_signature": "OAuth realm=\"Twitter API\""
        }

        print("headers %s" % headers)

        url = "https://api.twitter.com/1.1/account/verify_credentials.json"
        r = requests.get(url, headers=headers)
        data = r.json()

        print(data)
