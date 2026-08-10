import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dgnls-thpt-sec-key-2026'
    # Nhận chuỗi kết nối từ biến môi trường, mặc định dùng SQLite nếu không có
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///dgnls.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
