#!/usr/bin/env python3
import pyaml, slugify
import mixcloud, requests, sys, os
from mixcloudkeys import *

debug = True
showfile = "shows.yaml"
image_path = "images/"
base_url = 'https://api.mixcloud.com/upload/'

def load_shows(yaml):
    with open(yaml) as shows:
        shows = pyaml.yaml.load(shows)
    return shows


def auth_mixcloud():
    o = mixcloud.MixcloudOauth(
        client_id=client_id, client_secret=client_secret,
        redirect_uri="me")

    url = o.authorize_url()
    if debug:
        print(url)
    access_token = o.exchange_token(code)
    return access_token


def main():
    try:
        mp3file = sys.argv[1]
    except:
        print("You must provide a file to upload: %s <filename>" % (sys.argv[0]))
        exit(1)

    access_token = auth_mixcloud()
    #m = mixcloud.Mixcloud(access_token=access_token)
    path = os.path.dirname(os.path.abspath(__file__)) + "/"
    shows = load_shows(path + showfile)
    try:
        showname = mp3file.rpartition(" - ")[0]  # Raw show name, excluding date
        fullshowname = mp3file.rpartition(".")[0]  # Including date
        showdate = mp3file.rpartition(".")[0].rpartition(" - ")[2]
    except:
        print("Couldn't parse filename: %s" % (mp3file))
        exit(1)
    try:
        int(showdate)
    except:
        print("Couldn't find the show date in the filename")

    for show in shows:
        if show['title'].lower() == showname.lower():
            if debug:
                print("Found %s" % show['title'])
            name = fullshowname
            key = "booshfm/" + mixcloud.slugify(name)
            if debug:
                print("Key: %s" % key)
            payload = {'name': name,        # Use the filename which includes datestamp
                       'percentage_music': 100,
                       'description': show['desc'],
                       }
            with open(mp3file, 'rb') as mp3:
                files = {'mp3': mp3.read()}
            try:
                for num, tag in enumerate(show['tags']):
                    payload['tags-%s-tag' % num] = tag
            except:
                pass
            try:
                image_file = path + image_path + show['picturefile']
                files['picture'] = open(image_file, 'rb')
            except:
                print("Couldn't find an image file for show: %s" % (show['title']))
                pass

            r = requests.post(base_url,
                              data=payload,
                              params={'access_token': access_token},
                              files=files,
                              )

            if debug:
                print(r.status_code)
                print(r.text)


if __name__ == "__main__":
    main()