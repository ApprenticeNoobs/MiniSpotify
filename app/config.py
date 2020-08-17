import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or str(os.urandom(32))
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or "sqlite:///test.db"
    MAX_CONTENT_LENGTH = 64 * 1024 * 1024  # 64 MB max-limit
