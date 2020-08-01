#!/usr/bin/python3
from app import db
from app import User
from app import Song

# Create database table headers.
print("Creating database tables...")
db.create_all()

# # Query
print('=====================================')
print("Querying contents of database tables")
print('=====================================')
print('User Table:')
print(User.query.all())
print('=====================================')
print('Song Table')
print(Song.query.all())
print('=====================================')
print('Finished initializing database!')
