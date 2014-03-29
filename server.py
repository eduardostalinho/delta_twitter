# -*- coding: utf-8 -*-
from twython import Twython
from flask import Flask, jsonify
from coopy.base import init_persistent_system

from domain import UserRepo
from streamer import HashtagStreamer

try:
    from settings import *
except ImportError:
    KEY = 'PUT_YOUR_KEY_HERE'
    SECRET = 'PUT_YOUR_SECRET_HERE'
    TOKEN = 'GET_YOURSELF_A_TOKEN'
    TOKEN_SECRET = 'GET_YOURSELF_A_SECRET'
    HASHTAG = 'YOUR_HASHTAG'

user_repo = init_persistent_system(UserRepo())
app = Flask(__name__)

@app.route('/graph.json')
def retrieve_graph():
    response = user_repo.retrieve_as_graph()
    return jsonify(**response)


if __name__ == '__main__':
    app.run(debug=True)

twitter = Twython(KEY, SECRET, TOKEN, TOKEN_SECRET)
stream = HashtagStreamer(HASHTAG, user_repo, twitter, KEY, SECRET, TOKEN, TOKEN_SECRET)
stream.statuses.filter(track=['#' + HASHTAG])
