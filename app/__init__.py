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

# 🛠️ NẠP DỮ LIỆU CHUẨN XÁC VÀO CSDL TỪ FILE GV.XLSX
with app.app_context():
    db.create_all()
    try:
        Teacher = models.Teacher
        
        excel_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'GV.xlsx')
        if os.path.exists(excel_path):
            df = pd.read_excel(excel_path)
            added_count = 0
            
            for _, row in df.iterrows():
                email_val, magv_val, name_val, pass_val = '', '', '', '123456'
                
                # Dò cột trong file Excel
                for col in df.columns:
                    col_str = str(col).strip().lower()
                    val_str = str(row[col]).strip()
                    if val_str and val_str != 'nan':
                        if 'email' in col_str: email_val = val_str.lower()
                        elif 'mã' in col_str or 'magv' in col_str or 'ma_gv' in col_str: magv_val = val_str
                        elif 'họ' in col_str or 'hoten' in col_str or 'ho_ten' in col_str or 'tên' in col_str: name_val = val_str
                        elif 'mật' in col_str or 'matkhau' in col_str or 'pass' in col_str: pass_val = val_str

                if email_val or magv_val:
                    # Kiểm tra xem tài khoản đã tồn tại trong database chưa
                    existing = None
                    if email_val: 
                        existing = Teacher.query.filter(Teacher.email.ilike(email_val)).first()
                    if not existing and magv_val: 
                        existing = Teacher.query.filter_by(magv=magv_val).first()

                    if not existing:
                        gv = Teacher(
                            email=email_val if email_val else f"{magv_val}@school.edu.vn",
                            magv=magv_val if magv_val else email_val.split('@')[0],
                            full_name=name_val if name_val else 'Giáo viên',
                            password_hash=generate_password_hash(pass_val)
                        )
                        db.session.add(gv)
                        added_count += 1

            # Đảm bảo chắc chắn có tài khoản của cô
            admin_email = 'lethingochon.hoabinh@gmail.com'
            if not Teacher.query.filter(Teacher.email.ilike(admin_email)).first():
                admin_acc = Teacher(
                    email=admin_email,
                    magv='ADMIN',
                    full_name='Lê Thị Ngọc Hớn',
                    password_hash=generate_password_hash('123456')
                )
                db.session.add(admin_acc)
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
