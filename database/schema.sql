-- ==========================================
-- 1. LOOKUP & ORGANIZATIONAL TABLES
-- ==========================================

CREATE TABLE IF NOT EXISTS campuses (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS colleges (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    campus_id BIGINT NOT NULL REFERENCES campuses(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS departments (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    college_id BIGINT NOT NULL REFERENCES colleges(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS roles (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS school_years (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    year_from INT NOT NULL,
    year_to INT NOT NULL,
    UNIQUE(year_from, year_to)
);

CREATE TABLE IF NOT EXISTS semesters (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- ==========================================
-- 2. USERS & AUTHORS
-- ==========================================

CREATE TABLE IF NOT EXISTS users (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    department_id BIGINT REFERENCES departments(id) ON DELETE SET NULL,
    role_id BIGINT REFERENCES roles(id) ON DELETE RESTRICT,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS authors (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
    department_id BIGINT REFERENCES departments(id) ON DELETE SET NULL,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    last_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- 3. RESEARCH CORE & BRIDGES
-- ==========================================

CREATE TABLE IF NOT EXISTS research_types (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS research_output_types (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS research_papers (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    research_type_id BIGINT REFERENCES research_types(id) ON DELETE RESTRICT,
    research_output_type_id BIGINT REFERENCES research_output_types(id) ON DELETE RESTRICT,
    school_year_id BIGINT REFERENCES school_years(id) ON DELETE RESTRICT,
    semester_id BIGINT REFERENCES semesters(id) ON DELETE RESTRICT,
    title TEXT NOT NULL,
    abstract TEXT,
    keywords TEXT[],
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS research_authors (
    paper_id BIGINT REFERENCES research_papers(id) ON DELETE CASCADE,
    author_id BIGINT REFERENCES authors(id) ON DELETE CASCADE,
    is_primary_author BOOLEAN DEFAULT FALSE,
    author_order INT,
    PRIMARY KEY (paper_id, author_id)
);

-- ==========================================
-- 4. EXTENSIONS
-- ==========================================

CREATE TABLE IF NOT EXISTS research_evaluations (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    paper_id BIGINT UNIQUE REFERENCES research_papers(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'Pending',
    document_links JSONB,
    authorship_from_link TEXT,
    journal_conference_info JSONB,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS presentations (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    paper_id BIGINT UNIQUE REFERENCES research_papers(id) ON DELETE CASCADE,
    venue VARCHAR(255),
    conference_name VARCHAR(255),
    presentation_date DATE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS publications (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    paper_id BIGINT UNIQUE REFERENCES research_papers(id) ON DELETE CASCADE,
    doi VARCHAR(100) UNIQUE,
    manuscript_link TEXT,
    journal_publisher VARCHAR(255),
    volume VARCHAR(50),
    issue_number VARCHAR(50),
    page_number VARCHAR(50),
    publication_date DATE,
    indexing VARCHAR(255),
    cite_score DECIMAL(10,2),
    impact_factor DECIMAL(10,2),
    editorial_board TEXT,
    journal_website TEXT,
    apa_format TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
