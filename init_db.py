#!/usr/bin/python3
from app import db
from app import User

# Create database table headers.
db.create_all()

# # Query
print(User.query.all())
