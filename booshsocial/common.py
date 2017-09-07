import os
import pyaml
from config import *


def find_show(current):
    """Pass this function a show name and it will return
        a dict of values if the show exists in the shows.yaml file
        or a None object if not found
    """
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(path + "/" + SHOWFILE) as shows:
        shows = pyaml.yaml.load(shows)

    if current[:6] == "Live: ":
        showname = current[6:]  # Strip off "Live: " prefix if present
    else:
        showname = current
    found = False
    for show in shows:
        if show['title'].lower() == showname.lower():
            found = True
            if debug:
                print("Found show: %s" % show['title'])
            foundshow = show
    if not found:
        if debug:
            print("Couldn't find show: %s in %s" % (showname, SHOWFILE))
        return None
    else:
        return foundshow