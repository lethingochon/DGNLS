from app import app, db
from sqlalchemy import text

with app.app_context():
    try:
        db.session.execute(text("ALTER TABLE teacher_criteria ADD COLUMN submitted_at DATETIME NULL;"))
        db.session.commit()
        print("✅ Đã thêm cột submitted_at (Thời gian nộp) thành công!")
    except Exception as e:
        print("ℹ️ Cột submitted_at đã tồn tại hoặc không cần thêm.")

    try:
        db.session.execute(text("ALTER TABLE teacher_criteria ADD COLUMN reviewed_at DATETIME NULL;"))
        db.session.commit()
        print("✅ Đã thêm cột reviewed_at (Thời gian duyệt) thành công!")
    except Exception as e:
        print("ℹ️ Cột reviewed_at đã tồn tại hoặc không cần thêm.")