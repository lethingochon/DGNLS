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

# 🛠️ NẠP HOÀN CHỈNH DỮ LIỆU TỪ TẤT CẢ CÁC SHEET CỦA GV.XLSX
with app.app_context():
    db.create_all()
    try:
        Teacher = models.Teacher
        Criteria = models.Criteria
        Field = models.Field
        TeacherCriteria = models.TeacherCriteria
        Evidence = models.Evidence
        TeacherCriteriaEvidence = models.TeacherCriteriaEvidence
        Role = models.Role
        Department = models.Department
        Subject = models.Subject

        excel_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'GV.xlsx')
        if os.path.exists(excel_path):
            xls = pd.ExcelFile(excel_path)

            # 1. Nạp Vai trò (HT, HP, TT, TP, GV)
            roles_dict = {}
            roles_data = [
                (1, "HT", "HIỆU TRƯỜNG"),
                (2, "HP", "HIỆU PHÓ"),
                (3, "TT", "TỔ TRƯỜNG"),
                (4, "TP", "TỔ PHÓ"),
                (5, "GV", "GIÁO VIÊN")
            ]
            for r_id, r_code, r_name in roles_data:
                r = Role.query.filter_by(code=r_code).first()
                if not r:
                    r = Role(id=r_id, code=r_code, name=r_name)
                    db.session.add(r)
                    db.session.commit()
                roles_dict[r_code] = r

            # 2. Nạp Lĩnh vực từ sheet LINHVUC
            fields_dict = {}
            if 'LINHVUC' in xls.sheet_names:
                df_lv = pd.read_excel(excel_path, sheet_name='LINHVUC')
                for idx, row in df_lv.iterrows():
                    m_lv = str(row.get('MÃ LV', f'LV{idx+1}')).strip()
                    t_lv = str(row.get('TÊN LĨNH VỰC', '')).strip()
                    f_obj = Field.query.filter_by(code=m_lv).first()
                    if not f_obj:
                        f_obj = Field(id=idx+1, code=m_lv, name=t_lv)
                        db.session.add(f_obj)
                        db.session.commit()
                    fields_dict[m_lv] = f_obj

            default_field = Field.query.first()
            if not default_field:
                default_field = Field(id=1, code="LV01", name="NĂNG LỰC SỬ DỤNG CÔNG NGHỆ SỐ")
                db.session.add(default_field)
                db.session.commit()

            # 3. Nạp 35 Tiêu chí từ sheet TIEUCHI
            criterias_dict = {}
            if 'TIEUCHI' in xls.sheet_names:
                df_tc = pd.read_excel(excel_path, sheet_name='TIEUCHI')
                for idx, row in df_tc.iterrows():
                    m_tc = str(row.get('MATC', f'TC{idx+1}')).strip()
                    m_lv = str(row.get('MALV', '')).strip()
                    t_tc = str(row.get('TENTIEUCHI', '')).strip()
                    d_max = float(row.get('DIEMTOIDA', 10.0)) if pd.notnull(row.get('DIEMTOIDA')) else 10.0
                    
                    target_field = fields_dict.get(m_lv, default_field)
                    c_obj = Criteria.query.filter_by(code=m_tc).first()
                    if not c_obj:
                        c_obj = Criteria(
                            id=idx+1, field_id=target_field.id, code=m_tc,
                            name=t_tc, description=t_tc, max_score=d_max, display_order=idx+1, is_active=True
                        )
                        db.session.add(c_obj)
                        db.session.commit()
                    criterias_dict[m_tc] = c_obj

            # 4. Nạp Giáo viên từ sheet GIAOVIEN
            dept_dict = {}
            subject_dict = {}
            if 'GIAOVIEN' in xls.sheet_names:
                df_gv = pd.read_excel(excel_path, sheet_name='GIAOVIEN')
                
                for idx, row in df_gv.iterrows():
                    magv = str(row.get('MAGV', '')).strip()
                    hoten = str(row.get('HOTEN', '')).strip()
                    tocm = str(row.get('TOCM', 'Tổ Tổng hợp')).strip()
                    monday = str(row.get('MONDAY', 'Tin học')).strip()
                    chucvu = str(row.get('CHUCVU', 'GV')).strip().upper()
                    email = str(row.get('EMAIL', '')).strip().lower()

                    # Xử lý Tổ CM
                    if tocm not in dept_dict:
                        d_obj = Department.query.filter_by(name=tocm).first()
                        if not d_obj:
                            d_obj = Department(id=len(dept_dict)+1, name=tocm)
                            db.session.add(d_obj)
                            db.session.commit()
                        dept_dict[tocm] = d_obj

                    # Xử lý Môn dạy
                    if monday not in subject_dict:
                        s_obj = Subject.query.filter_by(name=monday).first()
                        if not s_obj:
                            s_obj = Subject(id=len(subject_dict)+1, code=f"MON_{len(subject_dict)+1}", name=monday)
                            db.session.add(s_obj)
                            db.session.commit()
                        subject_dict[monday] = s_obj

                    target_role = roles_dict.get(chucvu, roles_dict["GV"])
                    target_dept = dept_dict[tocm]
                    target_subj = subject_dict[monday]

                    final_email = email if (email and email != 'nan') else f"{magv.lower()}@thpt.edu.vn"

                    existing = Teacher.query.filter((Teacher.email.ilike(final_email)) | (Teacher.magv.ilike(magv))).first()
                    if not existing:
                        gv = Teacher(
                            id=idx+1, magv=magv, full_name=hoten, email=final_email,
                            password_hash=generate_password_hash('123456'),
                            subject_id=target_subj.id, role_id=target_role.id, department_id=target_dept.id
                        )
                        db.session.add(gv)
                    else:
                        existing.magv = magv
                        existing.full_name = hoten
                        existing.role_id = target_role.id
                        existing.department_id = target_dept.id
                        existing.subject_id = target_subj.id

                db.session.commit()

            # 5. Khởi tạo bộ tiêu chí cho tất cả giáo viên
            all_teachers = Teacher.query.all()
            all_criterias = Criteria.query.all()
            tc_max = TeacherCriteria.query.order_by(TeacherCriteria.id.desc()).first()
            tc_id = tc_max.id if tc_max else 0
            
            for t in all_teachers:
                for c in all_criterias:
                    if not TeacherCriteria.query.filter_by(teacher_id=t.id, criteria_id=c.id).first():
                        tc_id += 1
                        db.session.add(TeacherCriteria(id=tc_id, teacher_id=t.id, criteria_id=c.id, status="CHUA_NOP"))
            db.session.commit()

            # 6. Nạp Minh chứng sẵn có từ sheet MINHCHUNG
            if 'MINHCHUNG' in xls.sheet_names:
                df_mc = pd.read_excel(excel_path, sheet_name='MINHCHUNG')
                ev_id = Evidence.query.count()
                for _, row in df_mc.iterrows():
                    mc_magv = str(row.get('MAGV', '')).strip()
                    mc_matc = str(row.get('MATC', '')).strip()
                    tenhd = str(row.get('TENHD', '')).strip()
                    tep = str(row.get('TEPMINHCHUNG', '')).strip()
                    trangthai_str = str(row.get('TRANGTHAI', '')).strip()

                    status_map = {"Đạt": "DA_XAC_NHAN", "Chờ duyệt": "DA_NOP", "Bổ sung": "TU_CHOI"}
                    final_status = status_map.get(trangthai_str, "DA_NOP")

                    teacher_obj = Teacher.query.filter_by(magv=mc_magv).first()
                    criteria_obj = Criteria.query.filter_by(code=mc_matc).first()

                    if teacher_obj and criteria_obj:
                        tc_obj = TeacherCriteria.query.filter_by(teacher_id=teacher_obj.id, criteria_id=criteria_obj.id).first()
                        if tc_obj:
                            tc_obj.status = final_status
                            if tep and tep != 'nan':
                                ev_id += 1
                                clean_file_path = tep.replace('\\', '/')
                                if not clean_file_path.startswith('/uploads/') and not clean_file_path.startswith('static/'):
                                    clean_file_path = f"/uploads/{clean_file_path}"

                                ev = Evidence(
                                    id=ev_id,
                                    title=tenhd if tenhd != 'nan' else f"Minh chứng {mc_matc}",
                                    storage_type="FILE",
                                    file_path=clean_file_path,
                                    url=None
                                )
                                db.session.add(ev)
                                db.session.commit()
                                db.session.add(TeacherCriteriaEvidence(teacher_criteria_id=tc_obj.id, evidence_id=ev.id))
                db.session.commit()

            print(">>> NẠP THÀNH CÔNG 35 TIÊU CHÍ VÀ DỮ LIỆU CHÍNH XÁC TỪ FILE EXCEL!", flush=True)

    except Exception as e:
        print(f">>> LỖI NẠP DỮ LIỆU: {e}", flush=True)

from app import routes

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
