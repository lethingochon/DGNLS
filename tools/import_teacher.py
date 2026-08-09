import pandas as pd
from werkzeug.security import generate_password_hash

# Đọc file Excel
df = pd.read_excel("GV.xlsx", sheet_name="GIAOVIEN")

# Ánh xạ môn học
subject_map = {
    "TOÁN": "TOAN",
    "NGỮ VĂN": "VAN",
    "TIẾNG ANH": "TA",
    "VẬT LÝ": "LY",
    "HÓA HỌC": "HOA",
    "HOÁ HỌC": "HOA",
    "SINH HỌC": "SINH",
    "TIN HỌC": "TIN",
    "LỊCH SỬ": "SU",
    "ĐỊA LÝ": "DIA",
    "GDKTPL": "KTPL",
    "CÔNG NGHỆ": "CN",
    "QPAN": "QPAN",
    "GDQPAN": "QPAN",
    "KTPL": "KTPL",
    "AN-QP": "QPAN",
    "THỂ DỤC": "TD",
    "GD THỂ CHẤT": "TD",
    "TIẾNG KHMER": "KHMER"
}

# Chuẩn hóa tên tổ
department_map = {
    "Tổ Tiếng Anh": "Tổ Ngoại ngữ",
    "Tổ Ngoại ngữ": "Tổ Ngoại ngữ",
    "Tổ Tự nhiên": "Tổ Tự nhiên",
    "Tổ Xã hội": "Tổ Xã hội",
    "Tổ Tổng hợp": "Tổ Tổng hợp",
    "Tổ Tổng hợp ": "Tổ Tổng hợp"
}

default_password = generate_password_hash("123456")

with open("database/04_sample_data.sql", "w", encoding="utf-8") as f:

    f.write("-- DỮ LIỆU GIÁO VIÊN\n\n")

    count = 0

    for _, row in df.iterrows():

        code = str(row["MAGV"]).strip()
        fullname = str(row["HOTEN"]).replace("'", "''").strip()
        email = str(row["EMAIL"]).strip()

        role_code = str(row["CHUCVU"]).strip()

        department_name = str(row["TOCM"]).strip()
        department_name = department_map.get(department_name, department_name)

        subject_name = str(row["MONDAY"]).strip().upper()
        if code == "ktplxuyen":
            print("MAGV:", code)
            print("Môn:", repr(subject_name))
            print("Tổ:", repr(department_name))

        if subject_name not in subject_map:
            print(f"Bỏ qua {code}: môn '{subject_name}' chưa khai báo")
            continue

        subject_code = subject_map[subject_name]

        sql = f"""
INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'{code}',
'{fullname}',
'{email}',
'{default_password}',
(SELECT id FROM role WHERE code='{role_code}'),
(SELECT id FROM department WHERE name='{department_name}'),
(SELECT id FROM subject WHERE code='{subject_code}')
);

"""

        f.write(sql)
        count += 1

print("========================================")
print("Hoàn thành!")
print("Đã tạo: database/04_sample_data.sql")
print("Tổng số giáo viên xuất:", count)