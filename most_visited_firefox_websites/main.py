import os
import re
from sqlite3 import *

import pandas as pd


def get_places_location():
    """Location of places.sqlite i.e. where cookies are stored"""
    username = os.listdir("/home")[0]
    default_release = [x for x in os.listdir(
        f"/home/{username}/.mozilla/firefox/") if "default-release" in x][0]
    places_location = f"/home/{username}/.mozilla/firefox/{default_release}/places.sqlite"
    return places_location


def get_visits_per_website():
    """Get the number of visits for each website for Mozilla Firefox"""
    places_location = get_places_location()
    conn = connect(places_location)
    cursor = conn.cursor()

    query = """SELECT pl.rev_host as reversed_host, count(*) as n_visits
               FROM moz_places as pl, moz_historyvisits as hist
               WHERE pl.id = hist.place_id
               GROUP BY pl.rev_host
               ORDER BY n_visits desc
               """
    cursor.execute(query)
    rows = [(re.sub("^\.www\.|^\.", "", website[::-1]), counts)
            for website, counts in cursor]
    website_n_visits = pd.DataFrame(rows)
    website_n_visits.columns = ["Website", "visits"]

    cursor.close()
    conn.close()
    return website_n_visits


if __name__ == "__main__":
    SHOW = 10
    website_visits = get_visits_per_website()
    print(website_visits[:SHOW])
