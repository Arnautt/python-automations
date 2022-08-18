import functools
import operator
import os
import re
from sqlite3 import *

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from wordcloud import WordCloud


def plot_wordcloud_from_dict(d):
    """Plot and save wordcloud from a frequency dictionary"""
    mask = np.array(Image.open("logo_firefox.png"))

    wordcloud = WordCloud(mask=mask,
                          background_color="white",
                          contour_color='steelblue',
                          contour_width=3)

    wordcloud.generate_from_frequencies(frequencies=d)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig("wordcloud.png")


def get_places_location():
    """Get location of Firefox cookies for Ubuntu"""
    username = os.listdir("/home")[0]
    default_release = [x for x in os.listdir(
        f"/home/{username}/.mozilla/firefox/") if "default-release" in x][0]
    places_location = f"/home/{username}/.mozilla/firefox/{default_release}/places.sqlite"
    return places_location


def get_dict_from_df(res):
    """Create frequency dictionary from the cookies dataframe"""
    d = dict()
    for _, row in res.iterrows():
        _word = row["word"]
        _n_search = row["n_search"]
        d[_word] = _n_search
    return d


def get_google_searches():
    """Get all google searches from cookies"""
    places_location = get_places_location()
    conn = connect(places_location)
    conn.create_function("reverse_string", 1, lambda s: s[::-1])
    cursor = conn.cursor()

    query = '''SELECT pl.url, pl.title
               FROM moz_places as pl, moz_historyvisits as hist
               WHERE pl.id = hist.place_id
               '''

    cursor.execute(query)

    googles_searchs = [r[1] for r in cursor if
                       ("google" in r[0]) and ("q=" in r[0]) and (r[1] is not None)]

    googles_searchs = [re.sub(
        r" - Recherche Google| – Recherche Google| – Recherche Google", "", r) for r in googles_searchs]
    return googles_searchs


def get_words_dataframe(googles_searchs):
    """Given the result of sqlite query, get a dataframe with words frequencies"""
    words = [search.split(" ") for search in googles_searchs]
    words = functools.reduce(operator.concat, words)
    words = pd.Series(words).value_counts(ascending=False).reset_index()
    words.columns = ["word", "n_search"]
    _filter = [len(word) > 2 for word in words["word"]]
    words = words[_filter]
    return words


def main():
    """Retrieve google searches information and plot a wordcloud"""
    googles_searches = get_google_searches()
    words = get_words_dataframe(googles_searches)
    d = get_dict_from_df(words)
    plot_wordcloud_from_dict(d)


if __name__ == "__main__":
    main()
