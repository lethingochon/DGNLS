import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object("config.Config")

# 📌 CẤU HÌNH CSDL TRỰC TUYẾN
# Tự động nhận CSDL Render (DATABASE_URL), nếu không có sẽ tự tạo CSDL SQLite (dgnls.db)
db_url = os.environ.get("DATABASE_URL", "sqlite:///dgnls.db")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Import models để SQLAlchemy biết các bảng
from app import models

# 🛠️ TỰ ĐỘNG TẠO BẢNG DỮ LIỆU KHI CHẠY TRÊN RENDER
with app.app_context():
    db.create_all()

from app import routes

# Tạo thư mục uploads nếu chưa có
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER