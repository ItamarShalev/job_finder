import sqlite3

# SQL commands to create tables
create_tables_sql = [
    """
    CREATE TABLE IF NOT EXISTS Position (
        linkdin_url VARCHAR(255) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        open_by VARCHAR(255) NOT NULL,
        company VARCHAR(255) NOT NULL,
        location VARCHAR(255),
        description TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS InterviewerType (
        type VARCHAR(2) PRIMARY KEY
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Interviewer (
        user_name VARCHAR(255) PRIMARY KEY,
        password VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        company VARCHAR(255) NOT NULL,
        phone VARCHAR(20),
        email VARCHAR(255),
        type VARCHAR(2),
        FOREIGN KEY (type) REFERENCES InterviewerType(type)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS InterviewerPositions (
        interviewer_user_name VARCHAR(255),
        position_linkdin_url VARCHAR(255),
        PRIMARY KEY (interviewer_user_name, position_linkdin_url),
        FOREIGN KEY (interviewer_user_name) REFERENCES Interviewer(user_name),
        FOREIGN KEY (position_linkdin_url) REFERENCES Position(linkdin_url)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Stage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reviewer VARCHAR(255),
        summery TEXT,
        score INT,
        type VARCHAR(255),
        FOREIGN KEY (reviewer) REFERENCES Interviewer(user_name)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Candidate (
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        phone VARCHAR(20) PRIMARY KEY,
        city VARCHAR(255),
        summery TEXT,
        bazz_words TEXT,
        resume_url VARCHAR(255),
        linkdin_url VARCHAR(255),
        github_url VARCHAR(255)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS CandidateStages (
        candidate_phone VARCHAR(20),
        position_linkdin_url VARCHAR(255),
        stage_id INT,
        PRIMARY KEY (candidate_phone, position_linkdin_url, stage_id),
        FOREIGN KEY (candidate_phone) REFERENCES Candidate(phone),
        FOREIGN KEY (position_linkdin_url) REFERENCES Position(linkdin_url),
        FOREIGN KEY (stage_id) REFERENCES Stage(id)
    );
    """
]


def initialize_database(db_file):
    # Connect to the database (it will create the file if it doesn't exist)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Execute SQL commands to create tables
    for sql in create_tables_sql:
        cursor.execute(sql)

    # Commit and close connection
    conn.commit()
    conn.close()
