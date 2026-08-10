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

# 🛠️ TỰ ĐỘNG NẠP TOÀN BỘ 37 GIÁO VIÊN TỪ FILE GV.XLSX VÀO CSDL
with app.app_context():
    db.create_all()
    try:
        TeacherModel = getattr(models, 'Teacher', None) or getattr(models, 'GiaoVien', None) or getattr(models, 'User', None)
        
        if TeacherModel and TeacherModel.query.count() == 0:
            # Đường dẫn tới file GV.xlsx ở thư mục gốc
            excel_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'GV.xlsx')
            
            if os.path.exists(excel_path):
                df = pd.read_excel(excel_path)
                for _, row in df.iterrows():
                    # Đọc thông tin các cột linh hoạt
                    email_val = str(row.get('Email', '')).strip()
                    ma_gv_val = str(row.get('Mã GV', row.get('MaGV', ''))).strip()
                    ho_ten_val = str(row.get('Họ và tên', row.get('HoTen', ''))).strip()
                    pass_val = str(row.get('Mật khẩu', row.get('MatKhau', '123456'))).strip()

                    # Lấy thông tin môn học, tổ bộ môn nếu có trong Excel
                    mon_hoc_val = str(row.get('Môn học', row.get('MonHoc', ''))).strip() if 'Môn học' in row or 'MonHoc' in row else None
                    to_bm_val = str(row.get('Tổ bộ môn', row.get('ToBoMon', ''))).strip() if 'Tổ bộ môn' in row or 'ToBoMon' in row else None

                    if (email_val and email_val != 'nan') or (ma_gv_val and ma_gv_val != 'nan'):
                        gv = TeacherModel()
                        if hasattr(gv, 'email'): gv.email = email_val if email_val != 'nan' else None
                        if hasattr(gv, 'ma_gv'): gv.ma_gv = ma_gv_val if ma_gv_val != 'nan' else None
                        if hasattr(gv, 'ho_ten'): gv.ho_ten = ho_ten_val if ho_ten_val != 'nan' else ''
                        if hasattr(gv, 'password'): gv.password = generate_password_hash(pass_val if pass_val != 'nan' else '123456')
                        if hasattr(gv, 'mon_hoc') and mon_hoc_val and mon_hoc_val != 'nan': gv.mon_hoc = mon_hoc_val
                        if hasattr(gv, 'to_bo_mon') and to_bm_val and to_bm_val != 'nan': gv.to_bo_mon = to_bm_val
                        
                        db.session.add(gv)
                db.session.commit()
                print(">>> Đã nạp thành công toàn bộ danh sách giáo viên từ GV.xlsx!")
    except Exception as e:
        print("Lỗi khi tự động nạp danh sách giáo viên:", e)

from app import routes

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
