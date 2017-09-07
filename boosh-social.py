#!/usr/bin/env python3
import requests
import html
from time import sleep
from booshsocial.booshfb import check_facebook
from booshsocial.booshtw import check_twitter
from booshsocial.common import find_show

from config import *

def get_current(url):
    r = requests.get(url)
    return(html.unescape(r.text))

def main():

    sleep(3)
    current = get_current(CURRENT_URL).rstrip()

    if "Live: " in current and len(current) > 7:
        show = find_show(current)
        check_twitter(current, show)
        check_facebook(current, show)
    else:
        pass

if __name__ == "__main__":
  main()
