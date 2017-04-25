#!/usr/bin/env python3
import facebook
import requests
import os
from facebookkeys import *

CURRENT_URL = "http://stream.boosh.fm/current"
IMAGES = "/images/"
debug = True

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

def get_previous(api, cfg):
    try:
        posts = api.get_connections(cfg['page_id'], 'posts?limit=1')
        last_post = posts['data'][0]['message']
    except:
        print("Couldn't get last post for page id: %s" % cfg['page_id'])

    return last_post

def get_current(url):
    r = requests.get(url)
    return(r.text)

def main():
    cfg = {
    "page_id"      : page_id,
    "access_token" : access_token
    }

    api = facebook.GraphAPI(cfg['access_token'])
    current = get_current(CURRENT_URL).rstrip()

    if "Live: " in current and len(current) > 7:
        last = get_previous(api, cfg)
        if current in last:
            pass
        else:
            if debug:
                print("Updating Facebook with: %s" % current)
            file = find_image(current)
            if file is not None:
                if debug:
                    print("Found image: %s" % file)
                image = open(file, "rb")
                message = current + "\nListen now: Boosh.FM"
                api.put_photo(message=message,
                               image=image.read())
                image.close()
            else:
                if debug:
                    print("No image found for show: %s" % current)
                api.put_wall_post("%s \nListen now: Boosh.FM" % current)
    else:
        pass


if __name__ == "__main__":
    main()
