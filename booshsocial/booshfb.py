import html
import facebook
import os
from facebookkeys import cfg
from config import *

def get_last_fb(api):
    try:
        posts = api.get_connections(cfg['page_id'], 'posts?limit=1')
        last_post = posts['data'][0]['message']
        last_post = html.unescape(last_post)
    except:
        print("Couldn't get last Facebook post for page id: %s" % cfg['page_id'])
        last_post = None
    return(last_post)

def check_facebook(current, show):
    api = facebook.GraphAPI(cfg['access_token'])
    last = get_last_fb(api)
    if last is not None and current in last:
        pass
    else:
        if debug:
            print("Updating Facebook with: %s" % current)
        message = current + "\nListen now: Boosh.FM"

        if show is not None and show['tags'] is not None:
            message = message + "\n"
            for tag in show['tags']:
                message = message + " #" + tag.replace(' ', '')

        if show is not None and show['picturefile'] is not None:
            filename = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + IMAGES + show['picturefile']
            try:
                image = open(filename, "rb")
                api.put_photo(message=message,
                              image=image.read())
                image.close()
            except:
                print("Couldn't open image file: %s" % filename)
                api.put_wall_post(message)
        else:
            if debug:
                print("No image found for show: %s" % current)
            api.put_wall_post(message)