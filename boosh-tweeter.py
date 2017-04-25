#!/usr/bin/env python3
import tweepy
import requests
from twitterkeys import *

USER = "booshfm"
CURRENT_URL = "http://boosh.fm/current"

# OAUTH2 Keys, imported from twitterkeys
"""
API_KEY = ''
API_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_SECRET = ''
"""

def get_current(url):
    r = requests.get(url)
    return(r.text)

def get_last_tweet(api):
    tweet = api.user_timeline(id = USER, count = 1)[0]
    return(tweet.text)


def get_api(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)

def main():
    cfg = {
    "consumer_key": API_KEY,
    "consumer_secret": API_SECRET,
    "access_token": ACCESS_TOKEN,
    "access_token_secret": ACCESS_SECRET
    }

    api = get_api(cfg)
    current = get_current(CURRENT_URL)
    if "Live: " in current and len(current) > 7:
        last = get_last_tweet(api)
        if current in last:
            pass
        else:
            print("Updating Twitter with: %s" % current)
            api.update_status(status="%s Listen now: http://boosh.fm" % current)
    else:
        pass

if __name__ == "__main__":
  main()