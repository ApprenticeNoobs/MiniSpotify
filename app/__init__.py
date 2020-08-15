#!/usr/bin/python3
from __future__ import print_function
from flask import Flask, render_template
from flask import escape, request, url_for, redirect
import json
from flask_sqlalchemy import SQLAlchemy

from app.models import MyForm, LoginForm, PlaySongForm
from app.config import Config

from pydub import AudioSegment
from pydub.playback import play
import io


app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
app.static_folder = 'static'
db = SQLAlchemy(app)

MAX_LARGE_BINARY_LENGTH_IN_BYTES = 64000000


# NOTE: if we put db in a separate file, then it has to import app and the file
# containing app has to import db, causing circular dependency `ImportError`.
# Can't figure out alternative solution so we are lumping db table into __init__.py.
# START: Database Tables
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return f'<User: id={self.id}, name={self.name}, email={self.email}>'


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    artist = db.Column(db.String(120), unique=False, nullable=False)
    mp3_file = db.Column(
        db.LargeBinary(MAX_LARGE_BINARY_LENGTH_IN_BYTES), unique=False, nullable=False
    )

    def __repr__(self):
        return f'<Song: id={self.id}, name={self.name}, mp3_file_size={len(self.mp3_file)} bytes>'

# END: Database Tables


# START: run when web app starts up
data_path = 'test/song.json'
with open(data_path) as f:
    test_data = json.load(f)
# END: run when web app starts up


# START: Utility functions
def add_user_to_db(name, email, password) -> bool:
    """Return `False` if unable to insert entry to User table due to bad input
    or some referential integrity violation. Otherwise return `True`."""
    print(f"Trying adding user: {name} with email: {email} to database")
    try:
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return True
    except Exception:
        return False
# END: Utility functions #


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = MyForm()
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return render_template('home.html', form=form)
    return render_template('login.html', form=form)


@app.route('/submit', methods=('GET', 'POST'))
def submit():
    """Submit user registration form to database and redirect to success/failure status view.
    """
    form = MyForm(
        name=request.form['name'],
        email=request.form['email'],
        password=request.form['password']
    )
    status = form.validate()
    if status:
        status = add_user_to_db(
            name=request.form['name'],
            email=request.form['email'],
            password=request.form['password']
        )
    return render_template('/status.html', status=status)


@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    """load home template"""
    return render_template('home.html', form=None)


@app.route('/all_data')
def all_data():
    '''
    get data from song table
    reconstruct the binary blob to mp3 file
    arg: None
    return: the entire json data we loaded
    '''
    songs = Song.query.all()
    songs = [dict(id=str(song.id), name=str(song.name), artist=str(song.artist)) for song in songs]
    form = PlaySongForm()
    return render_template('music_page.html', form=form, songs=songs)


@app.route('/play_song', methods=('GET', 'POST'))
def play_song():
    song_id = request.form['id']
    song = Song.query.get(song_id)
    print(f"Requested to play song: {song}")

    audio = AudioSegment.from_file(io.BytesIO(song.mp3_file), format="mp3")
    first_ten_seconds = audio[:10000]
    play(first_ten_seconds)
    return redirect(url_for('all_data'))


@app.route('/admin')
def admin():
    users = User.query.all()
    print(users)
    return render_template('admin.html', users=users)



if __name__ == '__main__':
    app.run(debug=True)
