# Billboard to Spotify-playlist
This script will scrap the billboard website page of trending songs in the specified time

## Set up
1. clone this repo
```bash
git clone git@github.com:ifilipe-lype/billboard-to-spotify-playlist.git
```
2. setup the enviroment
```bash
cd billboard-to-spotify-playlist
python3 -m venv venv
```
3. installs the dependencies
```bash
./venv/bin/pip install -r requirements.txt
```
## Enviroments vars
1. go to [spotify's developer page](https://developer.spotify.com/dashboard/) (authenticate) and creates an app
2. creates a **.env** file, and fill in the blanks with your own data
3. **makes sure your SPOTIFY_REDIRECTION_URI is the same on your app's Redirect URIs section**
```
SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
SPOTIFY_REDIRECTION_URI=http://example.com
```

## Run
1. On the first run your browse will open up on spotify's authorization page
2. You will be redirected to another page (example.com) you must copy the entire url and past it into the terminal (it will be prompting you for it)
```bash
./venv/bin/python main.py [DATE] [TOP_LIMIT]
```
or
```bash
chmod +x main.py # makes file executable
./main.py [DATE] [TOP_LIMIT] # runs file directly
```
3. **DATE on format YYYY-MM-DD, TOP_LIMIT as integer will be prompted if not provided**