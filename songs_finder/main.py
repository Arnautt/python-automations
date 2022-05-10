import requests
from bs4 import BeautifulSoup

N_SONGS = 5
keywords = input("Enter keywords you want to find (any number of keywords with space between each of them): ")
URL = f"https://www.lyrics.com/lyrics/{keywords}"
response = requests.get(URL)

soup = BeautifulSoup(response.text, "html.parser")
songs = soup.find_all("pre", class_="lyric-body")


for song in songs[:N_SONGS]:
    song_location = song.attrs["onclick"]
    url = song_location.split("=")[-1][:-1][1:-1]
    url = requests.utils.unquote(url)
    artist = url.split("/")[-2].replace("+", " ")
    title = url.split("/")[-1].replace("+", " ")

    print(f"{artist} - {title}")
