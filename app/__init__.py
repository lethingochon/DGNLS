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

# 🛠️ CHUẨN HÓA VÀ NẠP TẤT CẢ GIÁO VIÊN TỪ GV.XLSX VÀO CSDL
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
                    # Đọc và chuẩn hóa dữ liệu
                    email_val = str(row.get('Email', row.get('email', ''))).strip().lower()
                    ma_gv_val = str(row.get('Mã GV', row.get('MaGV', row.get('ma_gv', '')))).strip()
                    ho_ten_val = str(row.get('Họ và tên', row.get('HoTen', ''))).strip()
                    pass_val = str(row.get('Mật khẩu', row.get('MatKhau', '123456'))).strip()

                    if email_val == 'nan': email_val = ''
                    if ma_gv_val == 'nan': ma_gv_val = ''
                    if pass_val == 'nan' or not pass_val: pass_val = '123456'

                    if email_val or ma_gv_val:
                        # Kiểm tra xem tài khoản đã có trong CSDL chưa
                        existing = None
                        if email_val:
                            existing = TeacherModel.query.filter(TeacherModel.email.ilike(email_val)).first()
                        if not existing and ma_gv_val:
                            existing = TeacherModel.query.filter_by(ma_gv=ma_gv_val).first()

                        # Nếu chưa có thì thêm mới
                        if not existing:
                            gv = TeacherModel()
                            if hasattr(gv, 'email') and email_val: gv.email = email_val
                            if hasattr(gv, 'ma_gv') and ma_gv_val: gv.ma_gv = ma_gv_val
                            if hasattr(gv, 'ho_ten'): gv.ho_ten = ho_ten_val if ho_ten_val != 'nan' else ''
                            if hasattr(gv, 'password'): gv.password = generate_password_hash(pass_val)
                            db.session.add(gv)
                            added_count += 1
                
                db.session.commit()
                print(f">>> ĐÃ NẠP THÀNH CÔNG {added_count} GIÁO VIÊN VÀO CSDL!", flush=True)
            else:
                print(f">>> KHÔNG TÌM THẤY FILE GV.XLSX TẠI: {excel_path}", flush=True)
    except Exception as e:
        print(f">>> LỖI NẠP DỮ LIỆU: {e}", flush=True)

from app import routes

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
