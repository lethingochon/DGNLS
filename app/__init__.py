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

# 🛠️ TỰ ĐỘNG KHỞI TẠO BỘ DỮ LIỆU & PHÂN QUYỀN ĐẦY ĐỦ (HT, HP, TT, GV)
with app.app_context():
    db.create_all()
    try:
        Teacher = models.Teacher
        Criteria = models.Criteria
        Field = models.Field
        TeacherCriteria = models.TeacherCriteria
        Role = models.Role
        Department = models.Department
        Subject = models.Subject

        # 1. Khởi tạo đầy đủ 4 Vai trò hệ thống
        roles_dict = {}
        roles_data = [
            (1, "HT", "HIỆU TRƯỜNG"),
            (2, "HP", "HIỆU PHÓ"),
            (3, "TT", "TỔ TRƯỜNG"),
            (4, "GV", "GIÁO VIÊN")
        ]
        for r_id, r_code, r_name in roles_data:
            r = Role.query.filter_by(code=r_code).first()
            if not r:
                r = Role(id=r_id, code=r_code, name=r_name)
                db.session.add(r)
                db.session.commit()
            roles_dict[r_code] = r

        # 2. Khởi tạo các Tổ chuyên môn
        dept_dict = {}
        dept_names = ["Tổ Tự Nhiên", "Tổ Xã Hội", "Tổ Ngoại Ngữ", "Tổ Tổng Hợp"]
        for idx, d_name in enumerate(dept_names, start=1):
            d = Department.query.filter(Department.name.ilike(f"%{d_name.replace('Tổ ', '')}%")).first()
            if not d:
                d = Department(id=idx, name=d_name)
                db.session.add(d)
                db.session.commit()
            dept_dict[d_name] = d

        # 3. Khởi tạo Môn học mặc định
        default_subject = Subject.query.first()
        if not default_subject:
            default_subject = Subject(id=1, code="TIN", name="Tin học")
            db.session.add(default_subject)
            db.session.commit()

        # 4. Khởi tạo Lĩnh vực & Bộ Tiêu chí đánh giá
        default_field = Field.query.first()
        if not default_field:
            default_field = Field(id=1, code="LV1", name="Năng lực số cơ bản")
            db.session.add(default_field)
            db.session.commit()

        if Criteria.query.count() == 0:
            sample_criterias = [
                ("TC01", "Sử dụng thiết bị số và phần mềm dạy học cơ bản", "Sử dụng máy tính, máy chiếu, bảng tương tác trong giảng dạy."),
                ("TC02", "Khai thác và quản lý dữ liệu số trong giáo dục", "Lưu trữ, khai thác giáo án và tài liệu trên đám mây (Google Drive, OneDrive)."),
                ("TC03", "Ứng dụng AI và công nghệ số thiết kế bài giảng", "Sử dụng các công cụ AI, Canva, PowerPoint nâng cao để thiết kế bài học."),
                ("TC04", "Tổ chức kiểm tra đánh giá trên môi trường số", "Sử dụng Azota, Google Forms, Kahoot để tổ chức kiểm tra, đánh giá học sinh."),
            ]
            for idx, (code, name, desc) in enumerate(sample_criterias, start=1):
                c = Criteria(
                    id=idx, field_id=default_field.id, code=code, name=name,
                    description=desc, max_score=10.0, display_order=idx, is_active=True
                )
                db.session.add(c)
            db.session.commit()

        # 5. Đọc file GV.xlsx và Nạp danh sách Giáo viên
        excel_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'GV.xlsx')
        if os.path.exists(excel_path):
            df = pd.read_excel(excel_path)
            max_teacher = Teacher.query.order_by(Teacher.id.desc()).first()
            current_id = max_teacher.id if max_teacher else 0
            
            # Danh sách từ khóa nhận diện Tổ trưởng chuyên môn
            tt_keywords = ["THUỶ", "THỦY", "TRƯỞNG", "TỔ TRƯỜNG"]

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
                    final_magv = magv_val if magv_val else (email_val.split('@')[0] if email_val else f"GV{current_id+1}")
                    final_email = email_val if email_val else f"{final_magv.lower()}@thpt.edu.vn"

                    # Phân định vai trò ban đầu
                    assigned_role_id = roles_dict["GV"].id
                    name_upper = name_val.upper()
                    if any(kw in name_upper for kw in tt_keywords):
                        assigned_role_id = roles_dict["TT"].id

                    existing = Teacher.query.filter(
                        (Teacher.email.ilike(final_email)) | (Teacher.magv.ilike(final_magv))
                    ).first()

                    if not existing:
                        current_id += 1
                        gv = Teacher(
                            id=current_id, magv=final_magv, full_name=name_val if name_val else 'Giáo viên',
                            email=final_email, password_hash=generate_password_hash(pass_val),
                            subject_id=default_subject.id, role_id=assigned_role_id, department_id=dept_dict["Tổ Tổng Hợp"].id
                        )
                        db.session.add(gv)

        # 6. Thiết lập quyền Hiệu phó/Quản trị (HP) cho tài khoản của cô Lê Thị Ngọc Hớn
        admin_email = 'lethingochon.hoabinh@gmail.com'
        admin_acc = Teacher.query.filter(Teacher.email.ilike(admin_email)).first()
        if admin_acc:
            admin_acc.role_id = roles_dict["HP"].id
        else:
            max_teacher = Teacher.query.order_by(Teacher.id.desc()).first()
            current_id = (max_teacher.id + 1) if max_teacher else 1
            admin_acc = Teacher(
                id=current_id, magv='ADMIN', full_name='Lê Thị Ngọc Hớn',
                email=admin_email, password_hash=generate_password_hash('123456'),
                subject_id=default_subject.id, role_id=roles_dict["HP"].id, department_id=dept_dict["Tổ Tổng Hợp"].id
            )
            db.session.add(admin_acc)

        db.session.commit()

        # 7. Gán tự động bộ tiêu chí cho tất cả giáo viên
        all_teachers = Teacher.query.all()
        all_criterias = Criteria.query.all()
        tc_max = TeacherCriteria.query.order_by(TeacherCriteria.id.desc()).first()
        tc_id = tc_max.id if tc_max else 0
        
        for t in all_teachers:
            for c in all_criterias:
                if not TeacherCriteria.query.filter_by(teacher_id=t.id, criteria_id=c.id).first():
                    tc_id += 1
                    tc = TeacherCriteria(id=tc_id, teacher_id=t.id, criteria_id=c.id, status="CHUA_NOP")
                    db.session.add(tc)
        db.session.commit()
        print(">>> NẠP VÀ PHÂN QUYỀN HỆ THỐNG THÀNH CÔNG!", flush=True)

    except Exception as e:
        print(f">>> LỖI NẠP DỮ LIỆU: {e}", flush=True)

from app import routes

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
