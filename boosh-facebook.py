#!/usr/bin/env python3
import facebook
import requests
from facebookkeys import *

CURRENT_URL = "http://stream.boosh.fm/current"

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
  current = get_current(CURRENT_URL)

  if "Live: " in current and len(current) > 7:
      last = get_previous(api, cfg)
      if current in last:
          pass
      else:
          print("Updating Facebook with: %s" % current)
          status = api.put_wall_post("%s Listen now: Boosh.FM" % current)
  else:
      pass


if __name__ == "__main__":
  main()
