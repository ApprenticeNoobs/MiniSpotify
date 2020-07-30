#!/usr/bin/python3
from __future__ import print_function
from flask import Flask, jsonify, render_template
from flask import escape, request, url_for
from flask import flash, redirect
import json
import os
from flask_sqlalchemy import SQLAlchemy

from app.models import MyForm, LoginForm
from app.config import Config

app = Flask(__name__, instance_relative_config=True)

# SECRET_KEY = os.urandom(32)
# app.config['SECRET_KEY'] = SECRET_KEY
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config.from_object(Config)
db = SQLAlchemy(app)


# START: Database Tables
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return f'<User: id={self.id}, name={self.name}, email={self.email}>'
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
    if(form.validate_on_submit()):
        return render_template('home.html',form=form)
    return render_template('login.html',form=form)

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
    return render_template('home.html',form=None)


@app.route('/all_data')
def all_data():
    '''
    arg: None
    return: the entire json data we loaded
    '''
    return jsonify(test_data)


@app.route('/render_all_data', methods=['POST', 'GET'])
def render_all_data():
    '''
    arg: None
    return: a rendered html using the entire json data
    '''
    data_path = 'test/song.json'
    with open(data_path) as f:
        test_data = json.load(f)
    return render_template('visualize_data.html', data=test_data)


@app.route('/user/<name>')
def user_page(name):
    return "User: %s" % escape(name)


@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name="Haosong"))
    print(url_for('user_page', name="Zishi"))
    print(url_for("test_url_for"))
    print(url_for('test_url_for', num=2))
    return "Test page"


if __name__ == '__main__':
    app.run(debug=True)
