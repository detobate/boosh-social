import tweepy
import html
import os
from twitterkeys import cfg
from config import *

def get_last_tweet(api):
    tweet = api.user_timeline(id = cfg['tw_user'], count = 1)[0]
    return(html.unescape(tweet.text))

def get_tw_api():
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return(tweepy.API(auth))

def check_twitter(current, show):
    api = get_tw_api()
    last = get_last_tweet(api)
    if current in last:
        pass
    else:
        print("Updating Twitter with: %s" % current)
        message = "%s \nListen now: http://boosh.fm" % current
        # Add genre tags from yaml file as Twitter hashtags
        if show is not None and show['tags'] is not None:
            message = message + "\n"
            for tag in show['tags']:
                message = message + " #" + tag.replace(' ', '')
        if show is not None and show['picturefile'] is not None:
            filename = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + IMAGES + show['picturefile']
            try:
                api.update_with_media(filename=filename, status=message)
            except:
                print("Failed to find image file: %s" % filename)
                api.update_status(status=message)
        else:
            api.update_status(status=message)