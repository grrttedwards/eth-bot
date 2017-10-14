import requests

class Pushbullet:
    PUSH_URL = 'https://api.pushbullet.com/v2/pushes'

    def __init__(self, api_key):
        self.api_key = api_key

    def push_note(self, title, body):
        headers = {
            'Access-Token': self.api_key
        }
        data = {
            'type': 'note',
            'title': title,
            'body': body
        }
        r = requests.post(Pushbullet.PUSH_URL, data=data, headers=headers)
        print(data, headers)
        if r.status_code == 401:
            raise InvalidKeyError(r.content)
        elif not r.ok:
            raise PushbulletError(r.content)

class PushbulletError(Exception):
    pass

class InvalidKeyError(PushbulletError):
    pass