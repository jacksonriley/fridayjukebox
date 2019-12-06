# fridayjukebox
Repository to scrape the friday jukebox playlist and maintain a back catalogue


Once you clone the repo, you can just run the scraping script:

```
python3 -m venv my_virtual_env
source my_virtual_env/bin/activate
pip3 install -r requirements.txt
python3 fridayjukebox/scraping.py
```

That'll output a new file (or overwrite the existing one) corresponding to the current Friday Jukebox playlist
