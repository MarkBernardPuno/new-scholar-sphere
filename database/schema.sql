-- Create Colleges Table
CREATE TABLE IF NOT EXISTS colleges (
    college_id SERIAL PRIMARY KEY,
    college_name VARCHAR(255) NOT NULL,
    college_campus VARCHAR(255) NOT NULL
);

-- Create Departments Table
CREATE TABLE IF NOT EXISTS departments (
    dept_id SERIAL PRIMARY KEY,
    dept_name VARCHAR(255) NOT NULL
);

-- Create Roles Table
CREATE TABLE IF NOT EXISTS roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(100) NOT NULL UNIQUE
);

-- Create Campuses Table
CREATE TABLE IF NOT EXISTS campuses (
    campus_id SERIAL PRIMARY KEY,
    campus_name VARCHAR(255) NOT NULL
);

-- Create Indexes for better query performance

-- Users for JWT authentication
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role_id INTEGER REFERENCES roles(role_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Research status dictionary
CREATE TABLE IF NOT EXISTS statuses (
    status_id SERIAL PRIMARY KEY,
    status_name VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(255)
);

-- Researcher records
CREATE TABLE IF NOT EXISTS researchers (
    researcher_id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    department_id INTEGER REFERENCES departments(dept_id),
    campus_id INTEGER REFERENCES campuses(campus_id),
    status_id INTEGER REFERENCES statuses(status_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Author records
CREATE TABLE IF NOT EXISTS authors (
    author_id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    affiliation VARCHAR(255)
);

-- Research keywords
CREATE TABLE IF NOT EXISTS keywords (
    keyword_id SERIAL PRIMARY KEY,
    keyword_name VARCHAR(100) NOT NULL UNIQUE
);

-- Paper records
CREATE TABLE IF NOT EXISTS papers (
    paper_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    abstract TEXT,
    published_at TIMESTAMP WITH TIME ZONE,
    department_id INTEGER REFERENCES departments(dept_id),
    campus_id INTEGER REFERENCES campuses(campus_id),
    status_id INTEGER REFERENCES statuses(status_id),
    researcher_id INTEGER REFERENCES users(user_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Paper-author mapping
CREATE TABLE IF NOT EXISTS paper_authors (
    paper_id INTEGER NOT NULL REFERENCES papers(paper_id) ON DELETE CASCADE,
    author_id INTEGER NOT NULL REFERENCES authors(author_id) ON DELETE CASCADE,
    PRIMARY KEY (paper_id, author_id)
);

-- Paper-keyword mapping
CREATE TABLE IF NOT EXISTS paper_keywords (
    paper_id INTEGER NOT NULL REFERENCES papers(paper_id) ON DELETE CASCADE,
    keyword_id INTEGER NOT NULL REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    PRIMARY KEY (paper_id, keyword_id)
);

-- Agenda/work tracking
CREATE TABLE IF NOT EXISTS agendas (
    agenda_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    details TEXT,
    due_date TIMESTAMP WITH TIME ZONE,
    status_id INTEGER REFERENCES statuses(status_id),
    created_by INTEGER REFERENCES users(user_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Research outputs (requested schema)
CREATE TABLE IF NOT EXISTS research_outputs (
    paper_id SERIAL PRIMARY KEY,
    school_year_id VARCHAR(9) NOT NULL,
    semester_id VARCHAR(50) NOT NULL,
    research_output_type_id VARCHAR(50) NOT NULL CHECK (
        research_output_type_id IN ('Presentation', 'Publication', 'Intl Presentation', 'Intl Publication')
    ),
    research_title TEXT NOT NULL,
    research_type_id VARCHAR(100) NOT NULL,
    authors_id TEXT NOT NULL,
    college_id VARCHAR(100) NOT NULL,
    program_department_id VARCHAR(100) NOT NULL,

    presentation_venue VARCHAR(255),
    conference_name VARCHAR(255),
    presentation_abstract TEXT,
    presentation_keywords TEXT,

    doi VARCHAR(255) UNIQUE,
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
    publication_abstract TEXT,
    publication_keywords TEXT,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Research evaluations
CREATE TABLE IF NOT EXISTS research_evaluations (
    re_id SERIAL PRIMARY KEY,
    author_id TEXT NOT NULL,
    campus_id INTEGER NOT NULL REFERENCES campuses(campus_id),
    college_id INTEGER NOT NULL REFERENCES colleges(college_id),
    department_id VARCHAR(100) NOT NULL,
    school_year_id VARCHAR(50) NOT NULL,
    semester_id VARCHAR(50) NOT NULL,
    title_of_research VARCHAR(255) NOT NULL,
    authorship_form_link TEXT NOT NULL,
    evaluation_form TEXT NOT NULL,
    full_paper TEXT NOT NULL,
    turnitin_report TEXT NOT NULL,
    grammarly_report TEXT NOT NULL,
    journal_conference_info TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
