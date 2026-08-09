-- DỮ LIỆU GIÁO VIÊN


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'tinhon',
'LÊ THỊ NGỌC HƠN',
'lethingochon.dtnt@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='GV'),
(SELECT id FROM department WHERE name='Tổ Tổng hợp'),
(SELECT id FROM subject WHERE code='TIN')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'cnquoc',
'LÊ PHÚ QUỐC',
'phuquoc.ipebl@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='TT'),
(SELECT id FROM department WHERE name='Tổ Tổng hợp'),
(SELECT id FROM subject WHERE code='CN')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'anqphue',
'TỐNG THỊ TUYẾT HUỆ',
'ttthuedtnt@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='GV'),
(SELECT id FROM department WHERE name='Tổ Tổng hợp'),
(SELECT id FROM subject WHERE code='QPAN')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'tdsung',
'DANH SUNG',
'danhsung1991@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='TP'),
(SELECT id FROM department WHERE name='Tổ Tổng hợp'),
(SELECT id FROM subject WHERE code='TD')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'tdchuyen',
'TĂNG CHUYỀN',
'tangchuyen2214@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='GV'),
(SELECT id FROM department WHERE name='Tổ Tổng hợp'),
(SELECT id FROM subject WHERE code='TD')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'tinthiem',
'NGUYỄN MINH THIỀM',
'minhthiem.cdn@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='GV'),
(SELECT id FROM department WHERE name='Tổ Tổng hợp'),
(SELECT id FROM subject WHERE code='TIN')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'toanyen',
'NNGUYỄN THỊ YẾN',
'thiyennguyen1981@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='TT'),
(SELECT id FROM department WHERE name='Tổ Tự nhiên'),
(SELECT id FROM subject WHERE code='TOAN')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'toanrinh',
'TTHẠCH THỊ KHEMARINH',
'rinh1983@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='GV'),
(SELECT id FROM department WHERE name='Tổ Tự nhiên'),
(SELECT id FROM subject WHERE code='TOAN')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'toanthao',
'TRỊNH THÀNH THẢO',
'thanhtrinh2103@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='GV'),
(SELECT id FROM department WHERE name='Tổ Tự nhiên'),
(SELECT id FROM subject WHERE code='TOAN')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'toanthi',
'TĂNG RA THI',
'tangrathi1977@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='GV'),
(SELECT id FROM department WHERE name='Tổ Tự nhiên'),
(SELECT id FROM subject WHERE code='TOAN')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'toanni',
'HỨA THỊ KIỀU NI',
'htkni.tt@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='GV'),
(SELECT id FROM department WHERE name='Tổ Tự nhiên'),
(SELECT id FROM subject WHERE code='TOAN')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'tachauhung',
'CHÂU VƯƠNG ANH HÙNG',
'chauvuonganhhung@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='TT'),
(SELECT id FROM department WHERE name='Tổ Ngoại ngữ'),
(SELECT id FROM subject WHERE code='TA')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'khmernha',
'LÂM THANH NHÃ',
'nhathanhlamda10vdt@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='TP'),
(SELECT id FROM department WHERE name='Tổ Ngoại ngữ'),
(SELECT id FROM subject WHERE code='KHMER')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'tavanhung',
'TRẦN VĂN HƯNG',
'tranvanhungbl72@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='GV'),
(SELECT id FROM department WHERE name='Tổ Ngoại ngữ'),
(SELECT id FROM subject WHERE code='TA')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'tahanh',
'PHẠM THỊ NGỌC HẠNH',
'ptngochanh1978@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='GV'),
(SELECT id FROM department WHERE name='Tổ Ngoại ngữ'),
(SELECT id FROM subject WHERE code='TA')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'khmerngoan',
'DANH THỊ BÉ NGOAN',
'utngoanchelsea@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='GV'),
(SELECT id FROM department WHERE name='Tổ Ngoại ngữ'),
(SELECT id FROM subject WHERE code='KHMER')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'khmerloc',
'MAI HỮU LỘC',
'maihuuloc150593@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='GV'),
(SELECT id FROM department WHERE name='Tổ Ngoại ngữ'),
(SELECT id FROM subject WHERE code='KHMER')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'tauyen',
'HỒ THỊ LÊ UYÊN',
'hothileuyen1905@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='GV'),
(SELECT id FROM department WHERE name='Tổ Ngoại ngữ'),
(SELECT id FROM subject WHERE code='TA')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'diahuynh',
'LÂM TÚ HUỲNH',
'lamtuhuynh040602@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='GV'),
(SELECT id FROM department WHERE name='Tổ Xã hội'),
(SELECT id FROM subject WHERE code='DIA')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'suxuyen',
'NGUYỄN THỊ XUYÊN',
'ntxuyen515@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='GV'),
(SELECT id FROM department WHERE name='Tổ Xã hội'),
(SELECT id FROM subject WHERE code='SU')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'susang',
'DANH SANG',
'sang050480@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='GV'),
(SELECT id FROM department WHERE name='Tổ Xã hội'),
(SELECT id FROM subject WHERE code='SU')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'diahuong',
'CAO THỊ TÚY HƯỜNG',
'caotuyhuong@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='GV'),
(SELECT id FROM department WHERE name='Tổ Xã hội'),
(SELECT id FROM subject WHERE code='DIA')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'ktplxuyen',
'TRƯƠNG BẢO XUYÊN',
'truongxuyen82@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='GV'),
(SELECT id FROM department WHERE name='Tổ Xã hội'),
(SELECT id FROM subject WHERE code='KTPL')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'vankim',
'VŨ BÍCH KIM',
'vubichkimbl@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='TT'),
(SELECT id FROM department WHERE name='Tổ Xã hội'),
(SELECT id FROM subject WHERE code='VAN')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'vanlanh',
'LÊ THỊ LANH',
'lethilanh1987bl@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='GV'),
(SELECT id FROM department WHERE name='Tổ Xã hội'),
(SELECT id FROM subject WHERE code='VAN')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'vankien',
'NGUYỄN HOÀNG KIÊN',
'nguyenhoangkienhb@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='GV'),
(SELECT id FROM department WHERE name='Tổ Xã hội'),
(SELECT id FROM subject WHERE code='VAN')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'vanchi',
'HOÀNG THỊ KIM CHI',
'hoangchi171@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='GV'),
(SELECT id FROM department WHERE name='Tổ Xã hội'),
(SELECT id FROM subject WHERE code='VAN')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'vanvinh',
'QUÁCH TẤN VINH',
'qtvinhthcstp.dh@sobaclieu.edu.vn',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='GV'),
(SELECT id FROM department WHERE name='Tổ Xã hội'),
(SELECT id FROM subject WHERE code='VAN')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'lycan',
'LÝ THANH CẦN',
'lythanhcandtnt@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='TP'),
(SELECT id FROM department WHERE name='Tổ Tự nhiên'),
(SELECT id FROM subject WHERE code='LY')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'lytran',
'TRẦN TRUNG TRẬN',
'ttran771@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='GV'),
(SELECT id FROM department WHERE name='Tổ Tự nhiên'),
(SELECT id FROM subject WHERE code='LY')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'lythoang',
'BÙI PHI THOÀNG',
'phithoangbui@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='GV'),
(SELECT id FROM department WHERE name='Tổ Tự nhiên'),
(SELECT id FROM subject WHERE code='LY')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'hoathuy',
'TRẦN NHƯ THUỶ',
'nguyetthuy1979@gmail,com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='TT'),
(SELECT id FROM department WHERE name='Tổ Tự nhiên'),
(SELECT id FROM subject WHERE code='HOA')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'hoaly',
'NGÔ THỊ LÝ',
'baply82@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='GV'),
(SELECT id FROM department WHERE name='Tổ Tự nhiên'),
(SELECT id FROM subject WHERE code='HOA')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'sinhhang',
'THẠCH THỊ THUÝ HẰNG',
'thachthithuyhang011099@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='GV'),
(SELECT id FROM department WHERE name='Tổ Tự nhiên'),
(SELECT id FROM subject WHERE code='SINH')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'hphung',
'LÂM VĂN HÙNG',
'lamvanhung.dtnt1969@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='HP'),
(SELECT id FROM department WHERE name='Tổ Tự nhiên'),
(SELECT id FROM subject WHERE code='LY')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'hphuu',
'NGUYỄN CHƠN NHẤT HỮU',
'ncnhuu83@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='HP'),
(SELECT id FROM department WHERE name='Tổ Tự nhiên'),
(SELECT id FROM subject WHERE code='LY')
);


INSERT INTO teacher
(magv, full_name, email, password_hash, role_id, department_id, subject_id)
VALUES
(
'htkiet',
'DƯ QUỐC KIỆT',
'duquockiet@gmail.com',
'scrypt:32768:8:1$X8nCVsmeUo4thJQY$b6f2c12d4b6c6151e31973eadddca76c1c4d131c48b980632b434f97a4575b1172b3ca9bb2be71e3c7f83397045d112fdeb92a00bd573f1bfe29e61fb42fc249',
(SELECT id FROM role WHERE code='HT'),
(SELECT id FROM department WHERE name='Tổ Xã hội'),
(SELECT id FROM subject WHERE code='DIA')
);

