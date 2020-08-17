#!/usr/bin/python3
from __future__ import print_function
from flask import Flask, render_template
from flask import request, url_for, redirect, Response
import json
from flask_sqlalchemy import SQLAlchemy

from app.models import MyForm, LoginForm, PlaySongForm, SubmitSongForm
from app.config import Config

from pydub import AudioSegment
from pydub.playback import play
import io


app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
# https://stackoverflow.com/questions/13772884/css-problems-with-flask-web-app
app.static_folder = 'static'
db = SQLAlchemy(app)

# MAX_LARGE_BINARY_LENGTH_IN_BYTES = 64000000


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
        db.LargeBinary(app.config['MAX_CONTENT_LENGTH']), unique=False, nullable=False
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


def add_song_to_db(name, artist, mp3_file) -> bool:
    """Return `False` if unable to insert entry to Song table due to bad input
    or some referential integrity violation. Otherwise return `True`."""
    print(f"Trying adding song: {name} by artist: {artist} to database")
    try:
        song = Song(name=name, artist=artist, mp3_file=mp3_file)
        db.session.add(song)
        db.session.commit()
        return True
    except Exception:
        return False
# END: Utility functions #


def delete_user_from_db(email) -> bool:
    print("Trying to delete user from db...")
    try:
        user = User.query.filter_by(email=email).first()
        db.session.delete(user)
        db.session.commit()
        return True
    except Exception:
        return False


def update_user_email_in_db(name, password, new_email) -> bool:
    print("Trying updating user...")
    # NOTE: we don't authenticate password for now. Just check if user exists
    # in db and if so we can delete and re-insert the user with the new email.
    try:
        user = User.query.filter_by(name=name, password=password).first()
        delete_user_from_db(user.email)
    except Exception:
        return False

    add_user_to_db(name=name, email=new_email, password=password)
    return True


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


@app.route('/upload_song', methods=('GET', 'POST'))
def upload_song():
    form = MyForm()
    return render_template('upload_song.html', form=form)


# TODO: convert uploaded mp3 file into bytes and implement the upload song db.
@app.route('/submit_song', methods=('GET', 'POST'))
def submit_song():
    """Submit a new mp3 file to uploaded to the website.
    """
    form = SubmitSongForm(
        name=request.form['name'],
        artist=request.form['artist'],
        mp3_file=request.form['mp3_file']
    )
    status = form.validate()
    if status:
        status = add_song_to_db(
            name=request.form['name'],
            artist=request.form['artist'],
            mp3_file=request.form['mp3_file']
        )
    else:
        print('Failed to upload')
        print(f'Checking type of mp3_file uploaded: {type(request.form["mp3_file"])}')
    return redirect(url_for('all_data'))


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
    return render_template('admin.html', users=users)


def user_api_get():
    name = request.args.get('name')
    email = request.args.get('email')
    password = request.args.get('password')
    is_successful = add_user_to_db(name=name, email=email, password=password)
    if is_successful:
        print('Successfully added user to db')
        return Response(
            "{'response': user was successfully created}",
            status=201, mimetype='application/json'
        )
    # Reference: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/406
    else:
        print('Failed to add user to db')
        return Response(
            "{'response': username already exists}",
            status=406, mimetype='application/json'
        )


def user_api_delete():
    email = request.args.get('email')
    is_deleted = delete_user_from_db(email=email)
    if is_deleted:
        print('Successfully deleted user from db')
        return Response(
            "{'response': user was successfully deleted!}",
            status=201, mimetype='application/json'
        )
    else:
        print('Failed to add user to db')
        return Response(
            "{'response': user with that email does not exist}",
            status=406, mimetype='application/json'
        )


def user_api_put():
    name = request.args.get('name')
    password = request.args.get('password')
    new_email = request.args.get('email')

    is_updatable = True
    if is_updatable:
        is_updated = update_user_email_in_db(name=name, password=password, new_email=new_email)
        if is_updated:
            print('Successfully updated email in db')
            return Response(
                "{'response': user email was successfully updated}",
                status=201, mimetype='application/json'
            )
        else:
            print('Failed to update email in db')
            return Response(
                "{'response': user name does not exist - failed to update email}",
                status=406, mimetype='application/json'
            )
    else:
        print('User email is not updatable')
        return Response(
            "{'response': user password is incorrect - failed to update email}",
            status=406, mimetype='application/json'
        )


# Example request url:
# http://127.0.0.1:5000/create_user?name=Randy%20%email=randy@gmail.com%20%password=12345
@app.route('/user', methods=['GET', 'DELETE', 'PUT'])
def user_api():
    """Handle each type of request method with:
        1) if/else statements OR
        2) dictionary that maps to function names (since python has no switch keyword)
    Otherwise we get a 405 method call permission denied error message.

    https://stackoverflow.com/questions/34853033/
    """
    api_methods_dict = {
        'GET': user_api_get,
        'DELETE': user_api_delete,
        'PUT': user_api_put
    }
    if request.method not in api_methods_dict.keys():
        print(f'Request method is not supported: {request.method}')
        return Response(
            "{'response:': request method not supported}",
            status=406, mimetype='application/json'
        )
    return api_methods_dict[request.method]()


if __name__ == '__main__':
    app.run(debug=True)
