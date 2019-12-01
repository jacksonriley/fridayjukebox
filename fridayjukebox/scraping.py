from bs4 import BeautifulSoup
import json
import re
import requests


# The Friday Jukebox URL
JUKEBOX_URL = "https://open.spotify.com/playlist/2rBhCRAfexo1VG01r1zP93"


def ms_to_minsec(time_ms):
    """
    Takes in a time in milliseconds and returns the formatted time in minutes
    and seconds
    """
    time_s = int(time_ms)/1000
    if time_s < 60:
        return "{}s".format(int(time_s))
    else:
        mins, secs = divmod(time_s, 60)
        return "{}m{}s".format(int(mins), int(secs))


# Get the HTML
r = requests.get(JUKEBOX_URL)

# Find the "Spotify.Entity" section which contains all the song information
p = re.compile(r'Spotify\.Entity = (.*?)};')
data = json.loads(p.findall(r.text)[0] + "}")

# Get the playlist title for this week
title = BeautifulSoup(r.text, 'html.parser').title.text.replace(' ', '_')

# Parse the data for each track and collate the interesting information
parsed_tracks = []
for track in data['tracks']['items']:
    parsed_tracks.append({
        "Added by": track["added_by"]["id"],
        "Added at": track["added_at"],
        "Song name": track["track"]["name"],
        "Song link": track["track"]["external_urls"]["spotify"],
        "Album": track["track"]["album"]["name"],
        "Album link": track["track"]["album"]["external_urls"]["spotify"],
        "Artist": track["track"]["artists"][0]["name"],
        "Artist link": track["track"]["artists"][0]["external_urls"]["spotify"],
        "Duration": ms_to_minsec(track["track"]["duration_ms"])
    })

with open(title, "w") as f:
    json.dump(parsed_tracks, f, indent=4)