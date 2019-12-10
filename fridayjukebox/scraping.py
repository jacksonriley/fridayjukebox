from bs4 import BeautifulSoup
import json
import re
import requests


# The Friday Jukebox URL
JUKEBOX_URL = "https://open.spotify.com/playlist/2rBhCRAfexo1VG01r1zP93"


def get_name_from_id(id):
    """
    Takes in an id to convert to a user's name
    """
    user_html = requests.get("https://open.spotify.com/user/" + id).text
    username = BeautifulSoup(user_html, 'html.parser').title.text.replace(" on Spotify", "")
    return username


def json_to_md(tracks):
    """
    Takes in the playlist summary data and outputs a table formatted in
    MarkDown
    """
    md_string = """| Song | Artist | Album | Added by |
|-|-|-|-|"""

    for track in tracks:
        # Construct the artist elements seperately to make multiple artists
        # easier
        artist_elements = ["[{}]({})".format(artist, link) for artist, link in
            zip(track["Artists"], track["Artist links"])]

        track_row = "| [{}]({}) | {} | [{}]({}) | {} |".format(
            track["Song name"], track["Song link"],
            "<br>".join(artist_elements),
            track["Album"], track["Album link"],
            track["Added by"]
        )
        md_string = md_string + "\n" + track_row

    return md_string


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
title = BeautifulSoup(r.text, 'html.parser').title.text.replace(' ', '_').replace('_on_Spotify', '')

# Parse the data for each track and collate the interesting information
parsed_tracks = []
for track in data['tracks']['items']:
    parsed_tracks.append({
        "Added by": get_name_from_id(track["added_by"]["id"]),
        "Added at": track["added_at"],
        "Song name": track["track"]["name"],
        "Song link": track["track"]["external_urls"]["spotify"],
        "Album": track["track"]["album"]["name"],
        "Album link": track["track"]["album"]["external_urls"]["spotify"],
        "Artists": [artist["name"] for artist in track["track"]["artists"]],
        "Artist links": [artist["external_urls"]["spotify"] for artist in track["track"]["artists"]],
        "Duration": ms_to_minsec(track["track"]["duration_ms"])
    })

with open("json/" + title + ".json", "w") as f:
    json.dump(parsed_tracks, f, indent=4)

with open("json/" + title + "_detailed.json", "w") as f:
    json.dump(data['tracks']['items'], f, indent=4)

with open("md/" + title + ".md", "w") as f:
    f.write(json_to_md(parsed_tracks))