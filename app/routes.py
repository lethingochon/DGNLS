from sqlalchemy.orm import joinedload
from datetime import datetime, timezone, timedelta
import os
import io
import uuid
import re
import pandas as pd
from sqlalchemy import or_
from flask import render_template, request, redirect, url_for, session, flash, send_file, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash

# Khai báo các mô hình CSDL và kết nối app, db
from app import app, db
from app.models import (
    Teacher, 
    TeacherCriteria, 
    Criteria, 
    Field, 
    Evidence, 
    TeacherCriteriaEvidence, 
    Department, 
    Role,
    Subject
)

# Thư viện Cloudinary
import cloudinary
import cloudinary.uploader

# Múi giờ Việt Nam (UTC+7)
VN_TZ = timezone(timedelta(hours=7))

def get_vn_now():
    # Lấy giờ VN và bỏ tzinfo để lưu chính xác vào CSDL
    return datetime.now(VN_TZ).replace(tzinfo=None)

# Hàm chuyển đổi tiếng Việt có dấu thành không dấu an toàn cho Cloudinary
def sanitize_filename(filename):
    patterns = {
        '[àáảãạăắằẳẵặâấầẩẫậ]': 'a',
        '[đ]': 'd',
        '[èéẻẽẹêếềểễệ]': 'e',
        '[ìíỉĩị]': 'i',
        '[òóỏõọôốồổỗộơớờởỡợ]': 'o',
        '[ùúủũụưứừửữự]': 'u',
        '[ỳýỷỹỵ]': 'y'
    }
    output = filename.lower()
    for regex, sub in patterns.items():
        output = re.sub(regex, sub, output)
    clean_name = re.sub(r'[^a-zA-Z0-9_]', '_', output)
    return clean_name or "minh_chung"


