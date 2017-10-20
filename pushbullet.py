import requests
import time


class Pushbullet:
    """Handles communication with Pushbullet"""
    PUSH_URL = 'https://api.pushbullet.com/v2/pushes'
    PUSH_UPDATE_URL = PUSH_URL + '/{iden}'

    def __init__(self, api_key):
        self.api_key = api_key
        self.last_push_iden = None

    def __backoff(self):
        for attempts in range(5):
            # raise the power of exponential backoff
            yield 5**attempts

    def __do_request(self, request_method, url, data=None, headers=None):
        backoff = self.__backoff()
        for attempt in backoff:
            try:
                response = request_method(url, data=data, headers=headers)
            except requests.exceptions.ConnectionError as e:
                print(e)
                print(f'Attempting {attempt}-second backoff...')
                time.sleep(attempt)
            if response.status_code == 401:
                raise InvalidKeyError(response.content)
            elif not response.ok:
                raise PushbulletError(response.content)
            return response

    def do_post(self, url, data, headers):
        """HTTP POST request to Pushbullet"""
        return self.__do_request(requests.post, url=url, data=data, headers=headers)

    def do_delete(self, url, headers):
        """HTTP DELETE request to Pushbullet"""
        return self.__do_request(requests.delete, url=url, headers=headers)

    def push_note(self, title, body):
        """Push a Pushbullet 'note' type object to all devices"""
        headers = {
            'Access-Token': self.api_key
        }
        data = {
            'type': 'note',
            'title': title,
            'body': body,
            'iden': 'gdax-agent'
        }
        if self.last_push_iden:
            # delete the last push with iden=last_push_iden
            self.do_delete(Pushbullet.PUSH_UPDATE_URL.format(iden=self.last_push_iden), headers)
        self.last_push_iden = self.do_post(Pushbullet.PUSH_URL, data, headers).json()['iden']


class PushbulletError(Exception):
    """Exception for any other error communicating with Pushbullet"""
    pass

class InvalidKeyError(PushbulletError):
    """Exception for Pushbullet returning 401 - Unauthorized"""
    pass
