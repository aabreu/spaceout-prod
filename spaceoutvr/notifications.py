from django.conf import settings

import requests

class OneSignalNotifications:

    def send(self, from_user, to_user):
        url = "https://onesignal.com/api/v1/notifications"

        data = """{
            "include_player_ids":["%s"],
            "app_id": "%s",
            "contents":{"en": "%s made a new comment"},
            "url":"spaceoutvr://notification/",
            "data":{"type":"COMMENT"}
        }"""

        data = data % (
            to_user.notification_id,
            settings.ONESIGNAL_APP_ID,
            from_user.user_name
        )

        print("SENDING NOTIFICATION %s" % data)

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": "Basic %s" % settings.ONESIGNAL_API_KEY
        }

        r = requests.post(url, data=data, headers=headers)

        print("STATUS: %s" % r.status_code)
        print("RESULT: %s" % r.text)

        return r.status_code==200
