# PURPOSE: Utility functions to populate Song table with list of songs.

from app import db
from app import Song

import os
import pathlib
from typing import List


# NOTE: if you really want to be Pythonic, create a decorate that appends
# a path prefix such as `ARTIST_DIR_PATH` to the artist names. Then the
# method `get_artist_paths()` can just be a call to the get_artist_names
# that applies the decorator with `ARTIST_DIR_PATH` as the input prefix.

class SongTracker:
    """Tracks all songs in the `assets` directory of the MiniSpotify project.

    Args:
        __ASSET_DIR_PATH (str):
            Path to assets directory
        __ARTIST_DIR_PATH (str):
            Path to directory containing artist names as subdirectories.
    """
    def __init__(self):
        self.__ASSET_DIR_PATH = str(pathlib.Path(os.getcwd(), 'assets'))
        self.__ARTIST_DIR_PATH = str(pathlib.Path(self.__ASSET_DIR_PATH, 'artist'))

    def get_artist_name(self, artist_path: str) -> str:
        # Assume the artist name is the string after the last '/' character
        return artist_path.split('/')[-1]

    def get_artist_paths(self) -> List[str]:
        # NOTE: this is not working for some reason so we will assume there are only
        # directories with artist names in the `ARTIST_DIR_PATH`.
        # all_subdirs = [d for d in os.listdir(ARTIST_DIR_PATH) if os.path.isdir(d)]
        return [str(pathlib.Path(self.__ARTIST_DIR_PATH, d)) for d in os.listdir(self.__ARTIST_DIR_PATH)]

    def get_song_name(self, song_path: str) -> str:
        # Assume the artist name is the string after the last '/' character
        return song_path.split('/')[-1]

    def get_song_paths(self, artist_path: str) -> List[str]:
        # NOTE: why is `os.path.isfile` not working?
        # return [f for f in os.listdir(artist_path) if os.path.isfile(f)]
        return [str(pathlib.Path(artist_path, f)) for f in os.listdir(artist_path)]

    def read_song_bytes(self, song_path: str) -> bytes:
        try:
            with open(song_path, "rb") as f:
                return f.read()
        except FileNotFoundError as e:
            print(f'Path to song file not found: {song_path}')
            raise FileNotFoundError(e)

    def get_song_list_for_db(self) -> List[tuple]:
        song_list_for_db = []
        artist_paths = self.get_artist_paths()
        for artist_path in artist_paths:
            artist_name = self.get_artist_name(artist_path)
            song_paths = self.get_song_paths(artist_path)
            for song_path in song_paths:
                song_name = self.get_song_name(song_path)
                song_bytes = self.read_song_bytes(song_path)
                song_list_for_db.append( (song_name, artist_name, song_bytes) )
        return song_list_for_db

    def write_to_db(self) -> None:
        for song_name, artist_name, song_bytes in self.get_song_list_for_db():
            print(f"Trying adding song: {song_name} by artist: {artist_name} to database")
            try:
                song = Song(name=song_name, artist=artist_name, mp3_file=song_bytes)
                db.session.add(song)
                db.session.commit()
                print('Success: wrote song to db')
            except Exception as e:
                print('Fail: error occurred while trying to write song to db.')
                raise Exception(e)


def main():
    song_tracker = SongTracker()
    song_tracker.write_to_db()


if __name__ == '__main__':
    main()
