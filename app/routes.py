# ----------------------------------------------------
# 5. ĐƯỜNG DẪN XEM VÀ TẢI FILE MINH CHỨNG DÙNG CHUNG
# ----------------------------------------------------
@app.route("/uploads/<path:filename>")
def download_file(filename):
    from flask import send_from_directory
    
    # 1. Kiểm tra trong thư mục uploads của app
    upload_dir = os.path.join(app.root_path, "static", "uploads")
    if os.path.exists(os.path.join(upload_dir, filename)):
        return send_from_directory(upload_dir, filename)
        
    # 2. Kiểm tra trong thư mục gốc dự án (nơi chứa các file đính kèm từ Excel)
    root_dir = os.path.dirname(app.root_path)
    if os.path.exists(os.path.join(root_dir, filename)):
        return send_from_directory(root_dir, filename)

    return f"Không tìm thấy tệp minh chứng: {filename}", 404
