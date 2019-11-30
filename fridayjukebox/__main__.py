import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

jukebox_uri = "spotify:playlist:2rBhCRAfexo1VG01r1zP93"
jukebox_url = "https://open.spotify.com/playlist/2rBhCRAfexo1VG01r1zP93?si=gpACiEhzQCer96EkEP3KjA"
client_id = "bc32c33e19d141979c000cac83666147"
client_secret = "fea686715b004c95be54aa5fd49366d7"
redirect_url = "http://localhost/"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# ret = sp.search(jukebox_url)
playlists = sp.user_playlists("jriley619@c2kni.net")
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None
import pdb; pdb.set_trace()