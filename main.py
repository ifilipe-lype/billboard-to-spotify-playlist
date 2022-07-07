import os
import sys
import spotipy
import requests

from datetime import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

# Loads .env data into os.environ
load_dotenv()

# Validates date input
try:
    date_input_separated = input(
        "Which year do you want to travel to? Type the date in this format YYYY-MM-DD: "
    ).split(sep="-")

    year, month, day = map(lambda x: int(x), date_input_separated)

    date = datetime(year, month, day).strftime("%Y-%m-%d")
except Exception as e:
    print("Invalid date format! Please type the date in this format YYYY-MM-DD")
    sys.exit(1)

# Validates top limit input
try:
    top = int(input("Type a number for the top limit of songs: "))
    if top <= 0 or top > 100:
        raise Exception()

except Exception as e:
    print("Invalid number! top must be greater than 1 and less than or equal to 100")
    sys.exit(1)

# Scraping Billboard 100
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
soup = BeautifulSoup(response.text, 'html.parser')
char_results = soup.find(name="div", class_="chart-results-list")

song_cards = char_results.select(
    selector=".o-chart-results-list-row-container > ul > li > ul > li:first-of-type"
)

songs = []

counter = 0
for song_card in song_cards:

    song_title = song_card.find(
        name="h3", id="title-of-a-story").getText().strip()
    song_owner = song_card.find(
        name="span", class_="c-label").getText().strip()

    songs.append([song_owner, song_title])

    counter += 1

    if counter >= top:
        break

# #Spotify Authentication
try:
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope="playlist-modify-public",
            redirect_uri=os.environ.get("SPOTIFY_REDIRECTION_URI"),
            client_id=os.environ.get("SPOTIFY_CLIENT_ID"),
            client_secret=os.environ.get("SPOTIFY_CLIENT_SECRET"),
            cache_path=".cache.token"
        )
    )
    user_id = sp.current_user()["id"]
except:
    print("Failled to authenticate with spotify! verify your credentials in .env file")

# Searches Spotify for songs by title
song_uris = []
year = date.split("-")[0]
for [song_author, song_title] in songs:
    result = sp.search(q=f"track:{song_title} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song_title} doesn't exist in Spotify. Skipping!")

playlist_name = f"{date} Billboard Top {top}"

# Gets the user playlists
try:
    playlists = sp.user_playlists(user=user_id)
except:
    print("Failled to get your playlists on spotify. Verify your network connection!")
    sys.exit(1)

playlist = None

# Check for a playlist with the same name as the playlist_name
for playlist_item in playlists['items']:
    if playlist_item.get("name") == playlist_name:
        playlist = playlist_item

if not playlist:
    # Creates a new public playlist in Spotify
    try:
        playlist = sp.user_playlist_create(
            user=user_id,
            name=playlist_name,
            description=f"Playlist created by a bot from billboard top {top} at {date}"
        )
        # Adding songs found into the new playlist
        sp.playlist_replace_items(playlist_id=playlist["id"], items=song_uris)
    except:
        print("Failled create your playlist on spotify. Verify your network connection!")
        sys.exit(1)
    

print(f"Done, check your '{playlist_name}' on spotify. Have fun!")