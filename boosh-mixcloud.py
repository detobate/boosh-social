#!/usr/bin/env python3
import mixcloud
import requests
import sys
import os
from mixcloudkeys import *
from booshsocial.common import find_show
from config import *

base_url = 'https://api.mixcloud.com/'
PIDFILE="/tmp/boosh_recording.pid"


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
        exit(1)

    show = find_show(showname)
    if show is not None:
        name = fullshowname
        key = "booshfm/" + mixcloud.slugify(name.replace("'", ""))
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
            if show['picturefile'] is not None:
                filename = os.path.dirname(os.path.abspath(__file__)) + IMAGES + show['picturefile']
                try:
                    files['picture'] = open(filename, 'rb')
                except:
                    print("Couldn't open image file: %s" % (filename))

            r = requests.post(base_url + "upload/",
                              data=payload,
                              params={'access_token': access_token},
                              files=files)
            if debug:
                print(r.status_code)
                print(r.text)


if __name__ == "__main__":
    main()