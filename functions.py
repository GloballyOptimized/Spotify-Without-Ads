import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch
from pytube import YouTube
import moviepy.editor as mp
#.....................................................................

load_dotenv()

# Set up Spotify credentials
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

def get_playlist_songs(playlist_link:str):

    index = 0
    last = 0 
    while index < len(playlist_link)-1:
        if playlist_link[index] == '/':
            last = index+1
        index+=1
    playlist_id = playlist_link[last:index+1]

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Get playlist tracks
    results = sp.playlist_tracks(playlist_id)

    # Extract song names from the tracks
    song_names = [track['track']['name'] for track in results['items']]

    return(song_names)
#.................................................................................................................

def search_youtube(song_name):  #working fine

    videos_search = VideosSearch(song_name, limit = 1)
    
    results = videos_search.result()

    if results and 'result' in results:
        first_video = results['result'][0]
        url = first_video['link']
        return url
    else:
        return None
#...................................................................................................................

def download_mp3(youtube_link, output_path:str):
    try:
        yt = YouTube(youtube_link)

        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream.download(output_path=output_path)
        video_path = f"{output_path}/{audio_stream.default_filename}"
        mp.AudioFileClip(video_path).write_audiofile(f"{output_path}/{yt.title}.mp3")
        mp.AudioFileClip(video_path).close()

        return True
    except:
        return None
#..............................................................................................................

def remove_video_files(directory_path): #working fine
    all_files = os.listdir(directory_path)
    for file in all_files:
        if '.mp4' in file:
            os.remove(directory_path+'//'+file)

    return('Task Executed Successfully')
#..............................................................................................................
