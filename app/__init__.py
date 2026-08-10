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

# 🛠️ NẠP TỐI ƯU SIÊU NHANH & TỰ ĐỘNG GÁN ID CHUẨN CHO SQLITE
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
                    db.session.add(Role(id=r_id, code=r_code, name=r_name))
            db.session.commit()
            roles_dict = {r.code: r for r in Role.query.all()}

            # 2. Nạp Lĩnh vực
            if 'LINHVUC' in xls.sheet_names:
                df_lv = pd.read_excel(excel_path, sheet_name='LINHVUC')
                for idx, row in df_lv.iterrows():
                    m_lv = str(row.get('MÃ LV', f'LV{idx+1}')).strip()
                    t_lv = str(row.get('TÊN LĨNH VỰC', '')).strip()
                    if not Field.query.filter_by(code=m_lv).first():
                        db.session.add(Field(id=idx+1, code=m_lv, name=t_lv))
                db.session.commit()

            default_field = Field.query.first()
            if not default_field:
                default_field = Field(id=1, code="LV01", name="NĂNG LỰC SỬ DỤNG CÔNG NGHỆ SỐ")
                db.session.add(default_field)
                db.session.commit()

            # 3. Nạp Tiêu chí
            if 'TIEUCHI' in xls.sheet_names:
                df_tc = pd.read_excel(excel_path, sheet_name='TIEUCHI')
                for idx, row in df_tc.iterrows():
                    m_tc = str(row.get('MATC', f'TC{idx+1}')).strip()
                    m_lv = str(row.get('MALV', '')).strip()
                    t_tc = str(row.get('TENTIEUCHI', '')).strip()
                    d_max = float(row.get('DIEMTOIDA', 10.0)) if pd.notnull(row.get('DIEMTOIDA')) else 10.0
                    
                    f_obj = Field.query.filter_by(code=m_lv).first() or default_field
                    if not Criteria.query.filter_by(code=m_tc).first():
                        db.session.add(Criteria(id=idx+1, field_id=f_obj.id, code=m_tc, name=t_tc, description=t_tc, max_score=d_max, display_order=idx+1, is_active=True))
                db.session.commit()

            # 4. Nạp Giáo viên & Gán ID tự tăng cho Tổ CM, Môn học
            max_d = Department.query.order_by(Department.id.desc()).first()
            dept_id_cnt = max_d.id if max_d else 0

            max_s = Subject.query.order_by(Subject.id.desc()).first()
            subj_id_cnt = max_s.id if max_s else 0

            if 'GIAOVIEN' in xls.sheet_names:
                df_gv = pd.read_excel(excel_path, sheet_name='GIAOVIEN')
                for idx, row in df_gv.iterrows():
                    magv = str(row.get('MAGV', '')).strip()
                    hoten = str(row.get('HOTEN', '')).strip()
                    tocm = str(row.get('TOCM', 'Tổ Tổng hợp')).strip()
                    monday = str(row.get('MONDAY', 'Tin học')).strip()
                    chucvu = str(row.get('CHUCVU', 'GV')).strip().upper()
                    email = str(row.get('EMAIL', '')).strip().lower()

                    d_obj = Department.query.filter_by(name=tocm).first()
                    if not d_obj:
                        dept_id_cnt += 1
                        d_obj = Department(id=dept_id_cnt, name=tocm)
                        db.session.add(d_obj)
                        db.session.commit()

                    s_obj = Subject.query.filter_by(name=monday).first()
                    if not s_obj:
                        subj_id_cnt += 1
                        s_obj = Subject(id=subj_id_cnt, code=f"MON_{subj_id_cnt}", name=monday)
                        db.session.add(s_obj)
                        db.session.commit()

                    target_role = roles_dict.get(chucvu, roles_dict.get("GV"))
                    final_email = email if (email and email != 'nan') else f"{magv.lower()}@thpt.edu.vn"

                    existing = Teacher.query.filter((Teacher.email.ilike(final_email)) | (Teacher.magv.ilike(magv))).first()
                    if not existing:
                        gv = Teacher(
                            id=idx+1, magv=magv, full_name=hoten, email=final_email,
                            password_hash=generate_password_hash('123456'),
                            subject_id=s_obj.id, role_id=target_role.id, department_id=d_obj.id
                        )
                        db.session.add(gv)
                    else:
                        existing.magv = magv
                        existing.full_name = hoten
                        existing.role_id = target_role.id
                        existing.department_id = d_obj.id
                        existing.subject_id = s_obj.id
                db.session.commit()

            # 5. Gán tiêu chí siêu tốc
            all_teachers = Teacher.query.all()
            all_criterias = Criteria.query.all()
            existing_tc = set(db.session.query(TeacherCriteria.teacher_id, TeacherCriteria.criteria_id).all())
            
            tc_max = TeacherCriteria.query.order_by(TeacherCriteria.id.desc()).first()
            tc_id = tc_max.id if tc_max else 0

            new_tc_list = []
            for t in all_teachers:
                for c in all_criterias:
                    if (t.id, c.id) not in existing_tc:
                        tc_id += 1
                        new_tc_list.append(TeacherCriteria(id=tc_id, teacher_id=t.id, criteria_id=c.id, status="CHUA_NOP"))

            if new_tc_list:
                db.session.bulk_save_objects(new_tc_list)
                db.session.commit()

            # 6. Nạp Minh chứng cũ từ Excel nếu CSDL trống
            if 'MINHCHUNG' in xls.sheet_names and Evidence.query.count() == 0:
                df_mc = pd.read_excel(excel_path, sheet_name='MINHCHUNG')
                ev_id = 0
                status_map = {"Đạt": "DA_XAC_NHAN", "Chờ duyệt": "DA_NOP", "Bổ sung": "TU_CHOI"}
                
                for _, row in df_mc.iterrows():
                    mc_magv = str(row.get('MAGV', '')).strip()
                    mc_matc = str(row.get('MATC', '')).strip()
                    tenhd = str(row.get('TENHD', '')).strip()
                    tep = str(row.get('TEPMINHCHUNG', '')).strip()
                    trangthai_str = str(row.get('TRANGTHAI', '')).strip()

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

            print(">>> ĐÃ NẠP CSDL SIÊU NHANH VÀ SỬA LỖI ID THÀNH CÔNG!", flush=True)

    except Exception as e:
        print(f">>> LỖI NẠP DỮ LIỆU: {e}", flush=True)

from app import routes

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
