from app import app, db
from sqlalchemy import text

with app.app_context():
    db.session.execute(text('ALTER TABLE teacher_criteria MODIFY COLUMN status VARCHAR(50) DEFAULT "CHUA_NOP";'))
    db.session.commit()
    print("✅ Đã mở rộng độ dài cột status thành công!")