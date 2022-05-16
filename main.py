import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("Which year do you want to travel? Type date in the format- YYYY-MM-DD: ")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
response.raise_for_status()

song_list = []

id = "5957dca369e941abab9f2e50293ca549"
secret = "7aaa9794e6ec4625a298047c630f87cf"
Uri = "https://developer.spotify.com/dashboard/applications/5957dca369e941abab9f2e50293ca549"


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=id,
                                               client_secret=secret,
                                               redirect_uri=Uri,
                                               scope="user-library-read",
                                               cache_path="token.txt"))

user_id = sp.current_user()

soup = BeautifulSoup(response.text, 'html.parser')
for songs in soup.find_all('h3', id="title-of-a-story"):
    song = songs.getText()
    if "Songwriter(s):" not in song and "Producer(s):" not in song and "Imprint/Promotion Label:" not in song and "Gains in Weekly Performance" not in song and "Additional Awards" not in song:
        song_list.append(song.strip())

music_playlist = []

for music in song_list:
    result = sp.search(q=f"track {music}", type="tracks")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        music_playlist.append(result)
    except IndexError:
        print(f"{music} doesn't exist in Spotify. Skipped.")

print(music_playlist)

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)
new_playlist = sp.playlist_add_items(playlist_id=playlist, items=music_playlist, position=None)
print(new_playlist)
