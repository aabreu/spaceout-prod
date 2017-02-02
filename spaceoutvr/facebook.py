from spaceoutvr.models import SpaceoutUser

from django.conf import settings

import hashlib
import hmac
import json
import requests


class FacebookBackend(object):
    def authenticate(self, access_token=None):
        data = self.get_token_data(access_token)
        fb_email = data['email']
        try:
            existing_user = SpaceoutUser.objects.get(email=fb_email)
            return existing_user
        except SpaceoutUser.DoesNotExist:
            return None

    def get_user(self, email):
        try:
            return SpaceoutUser.objects.get(email=email)
        except SpaceoutUser.DoesNotExist:
            return None

    def signup(self, email, spacer_name, facebook_id):
        new_user = SpaceoutUser.objects.create_user(email=email, user_name=spacer_name)
        new_user.is_verified = True
        new_user.facebook_id = facebook_id
        new_user.save()
        return new_user

    def get_token_data(self, access_token):
        # app secret proof
        h = hmac.new (
            settings.FACEBOOK_SECRET.encode('utf-8'),
            msg = access_token.encode('utf-8'),
            digestmod = hashlib.sha256
        )
        appsecret_proof = h.hexdigest()

        # make sure token is valid
        api_call = "https://graph.facebook.com/me/?access_token=%s&appsecret_proof=%s&fields=id,name,email" % (access_token, appsecret_proof)
        r = requests.get(api_call)
        data = r.json()
        return data
