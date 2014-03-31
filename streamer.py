# -*- coding: utf-8 -*-
import logging
from datetime import date
from pprint import pprint

from twython import TwythonStreamer
from coopy.base import init_persistent_system


class HashtagStreamer(TwythonStreamer):

    def __init__(self, hashtag, repo, twitter, *args, **kwargs):
        self.repo = repo
        self.twitter = twitter
        self.hashtag = hashtag

        super(HashtagStreamer, self).__init__(*args, **kwargs)


    def on_success(self, data):
        hashtags = [ x.get('text'.lower()) for x in data.get('entities', {}).get('hashtags', []) ]
        print 'Received tweet!'
        print data
        import ipdb; ipdb.set_trace()
        if self.hashtag.lower() in hashtags:
            user_id = data.get('user', {}).get('id')
            screen_name = data.get('user', {}).get('screen_name')

            followers = []
            next_cursor = -1
            while next_cursor != 0:
                req = self.twitter.get_followers_ids(user_id=user_id, next_cursor=next_cursor)
                followers.append(req['ids'])
                next_cursor = req['next_cursor']

            self.repo.add_user(user_id, screen_name, followers)

    def on_error(self, status, data):
        print status, data
