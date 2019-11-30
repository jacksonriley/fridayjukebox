from bs4 import BeautifulSoup
import subprocess
import json
jukebox_url = "https://open.spotify.com/playlist/2rBhCRAfexo1VG01r1zP93?si=gpACiEhzQCer96EkEP3KjA"

html_doc = subprocess.run(["curl", jukebox_url], capture_output=True).stdout

soup = BeautifulSoup(html_doc, 'html.parser')
tracks = soup.find_all("div", class_="tracklist-col name")
parsed_tracks = []
for track in tracks:
    parsed_tracks.append({"Title": track.find("span", class_="track-name").text,
                          "Artist": track.find("span", class_="artists-albums").contents[0].text,
                          "Album": track.find("span", class_="artists-albums").contents[2].text})

with open(soup.title.text.replace(' ', '_'), "w") as f:
    json.dump(parsed_tracks, f)