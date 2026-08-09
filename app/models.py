from app import db

class Department(db.Model):
    __tablename__ = "department"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<Department {self.name}>"
class Role(db.Model):
    __tablename__ = "role"

    id = db.Column(db.BigInteger, primary_key=True)
    code = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f"<Role {self.code}>"
class Subject(db.Model):
    __tablename__ = "subject"

    id = db.Column(db.BigInteger, primary_key=True)
    code = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Subject {self.name}>"
class Teacher(db.Model):
    __tablename__ = "teacher"

    id = db.Column(db.BigInteger, primary_key=True)
    magv = db.Column(db.String(20), nullable=False, unique=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=False)

    role_id = db.Column(db.BigInteger, db.ForeignKey("role.id"))
    department_id = db.Column(db.BigInteger, db.ForeignKey("department.id"))
    subject_id = db.Column(db.BigInteger, db.ForeignKey("subject.id"))

    role = db.relationship("Role")
    department = db.relationship("Department")
    subject = db.relationship("Subject")

    def __repr__(self):
        return f"<Teacher {self.full_name}>"
class Field(db.Model):
    __tablename__ = "field"

    id = db.Column(db.BigInteger, primary_key=True)
    code = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Field {self.name}>"
class Criteria(db.Model):
    __tablename__ = "criteria"

    id = db.Column(db.BigInteger, primary_key=True)
    field_id = db.Column(db.BigInteger, db.ForeignKey("field.id"))

    code = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(500), nullable=False)

    description = db.Column(db.Text)
    max_score = db.Column(db.Float)

    display_order = db.Column(db.Integer)
    is_active = db.Column(db.Boolean)

    field = db.relationship("Field")

    def __repr__(self):
        return f"<Criteria {self.code}>"
class TeacherCriteria(db.Model):
    __tablename__ = "teacher_criteria"

    id = db.Column(db.BigInteger, primary_key=True)
    teacher_id = db.Column(db.BigInteger, db.ForeignKey("teacher.id"))
    criteria_id = db.Column(db.BigInteger, db.ForeignKey("criteria.id"))
    status = db.Column(db.String(50), default="CHUA_NOP")
    feedback = db.Column(db.Text, nullable=True)
    submitted_at = db.Column(db.DateTime, nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    # Bổ sung dòng này để Jinja2 gọi được item.evidences
    evidences = db.relationship("TeacherCriteriaEvidence", backref="teacher_criteria", lazy=True)
    teacher = db.relationship("Teacher")
    criteria = db.relationship("Criteria")
class Evidence(db.Model):
    __tablename__ = 'evidence'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=True)  # Sửa thành True để tránh bắt buộc
    storage_type = db.Column(db.String(50), default='FILE')  # Thêm default
    file_path = db.Column(db.Text, nullable=True)  # Bổ sung nullable=True
    url = db.Column(db.Text, nullable=True)

class TeacherCriteriaEvidence(db.Model):
    __tablename__ = "teacher_criteria_evidence"

    id = db.Column(db.BigInteger, primary_key=True)
    teacher_criteria_id = db.Column(db.BigInteger, db.ForeignKey("teacher_criteria.id"))
    evidence_id = db.Column(db.BigInteger, db.ForeignKey("evidence.id"))

    # Bổ sung dòng này để lấy thông tin chi tiết tệp minh chứng
    evidence = db.relationship("Evidence")