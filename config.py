import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "digiteacher-secret-key"

    # Kết nối chuẩn tới file SQLite dgnls.db trong thư mục instance
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'dgnls.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False