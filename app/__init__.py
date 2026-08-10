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

# 🛠️ NẠP DỮ LIỆU GIÁO VIÊN KHỚP 100% VỚI MODELS.PY
with app.app_context():
    db.create_all()
    try:
        Teacher = models.Teacher
        
        # 1. Khởi tạo Môn học, Vai trò, Tổ chuyên môn mặc định
        default_subject = models.Subject.query.first()
        if not default_subject:
            default_subject = models.Subject(code="TIN", name="Tin học")
            db.session.add(default_subject)

        default_role = models.Role.query.filter_by(code="GV").first()
        if not default_role:
            default_role = models.Role(code="GV", name="GIÁO VIÊN")
            db.session.add(default_role)

        default_dept = models.Department.query.first()
        if not default_dept:
            default_dept = models.Department(name="Tổ Tổng Hợp")
            db.session.add(default_dept)
            
        db.session.commit()

        # 2. Đọc file GV.xlsx
        excel_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'GV.xlsx')
        if os.path.exists(excel_path):
            df = pd.read_excel(excel_path)
            added_count = 0
            
            for _, row in df.iterrows():
                email_val, magv_val, name_val, pass_val = '', '', '', '123456'
                
                for col in df.columns:
                    col_str = str(col).strip().lower()
                    val_str = str(row[col]).strip()
                    if val_str and val_str != 'nan':
                        if 'email' in col_str: email_val = val_str.lower()
                        elif 'mã' in col_str or 'magv' in col_str or 'ma_gv' in col_str: magv_val = val_str
                        elif 'họ' in col_str or 'hoten' in col_str or 'ho_ten' in col_str or 'tên' in col_str: name_val = val_str
                        elif 'mật' in col_str or 'matkhau' in col_str or 'pass' in col_str: pass_val = val_str

                if email_val or magv_val:
                    final_magv = magv_val if magv_val else (email_val.split('@')[0] if email_val else f"GV{added_count+1}")
                    final_email = email_val if email_val else f"{final_magv.lower()}@thpt.edu.vn"

                    existing = Teacher.query.filter(
                        (Teacher.email.ilike(final_email)) | (Teacher.magv.ilike(final_magv))
                    ).first()

                    if not existing:
                        gv = Teacher(
                            magv=final_magv,
                            full_name=name_val if name_val else 'Giáo viên',
                            email=final_email,
                            password_hash=generate_password_hash(pass_val),
                            subject_id=default_subject.id,
                            role_id=default_role.id,
                            department_id=default_dept.id
                        )
                        db.session.add(gv)
                        added_count += 1

            # Bắt buộc tạo tài khoản của cô
            admin_email = 'lethingochon.hoabinh@gmail.com'
            if not Teacher.query.filter(Teacher.email.ilike(admin_email)).first():
                admin_acc = Teacher(
                    magv='ADMIN',
                    full_name='Lê Thị Ngọc Hớn',
                    email=admin_email,
                    password_hash=generate_password_hash('123456'),
                    subject_id=default_subject.id,
                    role_id=default_role.id,
                    department_id=default_dept.id
                )
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