# ----------------------------------------------------
# 1. TRANG ĐĂNG NHẬP & ĐĂNG XUẤT
# ----------------------------------------------------
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_input = (request.form.get("email") or request.form.get("username") or "").strip()
        password = request.form.get("password", "").strip()
        
        if not login_input:
            flash("Vui lòng nhập Email hoặc Mã GV!", "warning")
            return render_template("login.html")

        teacher = Teacher.query.filter(
            or_(
                db.func.lower(Teacher.email) == login_input.lower(),
                db.func.lower(Teacher.magv) == login_input.lower()
            )
        ).first()

        if not teacher:
            flash("Email hoặc Mã GV không tồn tại!", "danger")
        elif not check_password_hash(teacher.password_hash, password):
            flash("Mật khẩu không chính xác!", "danger")
        else:
            session["teacher_id"] = teacher.id
            session["teacher_name"] = teacher.full_name
            session["role_code"] = teacher.role.code if teacher.role else "GV"
            session["role_name"] = teacher.role.name if teacher.role else "GIÁO VIÊN"
            session["dept_name"] = teacher.department.name if teacher.department else ""

            if session["role_code"] in ["HT", "HP"]:
                return redirect(url_for("admin_dashboard"))
            elif session["role_code"] in ["TT", "TP"]:
                return redirect(url_for("department_review"))
            else:
                return redirect(url_for("my_criteria"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ----------------------------------------------------
# 2. DASHBOARD BGH, XUẤT EXCEL & THẨM ĐỊNH TỔ TRƯỞNG
# ----------------------------------------------------
@app.route("/admin/dashboard")
def admin_dashboard():
    teacher_id = session.get("teacher_id")
    role_code = session.get("role_code")

    if not teacher_id or role_code not in ["HT", "HP"]:
        flash("Trang này dành riêng cho Ban Giám Hiệu!", "warning")
        return redirect(url_for("login"))

    try:
        all_teachers = Teacher.query.all()
        official_teachers = [
            t for t in all_teachers 
            if not (t.role and t.role.code in ["HT", "HP"]) 
        ]
        total_teachers = len(official_teachers)
        official_teacher_ids = [t.id for t in official_teachers]

        total_records = TeacherCriteria.query.filter(TeacherCriteria.teacher_id.in_(official_teacher_ids)).count() if official_teacher_ids else 0
        total_approved = TeacherCriteria.query.filter(TeacherCriteria.teacher_id.in_(official_teacher_ids), TeacherCriteria.status == "DA_XAC_NHAN").count() if official_teacher_ids else 0
        total_pending = TeacherCriteria.query.filter(TeacherCriteria.teacher_id.in_(official_teacher_ids), TeacherCriteria.status == "DA_NOP").count() if official_teacher_ids else 0

        school_progress = round((total_approved / total_records) * 100, 1) if total_records > 0 else 0

        departments = Department.query.all()
        dept_stats = []

        for dept in departments:
            dept_teachers = [t for t in official_teachers if t.department_id == dept.id]
            dept_teacher_ids = [t.id for t in dept_teachers]
            
            leader = Teacher.query.filter_by(department_id=dept.id).join(Role).filter(Role.code.in_(["TT", "TP"])).first()
            leader_name = leader.full_name if leader else "Chưa phân công"

            if dept_teacher_ids:
                dept_total_crit = TeacherCriteria.query.filter(TeacherCriteria.teacher_id.in_(dept_teacher_ids)).count()
                dept_approved = TeacherCriteria.query.filter(
                    TeacherCriteria.teacher_id.in_(dept_teacher_ids),
                    TeacherCriteria.status == "DA_XAC_NHAN"
                ).count()
                dept_pending = TeacherCriteria.query.filter(
                    TeacherCriteria.teacher_id.in_(dept_teacher_ids),
                    TeacherCriteria.status == "DA_NOP"
                ).count()
                dept_reviewed = TeacherCriteria.query.filter(
                    TeacherCriteria.teacher_id.in_(dept_teacher_ids),
                    TeacherCriteria.status.in_(["DA_XAC_NHAN", "TU_CHOI"])
                ).count()
            else:
                dept_total_crit, dept_reviewed, dept_pending, dept_approved = 0, 0, 0, 0

            dept_progress = round((dept_approved / dept_total_crit) * 100, 1) if dept_total_crit > 0 else 0

            # 1. Gom danh sách chi tiết từng giáo viên trong tổ
            teacher_list = []
            for t in dept_teachers:
                t_criterias = TeacherCriteria.query.filter_by(teacher_id=t.id).all()
                t_total = len(t_criterias)
                t_appr = sum(1 for tc in t_criterias if tc.status == "DA_XAC_NHAN")
                t_pend = sum(1 for tc in t_criterias if tc.status == "DA_NOP")
                t_prog = round((t_appr / t_total) * 100, 1) if t_total > 0 else 0.0

                teacher_list.append({
                    "id": t.id,
                    "magv": t.magv,
                    "full_name": t.full_name,
                    "approved": t_appr,
                    "pending": t_pend,
                    "total": t_total,
                    "total_tc": t_total,
                    "progress": t_prog,
                    "percent": t_prog
                })

            # 2. Lưu vào dept_stats
            dept_stats.append({
                "id": dept.id,
                "name": dept.name,
                "teacher_count": len(dept_teachers),
                "leader": leader_name,
                "head_name": leader_name,
                "total_crit": dept_total_crit,
                "total": dept_total_crit,
                "reviewed": dept_reviewed,
                "pending": dept_pending,
                "dept_pending": dept_pending,
                "approved": dept_approved,
                "dept_approved": dept_approved,
                "progress": dept_progress,
                "dept_percent": dept_progress,
                "teachers": teacher_list,
                "teacher_list": teacher_list
            })

    except Exception as e:
        print("LỖI DASHBOARD BGH:", e)
        total_teachers, total_approved, total_pending, school_progress = 0, 0, 0, 0
        dept_stats = []

    return render_template(
        "admin/dashboard.html",
        total_teachers=total_teachers,
        total_approved=total_approved,
        total_pending=total_pending,
        school_progress=school_progress,
        dept_stats=dept_stats
    )

@app.route("/admin/review-heads")
def admin_review_heads():
    teacher_id = session.get("teacher_id")
    role_code = session.get("role_code")

    if not teacher_id or role_code not in ["HT", "HP"]:
        flash("Trang này dành riêng cho Ban Giám Hiệu duyệt minh chứng Tổ trưởng!", "warning")
        return redirect(url_for("admin_dashboard"))

    tt_roles = Role.query.filter(Role.code.in_(["TT", "TP"])).all()
    tt_role_ids = [r.id for r in tt_roles]

    head_teachers = Teacher.query.filter(Teacher.role_id.in_(tt_role_ids)).all()
    head_teacher_ids = [t.id for t in head_teachers]

    records = TeacherCriteria.query.filter(
        TeacherCriteria.teacher_id.in_(head_teacher_ids),
        TeacherCriteria.status.in_(["DA_NOP", "DA_XAC_NHAN", "TU_CHOI"])
    ).all()

    review_list = []
    for r in records:
        tc_evidences = TeacherCriteriaEvidence.query.filter_by(teacher_criteria_id=r.id).all()
        ev_list = []
        for tc_ev in tc_evidences:
            if tc_ev.evidence:
                ev_list.append({
                    "id": tc_ev.evidence.id,
                    "file_path": tc_ev.evidence.file_path,
                    "url": tc_ev.evidence.url,
                    "title": tc_ev.evidence.title,
                    "storage_type": getattr(tc_ev.evidence, "storage_type", "FILE")
                })

        review_list.append({
            "id": r.id,
            "teacher_name": r.teacher.full_name,
            "teacher_magv": r.teacher.magv,
            "dept_name": r.teacher.department.name if r.teacher.department else "Chưa phân tổ",
            "criteria_code": r.criteria.code if r.criteria else "",
            "criteria_name": r.criteria.name if r.criteria else "",
            "status": r.status,
            "feedback": r.feedback,
            "evidences": ev_list
        })

    return render_template("admin/review_heads.html", review_list=review_list)

@app.route("/admin/export-excel")
def export_excel():
    try:
        all_teachers = Teacher.query.all()
        official_teachers = [
            t for t in all_teachers 
            if not (t.role and t.role.code in ["HT", "HP"]) 
        ]

        report_data = []
        for idx, teacher in enumerate(official_teachers, start=1):
            dept_name = teacher.department.name if teacher.department else "Chưa phân tổ"
            total_crit = TeacherCriteria.query.filter_by(teacher_id=teacher.id).count()
            approved_crit = TeacherCriteria.query.filter_by(teacher_id=teacher.id, status="DA_XAC_NHAN").count()
            pending_crit = TeacherCriteria.query.filter_by(teacher_id=teacher.id, status="DA_NOP").count()
            progress = f"{round((approved_crit / total_crit) * 100)}%" if total_crit > 0 else "0%"

            report_data.append({
                "STT": idx,
                "Mã GV": teacher.magv,
                "Họ và Tên": teacher.full_name,
                "Tổ Chuyên Môn": dept_name,
                "Tiêu Chí Đã Đạt": approved_crit,
                "Tiêu Chí Chờ Duyệt": pending_crit,
                "Tỷ Lệ Hoàn Thành": progress
            })

        df = pd.DataFrame(report_data)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Bao_Cao_Kiem_Dinh')
        output.seek(0)

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='Bao_Cao_Kiem_Dinh_2026.xlsx'
        )
    except Exception as e:
        return f"Không thể xuất báo cáo: {e}", 500


# ----------------------------------------------------
# 3. MÀN HÌNH GIÁO VIÊN (NỘP & QUẢN LÝ MINH CHỨNG)
# ----------------------------------------------------
@app.route("/teacher/my-criteria")
def my_criteria():
    teacher_id = session.get("teacher_id")
    if not teacher_id:
        return redirect(url_for("login"))

    records = (
        TeacherCriteria.query
        .options(
            joinedload(TeacherCriteria.evidences)
            .joinedload(TeacherCriteriaEvidence.evidence)
        )
        .filter_by(teacher_id=teacher_id)
        .all()
    )

    criteria_list = []
    completed_count = 0

    for r in records:
        if r.status == "DA_XAC_NHAN":
            completed_count += 1

        ev_list = []
        for tc_ev in r.evidences:
            if tc_ev.evidence:
                ev_list.append({
                    "id": tc_ev.evidence.id,
                    "file_path": tc_ev.evidence.file_path,
                    "url": tc_ev.evidence.url,
                    "title": tc_ev.evidence.title,
                    "storage_type": getattr(tc_ev.evidence, "storage_type", "FILE")
                })

        criteria_list.append({
            "id": r.id,
            "criteria_code": r.criteria.code if r.criteria else "",
            "criteria_name": r.criteria.name if r.criteria else "",
            "field_name": r.criteria.field.name if r.criteria and r.criteria.field else "",
            "status": r.status,
            "feedback": getattr(r, "feedback", None),
            "submitted_at": getattr(r, "submitted_at", None),
            "reviewed_at": getattr(r, "reviewed_at", None),
            "evidences": ev_list
        })

    criteria_list.sort(key=lambda x: x["criteria_code"])

    return render_template(
        "teacher/my_criteria.html",
        criteria_list=criteria_list,
        completed_count=completed_count,
        total_count=len(records)
    )

@app.route("/teacher/submit-evidence", methods=["POST"])
def submit_evidence():
    try:
        tc_id = request.form.get("criteria_id")
        file = request.files.get("evidence_file")
        url_input = request.form.get("evidence_url")

        tc = TeacherCriteria.query.get(tc_id)
        if not tc:
            flash("Không tìm thấy tiêu chí cần nộp!", "danger")
            return redirect(url_for("my_criteria"))

        file_path = None
        storage_type = "URL"
        filename = None

        # 1. Xử lý Upload file lên Cloudinary an toàn tuyệt đối
        if file and file.filename != "":
            original_filename = file.filename
            filename = original_filename
            
            raw_name, file_ext = os.path.splitext(original_filename)
            file_ext = file_ext.lower()
            
            # Làm sạch tên tiếng Việt tránh lỗi Cloudinary
            safe_name = sanitize_filename(raw_name)
            unique_id = f"{safe_name}_{uuid.uuid4().hex[:6]}"

            raw_extensions = ['.xlsx', '.xls', '.docx', '.doc', '.pptx', '.ppt', '.zip', '.rar', '.txt']
            res_type = "raw" if file_ext in raw_extensions else "auto"

            try:
                final_public_id = f"{unique_id}{file_ext}" if res_type == "raw" else unique_id

                upload_result = cloudinary.uploader.upload(
                    file,
                    resource_type=res_type,
                    folder="minh_chung_dgnls",
                    public_id=final_public_id
                )
                file_path = upload_result.get("secure_url")
                storage_type = "FILE"
            except Exception as upload_err:
                print("LỖI CLOUDINARY UPLOAD:", upload_err)
                flash(f"Lỗi khi tải file lên kho lưu trữ: {upload_err}", "danger")
                return redirect(url_for("my_criteria"))

        evidence_title = filename if filename else (url_input if url_input else f"Minh chứng {tc.criteria.code if tc.criteria else ''}")
        final_url = file_path if file_path else url_input

        # 2. Lưu thông tin vào CSDL
        if file_path or url_input:
            ev = Evidence(
                title=evidence_title,
                storage_type=storage_type,
                file_path=file_path,
                url=final_url
            )
            db.session.add(ev)
            db.session.flush()

            # Liên kết bảng trung gian
            tc_ev = TeacherCriteriaEvidence(
                teacher_criteria_id=tc.id,
                evidence_id=ev.id
            )
            db.session.add(tc_ev)

            # Cập nhật trạng thái tiêu chí
            tc.status = "DA_NOP"
            try:
                tc.submitted_at = get_vn_now()
            except Exception:
                tc.submitted_at = datetime.utcnow()
            tc.feedback = None

            db.session.commit()
            flash("Nộp minh chứng thành công!", "success")
        else:
            flash("Vui lòng chọn file hoặc nhập đường dẫn liên kết!", "warning")

    except Exception as e:
        db.session.rollback()
        print("LỖI TỔNG THỂ SUBMIT EVIDENCE:", e)
        flash(f"Có lỗi xảy ra: {e}", "danger")

    return redirect(url_for("my_criteria"))

@app.route("/teacher/delete-evidence/<int:tc_id>/<int:evidence_id>", methods=["POST"])
def delete_evidence(tc_id, evidence_id):
    teacher_id = session.get("teacher_id")
    if not teacher_id:
        return redirect(url_for("login"))

    tc = TeacherCriteria.query.get(tc_id)
    if tc and tc.teacher_id == teacher_id:
        tc_ev = TeacherCriteriaEvidence.query.filter_by(teacher_criteria_id=tc.id, evidence_id=evidence_id).first()
        if tc_ev:
            ev = Evidence.query.get(evidence_id)
            db.session.delete(tc_ev)
            if ev:
                db.session.delete(ev)
            db.session.commit()

        remaining = TeacherCriteriaEvidence.query.filter_by(teacher_criteria_id=tc.id).count()
        if remaining == 0:
            tc.status = "CHUA_NOP"
            tc.feedback = None
            db.session.commit()

    return redirect(url_for("my_criteria"))


# ----------------------------------------------------
# 4. TỔ TRƯỞNG THẨM ĐỊNH & QUẢN LÝ GIÁO VIÊN
# ----------------------------------------------------
@app.route("/department/update-status", methods=["POST"])
def update_status():
    record_id = request.form.get("record_id")
    status = request.form.get("status")
    feedback = request.form.get("feedback")

    tc = TeacherCriteria.query.get(record_id)
    if tc:
        tc.status = status
        tc.feedback = feedback
        tc.reviewed_at = get_vn_now()
        db.session.commit()

    return redirect(request.referrer or url_for("department_review"))

@app.route("/department/review")
def department_review():
    teacher_id = session.get("teacher_id")
    if not teacher_id:
        return redirect(url_for("login"))

    current_teacher = Teacher.query.get(teacher_id)
    if not current_teacher or not current_teacher.role or current_teacher.role.code not in ["TT", "TP"]:
        return "Bạn không có quyền truy cập!", 403

    dept_id = current_teacher.department_id
    if not dept_id:
        return render_template("department/review.html", grouped_reviews=[], dept_name="Tổ Chuyên Môn")

    teachers_in_dept = Teacher.query.filter_by(department_id=dept_id).all()

    grouped_reviews = []
    total_dept_approved = 0
    total_dept_pending = 0

    for teacher in teachers_in_dept:
        tcs = TeacherCriteria.query.filter_by(teacher_id=teacher.id).all()

        total_crit = len(tcs)
        approved_count = 0
        pending_count = 0
        rejected_count = 0
        not_submitted_count = 0

        criterias_list = []
        for tc in tcs:
            if tc.status == "DA_XAC_NHAN":
                approved_count += 1
            elif tc.status == "DA_NOP":
                pending_count += 1
            elif tc.status == "TU_CHOI":
                rejected_count += 1
            else:
                not_submitted_count += 1

            if tc.status != "CHUA_NOP":
                evidences = []
                tc_evs = TeacherCriteriaEvidence.query.filter_by(teacher_criteria_id=tc.id).all()
                for tcev in tc_evs:
                    if tcev.evidence:
                        evidences.append({
                            "file_path": tcev.evidence.file_path,
                            "url": tcev.evidence.url
                        })

                criterias_list.append({
                    "id": tc.id,
                    "criteria_code": tc.criteria.code if tc.criteria else "",
                    "criteria_name": tc.criteria.name if tc.criteria else "",
                    "status": tc.status,
                    "feedback": tc.feedback,
                    "submitted_at": tc.submitted_at,
                    "reviewed_at": tc.reviewed_at,
                    "evidences": evidences
                })

        progress = round((approved_count / total_crit) * 100, 1) if total_crit > 0 else 0

        total_dept_approved += approved_count
        total_dept_pending += pending_count

        grouped_reviews.append({
            "teacher_id": teacher.id,
            "teacher_name": teacher.full_name,
            "teacher_magv": teacher.magv,
            "subject_name": teacher.subject.name if teacher.subject else "",
            "total_crit": total_crit,
            "approved_count": approved_count,
            "pending_count": pending_count,
            "rejected_count": rejected_count,
            "not_submitted_count": not_submitted_count,
            "progress": progress,
            "criterias": criterias_list
        })

    return render_template(
        "department/review.html",
        grouped_reviews=grouped_reviews,
        dept_name=current_teacher.department.name if current_teacher.department else "Tổ Chuyên Môn",
        total_dept_approved=total_dept_approved,
        total_dept_pending=total_dept_pending
    )

@app.route("/admin/manage-teachers")
def manage_teachers():
    teacher_id = session.get("teacher_id")
    role_code = session.get("role_code")
    if not teacher_id or role_code not in ["HT", "HP"]:
        return "Bạn không có quyền truy cập!", 403

    teachers = Teacher.query.order_by(Teacher.department_id).all()
    departments = Department.query.all()
    roles = Role.query.all()

    return render_template(
        "admin/manage_teachers.html",
        teachers=teachers,
        departments=departments,
        roles=roles
    )

@app.route("/admin/assign-role", methods=["POST"])
def assign_role():
    target_teacher_id = request.form.get("teacher_id")
    new_dept_id = request.form.get("department_id")
    new_role_code = request.form.get("role_code")

    teacher = Teacher.query.get(target_teacher_id)
    if teacher:
        if new_role_code == "TT" and new_dept_id:
            role_tt = Role.query.filter_by(code="TT").first()
            role_gv = Role.query.filter_by(code="GV").first()
            
            old_leaders = Teacher.query.filter_by(department_id=new_dept_id, role_id=role_tt.id).all()
            for old_leader in old_leaders:
                old_leader.role_id = role_gv.id

            teacher.role_id = role_tt.id
            teacher.department_id = new_dept_id
        else:
            role_obj = Role.query.filter_by(code=new_role_code).first()
            if role_obj:
                teacher.role_id = role_obj.id
            if new_dept_id:
                teacher.department_id = new_dept_id

        db.session.commit()
        flash(f"Đã cập nhật phân công cho {teacher.full_name}!", "success")

    return redirect(url_for("manage_teachers"))

@app.route("/admin/add-teacher", methods=["GET", "POST"])
def add_teacher():
    if request.method == "POST":
        magv = request.form.get("magv", "").strip()
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        dept_id = request.form.get("department_id")
        role_code = request.form.get("role_code", "GV")
        subject_id = request.form.get("subject_id")

        if not magv or not full_name:
            flash("Vui lòng nhập đầy đủ Mã GV và Họ tên!", "warning")
            return redirect(url_for("manage_teachers"))

        if Teacher.query.filter_by(magv=magv).first():
            flash("Mã Giáo viên này đã tồn tại trong hệ thống!", "danger")
            return redirect(url_for("manage_teachers"))

        final_email = email if email else f"{magv.lower()}@thpt.edu.vn"
        if Teacher.query.filter_by(email=final_email).first():
            flash(f"Email '{final_email}' đã được sử dụng bởi giáo viên khác!", "danger")
            return redirect(url_for("manage_teachers"))

        try:
            department_id = int(dept_id) if (dept_id and str(dept_id).isdigit()) else None
            
            sub_id = int(subject_id) if (subject_id and str(subject_id).isdigit()) else None
            if not sub_id:
                first_subject = Subject.query.first()
                sub_id = first_subject.id if first_subject else None

            role = Role.query.filter_by(code=role_code).first()
            role_id = role.id if role else 5

            new_teacher = Teacher(
                magv=magv,
                full_name=full_name,
                email=final_email,
                password_hash=generate_password_hash("123456"),
                department_id=department_id,
                subject_id=sub_id,
                role_id=role_id
            )
            db.session.add(new_teacher)
            db.session.commit()

            # Tự động gán toàn bộ Tiêu chí kiểm định
            all_criterias = Criteria.query.all()
            new_tc_list = [
                TeacherCriteria(teacher_id=new_teacher.id, criteria_id=c.id, status="CHUA_NOP")
                for c in all_criterias
            ]
            if new_tc_list:
                db.session.bulk_save_objects(new_tc_list)
                db.session.commit()

            flash(f"Thêm thành công giáo viên {full_name} ({magv})! Mật khẩu mặc định: 123456", "success")

        except Exception as e:
            db.session.rollback()
            print(f">>> LỖI THÊM GV: {e}", flush=True)
            flash(f"Đã xảy ra lỗi hệ thống khi lưu CSDL: {e}", "danger")

        return redirect(url_for("manage_teachers"))

    departments = Department.query.all()
    subjects = Subject.query.all()
    roles = Role.query.all()
    return render_template("admin/add_teacher.html", departments=departments, subjects=subjects, roles=roles)

@app.route("/admin/delete-teacher/<int:teacher_id>", methods=["POST"])
def delete_teacher(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    if teacher:
        tc_list = TeacherCriteria.query.filter_by(teacher_id=teacher.id).all()
        for tc in tc_list:
            TeacherCriteriaEvidence.query.filter_by(teacher_criteria_id=tc.id).delete()
            db.session.delete(tc)
        
        db.session.delete(teacher)
        db.session.commit()
        flash(f"Đã xóa thành công Giáo viên {teacher.full_name}!", "success")

    return redirect(url_for("manage_teachers"))


# ----------------------------------------------------
# 5. ĐƯỜNG DẪN XEM VÀ TẢI FILE MINH CHỨNG DÙNG CHUNG
# ----------------------------------------------------
@app.route("/uploads/<path:filename>")
def download_file(filename):
    upload_dir = os.path.join(app.root_path, "static", "uploads")
    if os.path.exists(os.path.join(upload_dir, filename)):
        return send_from_directory(upload_dir, filename)
        
    root_dir = os.path.dirname(app.root_path)
    if os.path.exists(os.path.join(root_dir, filename)):
        return send_from_directory(root_dir, filename)

    return f"Không tìm thấy tệp minh chứng: {filename}", 404
