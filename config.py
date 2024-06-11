import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://nikita:root@localhost/Hotel'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
