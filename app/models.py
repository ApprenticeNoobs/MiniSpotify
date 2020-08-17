#!/usr/bin/python3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired


class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class LoginForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField('Sign In')


class PlaySongForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired()])


class SubmitSongForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    artist = StringField('artist', validators=[DataRequired()])
    mp3_file = FileField('mp3_file', validators=[FileRequired(), FileAllowed(['mp3'], 'MP3 only!')])
