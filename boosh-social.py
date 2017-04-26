#!/usr/bin/env python3
import facebook
import tweepy
import requests
import os
from twitterkeys import *
from facebookkeys import *

CURRENT_URL = "http://stream.boosh.fm/current"
IMAGES = "/images/"
TW_USER = "booshfm"
debug = True

def get_current(url):
    r = requests.get(url)
    return(r.text)

def find_image(show):
    show = show.lstrip("Live: ").lower()
    path = os.path.dirname(os.path.abspath(__file__)) + IMAGES + show.rstrip()
    if debug:
        print("Looking for %s.jpg and %s.png" % (path, path))
    if os.path.isfile(path + '.jpg'):
        file = path + '.jpg'
    elif os.path.isfile(path + '.png'):
        file = path + '.png'
    else:
        file = None
    return file

def get_last_fb(api, cfg):
    try:
        posts = api.get_connections(cfg['page_id'], 'posts?limit=1')
        last_post = posts['data'][0]['message']
    except:
        print("Couldn't get last Facebook post for page id: %s" % cfg['page_id'])
    return(last_post)

def get_last_tweet(api):
    tweet = api.user_timeline(id = TW_USER, count = 1)[0]
    return(tweet.text)

def get_tw_api(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return(tweepy.API(auth))

def check_twitter(api, current):
    last = get_last_tweet(api)
    if current in last:
        pass
    else:
        print("Updating Twitter with: %s" % current)
        message = "%s \nListen now: http://boosh.fm" % current
        filename = find_image(current)
        if filename is not None:
            if debug:
                print("Found image: %s" % filename)
            #image = open(filename, "rb")
            api.update_with_media(filename=filename, status=message)
        else:
            api.update_status(status=message)

def check_facebook(api, current, cfg):
    last = get_last_fb(api, cfg)
    if current in last:
        pass
    else:
        if debug:
            print("Updating Facebook with: %s" % current)
        filename = find_image(current)
        if filename is not None:
            if debug:
                print("Found image: %s" % filename)
            image = open(filename, "rb")
            message = current + "\nListen now: Boosh.FM"
            api.put_photo(message=message,
                          image=image.read())
            image.close()
        else:
            if debug:
                print("No image found for show: %s" % current)
            api.put_wall_post("%s \nListen now: Boosh.FM" % current)

def main():
    tw_cfg = {
    "consumer_key": API_KEY,
    "consumer_secret": API_SECRET,
    "access_token": ACCESS_TOKEN,
    "access_token_secret": ACCESS_SECRET
    }
    fb_cfg = {
    "page_id"      : page_id,
    "access_token" : FB_ACCESS_TOKEN
    }

    current = get_current(CURRENT_URL).rstrip()

    if "Live: " in current and len(current) > 7:
        fb_api = facebook.GraphAPI(fb_cfg['access_token'])
        tw_api = get_tw_api(tw_cfg)
        check_twitter(tw_api, current)
        check_facebook(fb_api, current, fb_cfg)
    else:
        pass

if __name__ == "__main__":
  main()