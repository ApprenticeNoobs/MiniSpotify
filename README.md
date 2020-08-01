# MiniSpotify
Request mp3 files for song from a limited catalog

### Setup
1. Initialize the database containing tables for `User` and `Song`. Run `init_db.py`.
2. The `assets` folder contains the `artist` folder. Inside the `artist` folder is a bunch
   of folders where each folder is named after an artist, e.g. `mozart`. Inside a folder
   like `mozart` is a bunch of .mp3 files, where each file is the name of a song. For example,
   `assets/artist/mozart/rondo_alla_turca.mp3` would be the path to an .mp3 file of Mozart's
   Turkish March song. Once you have created your artist name folders, e.g. `mozart`, `the_beatles`,
   and you put at least one ".mp3" file in each artist name folder (otherwise program crashes).
   Then run `init_songs.py`, which will store your ".mp3" files in a database table.
3. After logging in, click `get_all_data` to see a list of all songs available to listen to.
   Enter the `id` of the song you wish to listen to, press play, and it will play the
   first 10 seconds of the song.

### Known Issues
1. If you press play and then back, the song keeps playing util 10 seconds are finished.
2. If song exists in db but you have the same mp3 file and you run `init_songs.py`, then
   the database insertion will fail. We need to check if song exists in db before inserting
   it to db.
3. The `init_songs.py` script assumes only .mp3 files exist in a artist name folder, and
   only artist name folders exist in `assets/artist`. If a file were to exist in `assets/artist`
   then the script assumes that file is directory. We tried using `os.path.isdir` to select
   only subdirectories in `assets/artist` but it failed; we need to make it work somehow.
   Likewise, if a non .mp3 file were to exist in `assets/artist/mozart`, for example either
   a .txt or a .wav file, the script would, assume it is an .mp3 file, store it as binary,
   and then when a user tries to play that file, it would fail because the file is not an
   .mp3 file and our `play_song` route only supports .mp3 file.
4. If no mp3 file exists in an artist name folder, then we think that `init_songs.py` will crash
   but it has not been confirmed yet. Need to fix issue #1 first before we can test this. 
5. To pass data from html view page to flask route function, we have to submit a form. We tried
   to make a clickable play button and link that to a route function, but could not find any
   examples online of how to do this.
