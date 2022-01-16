import os
import requests
import random
import sys
import spotipy as spot

def shufflePlaylist():
    # getting unparsed playlists
    try:
        unparsedPlaylists = client.current_user_playlists()
    except (requests.HTTPError, spot.SpotifyOauthError):
        sys.exit('Error: Authentication was unsuccessful (URL was more than likely entered incorrectly). The program will now exit.')
    
    # establishing some variables
    user_id = client.me()['id']
    listOfPlaylistsID = []
    playlistDigit = 1

    # printing each of the user's playlists and adding their IDs to a list
    print('Your playlists: ')
    for playlist in unparsedPlaylists['items']:
        if playlist['owner']['id'] == user_id:
            listOfPlaylistsID.append(playlist['id'])
            print (str(playlistDigit) + '. ' + playlist['name'] + ': ' + str(playlist['tracks']['total']) + ' tracks')
            playlistDigit += 1

    # prompting the user to either choose one of their playlists or enter the URL of one
    while True:
        n = input('Select a playlist from your library or enter the URL (beginning with ' + "'https://') of a playlist you'd like to shuffle: ")
        if n[0:5] == 'https':
            count = 0
            for i in range(len(n)):
                if n[i] == '/':
                    count += 1
                if count == 4:
                    chosenPlaylistID = n[i + 1:]
                    break
            break
        elif n == 'exit' or n == 'quit':
            sys.exit('You have successfully exited the application.')
        else:
            try:
                if int(n) == 0:
                    print ('Error: Playlist selection was out of bounds. Please reselect.')
                    continue
                if int(n) != 0 and int(n) <= len(listOfPlaylistsID):
                    chosenPlaylistID = listOfPlaylistsID[int(n) - 1]
                    break
                if int(n) > len(listOfPlaylistsID):
                    print ('Error: Playlist selection was out of bounds. Please reselect.')
                    continue
            except:
                print ('Error: Invalid character entered. Please try again.')
                continue

    # establishing some playlist related variables
    chosenPlaylist = client.playlist(chosenPlaylistID)
    newPlaylistName = chosenPlaylist['name'] + ' - SHUFFLED'
    shuffledTracks = []
    limit = 100
    offset = 0

    # shuffling the tracks and adding them to the newly created playlist above
    while True:
        tracksToShuffle = client.playlist_tracks(chosenPlaylistID, limit=limit, offset=offset)['items']
        for track in tracksToShuffle:
            shuffledTracks.append(track['track']['uri'])
        offset += limit
        if len(tracksToShuffle) != limit:
            break
    random.shuffle(shuffledTracks)
    offset = 0
    shuffledPlaylist = client.user_playlist_create(user_id, newPlaylistName, description='A shuffled version of the playlist titled ' + '"' + chosenPlaylist['name'] + '" - neilk225')
    try:
        while True:
            tracksToAdd = shuffledTracks[offset:offset + limit]
            client.user_playlist_add_tracks(user_id, shuffledPlaylist['id'], tracksToAdd)
            offset += limit
            if len(tracksToAdd) != limit:
                break
    except:
        client.current_user_unfollow_playlist(shuffledPlaylist['id'])
        sys.exit('Error: the selected playlist has local files which is not yet supported, sorry!')
    else:
        os.remove('.cache')
        sys.exit('The chosen playlist ' + "'" + chosenPlaylist['name'] + "' has been successfully shuffled and added to your library.")

# connecting to Spotify and authenticating the user
client = spot.Spotify(auth_manager=spot.SpotifyOAuth(client_id='enter within quotes', 
                    client_secret='enter within quotes',
                    redirect_uri='https://open.spotify.com',
                    scope='playlist-modify-public playlist-read-private playlist-modify-private'))

# calling the main function
shufflePlaylist()