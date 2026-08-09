USE digiteacher;

-- =====================================================
-- 03. INSERT MASTER DATA
-- =====================================================
-- =====================================================
-- ROLE
-- =====================================================

INSERT INTO role(code, name)
VALUES
('ADMIN', 'Quản trị hệ thống'),
('HT', 'Hiệu trưởng'),
('HP', 'Hiệu phó'),
('TT', 'Tổ trưởng'),
('TP', 'Tổ phó'),
('GV', 'Giáo viên');
-- =====================================================
-- DEPARTMENT
-- =====================================================

password_hash
-- =====================================================
-- SUBJECT
-- =====================================================

INSERT INTO subject(code, name)
VALUES
('TOAN', 'Toán'),
('VAN', 'Ngữ văn'),
('TA', 'Tiếng Anh'),
('LY', 'Vật lí'),
('HOA', 'Hóa học'),
('SINH', 'Sinh học'),
('TIN', 'Tin học'),
('SU', 'Lịch sử'),
('DIA', 'Địa lí'),
('KTPL', 'GDKTPL'),
('CN', 'Công nghệ'),
('QPAN', 'GDQPAN'),
('TD', 'GD Thể chất'),
('KHMER', 'Tiếng KHMER');
-- =====================================================
-- FIELD
-- =====================================================

INSERT INTO field(code, name)
VALUES
('LV1', 'NĂNG LỰC SỬ DỤNG CÔNG NGHỆ SỐ'),
('LV2', 'THIẾT KẾ HỌC LIỆU SỐ'),
('LV3', 'TỔ CHỨC DẠY HỌC SỐ'),
('LV4', 'KIỂM TRA, ĐÁNH GIÁ'),
('LV5', 'ỨNG DỤNG AI'),
('LV6', 'AN TOÀN, BẢO MẬT VÀ ĐẠO ĐỨC SỐ'),
('LV7', 'CHIA SẺ, PHÁT TRIỂN CHUYÊN MÔN'),
('LV8', 'ĐỔI MỚI SÁNG TẠO');
-- =====================================================
-- CRITERIA
-- =====================================================

INSERT INTO criteria(code, field_id, name)
VALUES
('TC101',1,'Vận hành thiết bị số phục vụ công việc chuyên môn'),
('TC102',1,'Quản lý dữ liệu và tài nguyên số phục vụ giảng dạy'),
('TC103',1,'Thực hiện giao tiếp số trong công việc'),
('TC104',1,'Sử dụng nền tảng trực tuyến(zoom, google meet,Microsoft Teams..)'),
('TC105',1,'Tìm kiếm và khai thác thông tin số'),

('TC201',2,'Thiết kế học liệu số'),
('TC202',2,'Thiết kế bài trình chiếu số'),
('TC203',2,'Thiết kế video bài giảng số'),
('TC204',2,'Thiết kế học liệu số tương tác'),
('TC205',2,'Quản lý học liệu số'),

('TC301',3,'Sử dụng nền tảng số trong tổ chức dạy học'),
('TC302',3,'Giao và thu nhận nhiệm vụ học tập trực tuyến'),
('TC303',3,'Quản lý lớp học trên môi trường số'),
('TC304',3,'Theo dõi và hỗ trợ tiến độ học tập'),
('TC305',3,'Tương tác và trao đổi với người học trên môi trường số'),

('TC401',4,'Tổ chức kiểm tra, đánh giá trên môi trường số'),
('TC402',4,'Xây dựng và quản lý ngân hàng câu hỏi số'),
('TC403',4,'Phân tích kết quả đánh giá bằng công cụ số'),
('TC404',4,'Phản hồi kết quả học tập trên môi trường số'),
('TC405',4,'Quản lý và lưu trữ kết quả đánh giá số'),

('TC501',5,'AI hỗ trợ soạn bài'),
('TC502',5,'AI tạo câu hỏi'),
('TC503',5,'AI tạo học liệu'),
('TC504',5,'Ứng dụng AI trong phân tích dữ liệu giáo dục'),
('TC505',5,'Sử dụng AI có trách nhiệm và đạo đức'),

('TC601',6,'Bảo vệ tài khoản'),
('TC602',6,'Bảo vệ dữ liệu'),
('TC603',6,'Bản quyền số'),
('TC604',6,'Ứng xử số'),

('TC701',7,'Chia sẻ học liệu số và kinh nghiệm chuyên môn'),
('TC702',7,'Hỗ trợ đồng nghiệp'),
('TC703',7,'Tham gia tập huấn'),
('TC704',7,'Cộng đồng học tập'),

('TC801',8,'Sáng kiến/chuyển đổi số'),
('TC802',8,'Tham gia dự án số');