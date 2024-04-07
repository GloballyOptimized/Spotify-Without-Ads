from functions import *

songs = get_playlist_songs()

for song in songs:
    song_link = search_youtube(song)
    download_mp3(song_link)
remove_video_files()

print('Playlist Downloaded Successfully')