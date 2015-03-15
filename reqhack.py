import tweepy
import tweepy.binder

import requests as _requests

class requests(object):
    __session = None
    @classmethod
    def Session(cls):
        if cls.__session is None:
            cls.__session = _requests.Session()
            adapter = _requests.adapters.HTTPAdapter(pool_maxsize = 1)
            cls.__session.mount("https://",adapter)
        return cls.__session

tweepy.binder.requests = requests