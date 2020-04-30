import os
import time

import requests
import json
from .error import error_message



API_KEY = os.environ.get('API_KEY')
headers = {
        'Content-Type': 'application/json',
        'x-happi-key': API_KEY,
    }


def get_lyrics_text(artist, album_name):
    lyrics_txt = get_artist_id(artist, album_name)
    return lyrics_txt


def get_artist_id(artist, album_name):
    url_endpoint = "https://api.happi.dev/v1/music"
    
    params ={
        'q': artist,
        'limit': '20',
        'type': 'artist'
    }

    r = requests.get(
            url= url_endpoint,
            headers=headers,
            params=params
        )

    body =json.loads(r.content)
    results = body['result']
    for n in results:
        if n['artist'].lower()== artist.lower():
            iD = n['id_artist']
            return get_album_id( iD, album_name)
    
    message =['Artist not found. Did you mean {artist_1}, {artist_2} or {artist_3}'.format(
        artist_1 = results[0]['artist'], 
        artist_2 = results[1]['artist'],
        artist_3 = results[2]['artist']
        )]
    return message




def get_album_id(ar_id, album_name):
    url_endpoint = 'https://api.happi.dev/v1/music/artists/{id_artist}/albums'.format(id_artist=ar_id)
    
    r = requests.get(
            url= url_endpoint,
            headers=headers
        )

    body =json.loads(r.content)
    results = body['result']
    albums = results['albums']
    for n in albums:
        if n['album'].lower()== album_name.lower():
            return get_song_list(n['api_album'])
        

    message = ['Album not found. You could try out {album_1}, {album_2} or {album_3}'.format(
        album_1 = results['albums'][0]['album'], 
        album_2 = results['albums'][1]['album'],
        album_3 = results['albums'][2]['album']
        )
    ]
    return message

def get_song_list(link):

    url_endpoint = link + '/tracks'
    r = requests.get(
            url= url_endpoint,
            headers=headers
        )

    if r.ok:
        body =json.loads(r.content)
        results = body['result']
        artist = results['artist']
        tracks = results['tracks']
        lyrics_txt = ''
        counter = 0
        for n in tracks:
            
            lyrics = compile_lyrics(n['track'], artist)
            if lyrics == -1:
                counter += lyrics
            else:
                if len(lyrics_txt)== 0:
                    lyrics_txt += lyrics
                else:
                    lyrics_txt = lyrics_txt + '\n\n\n' + lyrics
        if counter <= -5:
            return error_message()
        else:
            return lyrics_txt
    else:
        return error_message(r.status_code)


def compile_lyrics(track, artist):

        url_endpoint = 'https://api.lyrics.ovh/v1/{artist}/{track}'.format(artist=artist, track=track)
        r =requests.get(
            url = url_endpoint,
            headers={'Content-Type': 'application/json'}
        )
        if r.status_code == 429:
            print('Blocked, trying in a few seconds')
            time.sleep(10)
            return compile_lyrics(track, artist)
        if r.ok:
            response = json.loads(r.content)
            if response['lyrics']:
                lyrics = response['lyrics']
                if type(lyrics) ==str:
                    return lyrics
                else:
                    lyrics = -1
                    return lyrics

            else:
                lyrics = -1
                return lyrics
            

