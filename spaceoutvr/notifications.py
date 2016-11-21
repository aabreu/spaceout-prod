from django.conf import settings

import requests

class OneSignalNotifications:

    def send(self, ids):
        url = "https://onesignal.com/api/v1/notifications"

        data = """{
            "include_player_ids":["%s"],
            "app_id": "%s",
            "headings":{"en": "***** TITLE *****"},
            "contents":{"en": "***** BODY *****"},
            "url":"spaceoutvr://notification/"
        }"""

        data = data % (ids, settings.ONESIGNAL_APP_ID)

        print(data)

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": "Basic %s" % settings.ONESIGNAL_API_KEY
        }

        print(headers)

        r = requests.post(url, data=data, headers=headers)

        print(r)
        for k in r:
            print k
