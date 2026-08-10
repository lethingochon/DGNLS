import os
import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object("config.Config")

db.init_app(app)

from app import models

# 🛠️ NẠP TẤT CẢ GIÁO VIÊN VÀ TỰ ĐỘNG DÒ CỘT EXCEL
with app.app_context():
    db.create_all()
    try:
        TeacherModel = getattr(models, 'Teacher', None) or getattr(models, 'GiaoVien', None) or getattr(models, 'User', None)
        
        if TeacherModel:
            excel_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'GV.xlsx')
            if os.path.exists(excel_path):
                df = pd.read_excel(excel_path)
                added_count = 0
                
                for _, row in df.iterrows():
                    email_val, ma_gv_val, ho_ten_val, pass_val = '', '', '', '123456'
                    
                    # Dò tìm cột thông minh không phân biệt hoa thường
                    for col in df.columns:
                        col_str = str(col).strip().lower()
                        val_str = str(row[col]).strip()
                        if val_str and val_str != 'nan':
                            if 'email' in col_str: email_val = val_str.lower()
                            elif 'mã' in col_str or 'magv' in col_str or 'ma_gv' in col_str: ma_gv_val = val_str
                            elif 'họ' in col_str or 'hoten' in col_str or 'ho_ten' in col_str: ho_ten_val = val_str
                            elif 'mật' in col_str or 'matkhau' in col_str or 'pass' in col_str: pass_val = val_str

                    if email_val or ma_gv_val:
                        existing = None
                        if email_val: existing = TeacherModel.query.filter(TeacherModel.email.ilike(email_val)).first()
                        if not existing and ma_gv_val: existing = TeacherModel.query.filter_by(ma_gv=ma_gv_val).first()

                        if not existing:
                            gv = TeacherModel()
                            if hasattr(gv, 'email') and email_val: gv.email = email_val
                            if hasattr(gv, 'ma_gv') and ma_gv_val: gv.ma_gv = ma_gv_val
                            if hasattr(gv, 'ho_ten'): gv.ho_ten = ho_ten_val
                            if hasattr(gv, 'password'): gv.password = generate_password_hash(pass_val)
                            db.session.add(gv)
                            added_count += 1

                # Bắt buộc tạo tài khoản mặc định cho cô nếu chưa có trong file
                admin_email = 'lethingochon.hoabinh@gmail.com'
                if not TeacherModel.query.filter(TeacherModel.email.ilike(admin_email)).first():
                    admin_acc = TeacherModel()
                    if hasattr(admin_acc, 'email'): admin_acc.email = admin_email
                    if hasattr(admin_acc, 'ma_gv'): admin_acc.ma_gv = 'ADMIN'
                    if hasattr(admin_acc, 'ho_ten'): admin_acc.ho_ten = 'Lê Thị Ngọc Hớn'
                    if hasattr(admin_acc, 'password'): admin_acc.password = generate_password_hash('123456')
                    db.session.add(admin_acc)
                    added_count += 1

                db.session.commit()
                print(f">>> ĐÃ NẠP THÀNH CÔNG {added_count} TÀI KHOẢN VÀO CSDL!", flush=True)
    except Exception as e:
        print(f">>> LỖI NẠP DỮ LIỆU: {e}", flush=True)

from app import routes

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
