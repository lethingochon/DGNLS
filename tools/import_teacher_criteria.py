import pymysql

# ==============================
# Kết nối MySQL
# ==============================
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="123456",          # sửa nếu MySQL của thầy có mật khẩu
    database="digiteacher",
    charset="utf8mb4"
)

cursor = conn.cursor()

# ==============================
# Xóa dữ liệu cũ
# ==============================
cursor.execute("DELETE FROM teacher_criteria")

# ==============================
# Lấy danh sách giáo viên
# ==============================
cursor.execute("""
SELECT id
FROM teacher
ORDER BY id
""")
teachers = cursor.fetchall()

# ==============================
# Lấy danh sách tiêu chí
# ==============================
cursor.execute("""
SELECT id
FROM criteria
WHERE is_active = 1
ORDER BY field_id, code
""")
criterias = cursor.fetchall()

print(f"Số giáo viên : {len(teachers)}")
print(f"Số tiêu chí  : {len(criterias)}")

count = 0

# ==============================
# Sinh dữ liệu
# ==============================
for teacher in teachers:
    teacher_id = teacher[0]

    for criteria in criterias:
        criteria_id = criteria[0]

        cursor.execute("""
            INSERT INTO teacher_criteria
            (
                teacher_id,
                criteria_id,
                status,
                leader_comment,
                principal_comment,
                submitted_at,
                leader_reviewed_at,
                principal_reviewed_at
            )
            VALUES
            (
                %s,
                %s,
                'CHUA_THUC_HIEN',
                NULL,
                NULL,
                NULL,
                NULL,
                NULL
            )
        """, (teacher_id, criteria_id))

        count += 1

conn.commit()

print("=" * 40)
print("Hoàn thành!")
print("Đã tạo:", count, "bản ghi")

cursor.close()
conn.close()