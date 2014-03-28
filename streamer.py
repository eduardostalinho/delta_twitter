# -*- coding: utf-8 -*-
import logging
from datetime import date
from pprint import pprint

from twython import Twython, TwythonStreamer
from coopy.base import init_persistent_system

try:
    from settings import *
except ImportError:
    KEY = 'PUT_YOUR_KEY_HERE'
    SECRET = 'PUT_YOUR_SECRET_HERE'
    TOKEN = 'GET_YOURSELF_A_TOKEN'
    TOKEN_SECRET = 'GET_YOURSELF_A_SECRET'
    HASHTAG = 'YOUT_HASHTAG'

twitter = Twython(KEY, SECRET, TOKEN, TOKEN_SECRET)

class UserRepo(object):
    def __init__(self, *args, **kwargs):
        self.users = []
        self.relations = []

    def add_user(self, user_id):
        user = {
            str(user_id):  {
                'screen_name': twitter.show_user(user_id=user_id)['screen_name'],
                'followers': []
            }
        }

        next_cursor = -1
        while 'next_cursor' != 0:
            req = twitter.get_followers_ids(user_id=user_id, next_cursor=next_cursor)
            user['followers'].append(req['ids'])
            next_cursor = req['next_cursor']

        if user_id in self.users:
            self.users.append(user)
        else:
            self.users[str(user_id)]

        for saved_user in self.users:
            if user_id in saved_user['followers']:
                self.relations.append((user_id, saved_user))


user_repo = init_persistent_system(UserRepo)

class HashtagStreamer(TwythonStreamer):
    def on_success(self, data):
        hashtags = [ x.get('text') for x in data.get('entities', {}).get('hashtags', []) ]
        if HASHTAG in hashtags:
            user_id = data.get('user', {}).get('id')
            user_repo.add_user(user_id)

    def on_error(self, status, data):
        print status, data


stream = HashtagStreamer(KEY, SECRET, TOKEN, TOKEN_SECRET)
stream.statuses.filter(track=HASHTAG)
