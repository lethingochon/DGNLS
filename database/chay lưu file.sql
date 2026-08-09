-- 1. Xử lý CSDL dgnlgv
USE dgnlgv;

DROP TABLE IF EXISTS teacher_criteria_evidence;
DROP TABLE IF EXISTS evidence;

CREATE TABLE evidence (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    storage_type VARCHAR(50),
    file_path TEXT
);

CREATE TABLE teacher_criteria_evidence (
    id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_criteria_id INT,
    evidence_id INT
);

-- 2. Xử lý CSDL digiteacher
USE digiteacher;

DROP TABLE IF EXISTS teacher_criteria_evidence;
DROP TABLE IF EXISTS evidence;

CREATE TABLE evidence (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    storage_type VARCHAR(50),
    file_path TEXT
);

CREATE TABLE teacher_criteria_evidence (
    id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_criteria_id INT,
    evidence_id INT
);