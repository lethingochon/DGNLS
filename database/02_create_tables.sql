/*
=========================================================
 DigiTeacher
 File: 02_create_tables.sql
 Author : GPT + User
=========================================================
*/

USE digiteacher;

-- =====================================================
-- 1. DEPARTMENT
-- =====================================================

CREATE TABLE department (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 2. ROLE
-- =====================================================

CREATE TABLE role (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    code VARCHAR(10) NOT NULL UNIQUE,

    name VARCHAR(100) NOT NULL

) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 3. SUBJECT
-- =====================================================

CREATE TABLE subject (

    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    code VARCHAR(10) NOT NULL UNIQUE,

    name VARCHAR(100) NOT NULL UNIQUE

) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 4. FIELD
-- =====================================================

CREATE TABLE field (

    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    code VARCHAR(20) NOT NULL UNIQUE,

    name VARCHAR(255) NOT NULL,

    display_order INT DEFAULT 0

) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;
-- =====================================================
-- 5. CRITERIA
-- =====================================================

CREATE TABLE criteria (

    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    field_id BIGINT UNSIGNED NOT NULL,

    code VARCHAR(20) NOT NULL UNIQUE,

    name VARCHAR(255) NOT NULL,

    description TEXT,

    max_score DECIMAL(5,2) DEFAULT 1.00,

    display_order INT DEFAULT 0,

    is_active BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_criteria_field
        FOREIGN KEY (field_id)
        REFERENCES field(id)

) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;
-- =====================================================
-- 6. TEACHER
-- =====================================================

CREATE TABLE teacher (

    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    magv VARCHAR(20) NOT NULL UNIQUE,

    full_name VARCHAR(100) NOT NULL,

    email VARCHAR(100) UNIQUE,

    password_hash VARCHAR(255) NOT NULL,

    department_id BIGINT UNSIGNED NOT NULL,

    subject_id BIGINT UNSIGNED NOT NULL,

    role_id BIGINT UNSIGNED NOT NULL,

    manager_id BIGINT UNSIGNED NULL,

    avatar VARCHAR(255),

    active BOOLEAN DEFAULT TRUE,

    last_login DATETIME NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_teacher_department
        FOREIGN KEY (department_id)
        REFERENCES department(id),

    CONSTRAINT fk_teacher_subject
        FOREIGN KEY (subject_id)
        REFERENCES subject(id),

    CONSTRAINT fk_teacher_role
        FOREIGN KEY (role_id)
        REFERENCES role(id),

    CONSTRAINT fk_teacher_manager
        FOREIGN KEY (manager_id)
        REFERENCES teacher(id)

) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;
-- =====================================================
-- =====================================================
-- -- =====================================================
-- 7. TEACHER_CRITERIA
-- =====================================================

CREATE TABLE teacher_criteria (

    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    teacher_id BIGINT UNSIGNED NOT NULL,

    criteria_id BIGINT UNSIGNED NOT NULL,

    status ENUM(
        'CHUA_THUC_HIEN',
        'DA_NOP',
        'DA_XAC_NHAN',
        'HOAN_THANH'
    ) DEFAULT 'CHUA_THUC_HIEN',

    leader_comment TEXT,

    principal_comment TEXT,

    submitted_at DATETIME,

    leader_reviewed_at DATETIME,

    principal_reviewed_at DATETIME,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_tc_teacher
        FOREIGN KEY (teacher_id)
        REFERENCES teacher(id),

    CONSTRAINT fk_tc_criteria
        FOREIGN KEY (criteria_id)
        REFERENCES criteria(id),

    CONSTRAINT uk_teacher_criteria
        UNIQUE (teacher_id, criteria_id)

) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;
-- =====================================================
-- 8. EVIDENCE
-- =====================================================
DROP TABLE IF EXISTS evidence;
CREATE TABLE evidence (

    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    title VARCHAR(255) NOT NULL,

    file_name VARCHAR(255) NOT NULL,

    file_path VARCHAR(500) NOT NULL,

    file_type VARCHAR(20) NOT NULL,

    file_size BIGINT UNSIGNED,

    uploaded_by BIGINT UNSIGNED NOT NULL,

    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP,

is_active BOOLEAN DEFAULT TRUE,

CONSTRAINT fk_evidence_teacher
    FOREIGN KEY (uploaded_by)
    REFERENCES teacher(id)


) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;
-- =====================================================
-- 9. TEACHER_CRITERIA_EVIDENCE
-- =====================================================

DROP TABLE IF EXISTS teacher_criteria_evidence;

CREATE TABLE teacher_criteria_evidence (

    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    teacher_criteria_id BIGINT UNSIGNED NOT NULL,

    evidence_id BIGINT UNSIGNED NOT NULL,

    display_order INT DEFAULT 1,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_tce_teacher_criteria
        FOREIGN KEY (teacher_criteria_id)
        REFERENCES teacher_criteria(id),

    CONSTRAINT fk_tce_evidence
        FOREIGN KEY (evidence_id)
        REFERENCES evidence(id),

    CONSTRAINT uk_teacher_criteria_evidence
        UNIQUE (teacher_criteria_id, evidence_id)

) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;