import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import pandas as pd

class SpotifyClient:
    def __init__(self):
        """Initialize the Spotify client with authentication"""
        self.client = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
                redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
                scope='user-library-read playlist-modify-public user-top-read'
            )
        )

    def get_current_user_info(
        self
    ):
        """Get current user's Spotify profile information"""
        return self.client.current_user()

    def get_user_playlists(
        self,
        limit=50
    ):
        """Get user's playlists"""
        return self.client.current_user_playlists(limit=limit)

    def get_top_tracks(
        self,
        limit=20,
        time_range='medium_term'
    ):
        """
        Get user's top tracks
        time_range options: short_term, medium_term, long_term
        """
        return self.client.current_user_top_tracks(
            limit=limit,
            offset=0,
            time_range=time_range
        )

    def create_playlist(
        self,
        name,
        description=""
    ):
        """Create a new playlist"""
        user_id = self.client.current_user()['id']
        return self.client.user_playlist_create(
            user_id,
            name,
            public=True,
            description=description
        )

    def search_tracks(
        self,
        query,
        limit=10
    ):
        """Search for tracks"""
        return self.client.search(query, limit=limit, type='track')

def get_playlist_tracks(
    spotify,
    playlist
):
    playlist_id = playlist.get('id')
    playlist_name = playlist.get('name')
    
    playlist_info = spotify.client.playlist(
        playlist_id
    )

    song_list_list = []
    for item in playlist_info.get('tracks').get('items'):
        song_list = [
            item.get('added_at'),
            item.get('added_by').get('id'),
            item.get('track').get('id'),
            item.get('track').get('name'),
            item.get('track').get('artists')[0].get('name')
        ]
        song_list_list.append(song_list)

    playlist_song_df = pd.DataFrame(
        song_list_list,
        columns = [
            'added_at',
            'added_by',
            'track_id',
            'track_name',
            'track_artist'
        ]
    )

    playlist_song_df['playlist_id'] = playlist_id
    playlist_song_df['playlist_name'] = playlist_name

    return playlist_song_df
    

