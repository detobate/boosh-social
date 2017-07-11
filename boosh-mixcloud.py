#!/usr/bin/env python3
import pyaml, slugify
import mixcloud, requests, sys, os
from mixcloudkeys import *

debug = True
showfile = "shows.yaml"
image_path = "images/"
base_url = 'https://api.mixcloud.com/'
PIDFILE="/tmp/boosh_recording.pid"

def load_shows(yaml):
    with open(yaml) as shows:
        shows = pyaml.yaml.load(shows)
    return shows

def check_existing(slug):
    r = requests.get(base_url + slug)
    if r.status_code == 200:
        return True
    elif r.status_code == 404:
        return False

def auth_mixcloud():
    o = mixcloud.MixcloudOauth(
        client_id=client_id, client_secret=client_secret,
        redirect_uri="me")

    url = o.authorize_url()
    access_token = o.exchange_token(code)
    return access_token


def main():
    try:
        mp3file = os.path.basename(sys.argv[1])
        mp3file_full = os.path.dirname(os.path.abspath(sys.argv[1])) + "/" + mp3file
    except:
        print("You must provide a file to upload: %s <filename>" % (sys.argv[0]))
        exit(1)

    if os.path.isfile(PIDFILE):
        print("Still recording. Exiting")
        exit(1)

    access_token = auth_mixcloud()
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
                print("Found show: %s" % show['title'])
            name = fullshowname
            key = "booshfm/" + mixcloud.slugify(name)
            if debug:
                print("Key: %s" % key)

            exists = check_existing(key)
            if exists:
                print("Show already exists: %s" % ("https://mixcloud.com/" + key))
                exit(1)
            elif not exists:
                payload = {'name': name,        # Use the filename which includes datestamp
                           'percentage_music': 100,
                           'description': show['desc'],
                           }
                with open(mp3file_full, 'rb') as mp3:
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

                r = requests.post(base_url + "upload/",
                                  data=payload,
                                  params={'access_token': access_token},
                                  files=files)
                if debug:
                    print(r.status_code)
                    print(r.text)


if __name__ == "__main__":
    main()