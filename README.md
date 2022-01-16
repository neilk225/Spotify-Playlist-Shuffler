# Spotify Playlist Shuffler
This is a command line tool that shuffles a public/preexisting Spotify playlist and adds it to the user's library, it utilizes Spotipy (a lightweight library for the Spotify Web API).
## Usage/Setup
Create a new Spotify developer application at the following link: https://developer.spotify.com/dashboard/applications.

Within main.py, edit the code block (lines 89 - 90) below with your own **client_id** and **client_secret** found at the above link.
```
client = spot.Spotify(auth_manager=spot.SpotifyOAuth(client_id='enter within quotes', 
                    client_secret='enter within quotes',
                    redirect_uri='https://open.spotify.com',
                    scope='playlist-modify-public playlist-read-private playlist-modify-private'))
```

To run the program, enter the following line (make sure you are in the same directory).
```
python main.py
```
**WARNING: This tool does not work with any playlists that contain local files.**
