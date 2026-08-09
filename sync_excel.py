import os
import pandas as pd
from werkzeug.security import generate_password_hash
from app import app, db
from app.models import Teacher, Department, Role

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, "GV.xlsx")

def sync_excel():
    with app.app_context():
        if not os.path.exists(EXCEL_PATH):
            print(f"❌ Không tìm thấy file: {EXCEL_PATH}")
            return

        try:
            df = pd.read_excel(EXCEL_PATH)
            print("📖 Đã mở file GV.xlsx thành công!")
        except Exception as e:
            print("❌ Lỗi mở file GV.xlsx:", e)
            return

        # 1. Đảm bảo Roles tồn tại
        roles_def = {"HT": "HIỆU TRƯỜNG", "HP": "HIỆU PHÓ", "TT": "TỔ TRƯỜNG", "TP": "TỔ PHÓ", "GV": "GIÁO VIÊN"}
        for code, name in roles_def.items():
            if not Role.query.filter_by(code=code).first():
                db.session.add(Role(code=code, name=name))
        db.session.commit()
        roles = {r.code: r for r in Role.query.all()}

        # 2. Đảm bảo Departments tồn tại
        dept_objs = {}
        target_names = ["Tổ Tự Nhiên", "Tổ Xã Hội", "Tổ Tổng Hợp", "Tổ Ngoại Ngữ"]
        for name in target_names:
            d = Department.query.filter_by(name=name).first()
            if not d:
                d = Department(name=name)
                db.session.add(d)
                db.session.commit()
            dept_objs[name] = d

        # 3. Định vị cột
        magv_col = df.columns[0]
        name_col = df.columns[1]
        dept_col = df.columns[2]
        
        email_col = next((c for c in df.columns if "EMAIL" in str(c).upper() or "@" in str(c)), None)
        role_col = next((c for c in df.columns if any(v in df[c].astype(str).str.upper().tolist() for v in ["TT", "TP", "GV", "HT", "HP"])), None)

        default_password = generate_password_hash("123456")
        updated_count = 0

        for _, row in df.iterrows():
            magv = str(row[magv_col]).strip() if pd.notna(row[magv_col]) else None
            full_name = str(row[name_col]).strip() if pd.notna(row[name_col]) else None
            raw_dept = str(row[dept_col]).strip().lower() if pd.notna(row[dept_col]) else ""
            email = str(row[email_col]).strip() if email_col and pd.notna(row[email_col]) else None
            raw_role = str(row[role_col]).strip().upper() if role_col and pd.notna(row[role_col]) else "GV"

            if not magv or magv == "nan" or not full_name:
                continue

            teacher = Teacher.query.filter((Teacher.magv == magv) | (Teacher.full_name == full_name)).first()
            if not teacher:
                teacher = Teacher(magv=magv)
                db.session.add(teacher)

            teacher.magv = magv
            teacher.full_name = full_name
            if email:
                teacher.email = email
            teacher.password_hash = default_password  # Set mật khẩu mặc định 123456

            # Ghép Tổ
            if any(k in raw_dept for k in ["tự nhiên", "tu nhien", "tn", "toán", "lý", "hóa", "sinh"]):
                teacher.department_id = dept_objs["Tổ Tự Nhiên"].id
            elif any(k in raw_dept for k in ["xã hội", "xa hoi", "xh", "văn", "sử", "địa", "gdcd"]):
                teacher.department_id = dept_objs["Tổ Xã Hội"].id
            elif any(k in raw_dept for k in ["tổng hợp", "tong hop", "th", "thể dục", "tin", "công nghệ"]):
                teacher.department_id = dept_objs["Tổ Tổng Hợp"].id
            elif any(k in raw_dept for k in ["ngoại ngữ", "ngoai ngu", "nn", "anh", "tiếng anh"]):
                teacher.department_id = dept_objs["Tổ Ngoại Ngữ"].id

            # Gán vai trò
            name_upper = full_name.upper()
            if "DƯ QUỐC KIỆT" in name_upper:
                teacher.role_id = roles["HT"].id
            elif "NGUYỄN CHƠN NHẤT HỮU" in name_upper or "NHẤT HỮU" in name_upper or "LÂM VĂN HÙNG" in name_upper:
                teacher.role_id = roles["HP"].id
            elif raw_role in roles:
                teacher.role_id = roles[raw_role].id
            else:
                teacher.role_id = roles["GV"].id

            updated_count += 1

        db.session.commit()
        print(f"\n🎉 Đã đồng bộ thành công {updated_count} giáo viên kèm Email & Mật khẩu '123456'!")

if __name__ == "__main__":
    sync_excel()