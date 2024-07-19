import os
import sqlite3
from typing import List, Dict, Any, Tuple
from model.candidate import Candidate
from model.interviewer import Interviewer, InterviewerType
from model.position import Position
from model.stage import Stage

db_file = 'departments.db'

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


class Department:
    def __init__(self):
        self.db_file = db_file
        self.database(db_file)

    def database(self, db_file: str):
        # Check if the database file exists
        if not os.path.exists(db_file):
            print(f"Database file '{db_file}' does not exist. Creating and initializing the database.")
            self.initialize_database(db_file)
        else:
            # Connect to the existing database
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            # Check if tables exist and create them if not
            for sql in create_tables_sql:
                cursor.execute(sql)
            # Commit and close connection
            conn.commit()
            conn.close()
            print(f"Database file '{db_file}' exists. Checked and ensured all tables are present.")
        print("Database initialization complete.")

    def initialize_database(self, db_file):
        # Connect to the database (it will create the file if it doesn't exist)
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Execute SQL commands to create tables
        for sql in create_tables_sql:
            cursor.execute(sql)

        # Commit and close connection
        conn.commit()
        conn.close()

    def get_db_connection(self):
        """Get a connection to the database."""
        try:
            return sqlite3.connect(self.db_file)
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise

    def add_position(self, linkdin_url: str, name: str, open_by: str, company: str, location: str, description: str):
        """Add a new position to the Position table."""
        sql = """
        INSERT INTO Position (linkdin_url, name, open_by, company, location, description)
        VALUES (?, ?, ?, ?, ?, ?);
        """
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (linkdin_url, name, open_by, company, location, description))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding position: {e}")
            raise
        finally:
            conn.close()

    def add_interviewer(self, user_name: str, password: str, name: str, company: str, phone: str, email: str,
                        type: str):
        """Add a new interviewer to the Interviewer table."""
        sql = """
        INSERT INTO Interviewer (user_name, password, name, company, phone, email, type)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (user_name, password, name, company, phone, email, type))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding interviewer: {e}")
            raise
        finally:
            conn.close()

    def add_interviewer_position(self, interviewer_user_name, position_linkdin_url):
        try:
            query = """
                   INSERT INTO InterviewerPositions (interviewer_user_name, position_linkdin_url)
                   VALUES (?, ?)
               """
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query, (interviewer_user_name, position_linkdin_url))
            conn.commit()
            print("Interviewer position added successfully.")
        except sqlite3.Error as err:
            print(f"Error: {err}")
            conn.close()

    def add_interviewer_type(self, type: str):
        """Add a new interviewer type to the InterviewerType table."""
        sql = """
        INSERT INTO Interviewer (type)
        VALUES (?);
        """
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (type,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding interviewer: {e}")
            raise
        finally:
            conn.close()

    def add_stage(self, reviewer: str, summery: str, score: int, type: str):
        """Add a new stage to the Stage table."""
        sql = """
        INSERT INTO Stage (reviewer, summery, score, type)
        VALUES (?, ?, ?, ?);
        """
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (reviewer, summery, score, type))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding stage: {e}")
            raise
        finally:
            conn.close()

    def add_candidate(self, name: str, email: str, phone: str, city: str, summery: str, bazz_words: str,
                      resume_url: str, linkdin_url: str, github_url: str):
        """Add a new candidate to the Candidate table."""
        sql = """
        INSERT INTO Candidate (name, email, phone, city, summery, bazz_words, resume_url, linkdin_url, github_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (name, email, phone, city, summery, bazz_words, resume_url, linkdin_url, github_url))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding candidate: {e}")
            raise
        finally:
            conn.close()

    def add_candidate_stage(self, candidate_phone: str, position_linkdin_url: str, stage_id: int):
        """Add a new candidate stage to the CandidateStages table."""
        sql = """
        INSERT INTO CandidateStages (candidate_phone, position_linkdin_url, stage_id)
        VALUES (?, ?, ?);
        """
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (candidate_phone, position_linkdin_url, stage_id))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding candidate stage: {e}")
            raise
        finally:
            conn.close()

    ########################################################################################################################

    def delete_position(self, linkdin_url: str):
        """Delete a position from the Position table."""
        sql = "DELETE FROM Position WHERE linkdin_url = ?;"
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (linkdin_url,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting position: {e}")
            raise
        finally:
            conn.close()

    def delete_interviewer(self, user_name: str):
        """Delete an interviewer from the Interviewer table."""
        sql = "DELETE FROM Interviewer WHERE user_name = ?;"
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (user_name,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting interviewer: {e}")
            raise
        finally:
            conn.close()

    def delete_interviewer_position(self, interviewer_user_name, position_linkdin_url):
        """Delete an interviewer from the Interviewer table."""
        sql = """DELETE FROM InterviewerPositions WHERE interviewer_user_name = ? AND position_linkdin_url = ?"""
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (interviewer_user_name, position_linkdin_url,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting interviewer: {e}")
            raise
        finally:
            conn.close()

    def delete_stage(self, stage_id: int):
        """Delete a stage from the Stage table."""
        sql = "DELETE FROM Stage WHERE id = ?;"
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (stage_id,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting stage: {e}")
            raise
        finally:
            conn.close()

    def delete_interviewer_type(self, type: str):
        """DELETE FROM interviewerType from the InterviewerType table."""
        sql = "DELETE FROM InterviewerType WHERE type = ?;"
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (type,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting interviewer type: {e}")
            raise
        finally:
            conn.close()

    def delete_candidate(self, phone: str):
        """Delete a candidate from the Candidate table."""
        sql = "DELETE FROM Candidate WHERE phone = ?;"
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (phone,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting candidate: {e}")
            raise
        finally:
            conn.close()

    def delete_candidate_stage(self, candidate_phone: str, position_linkdin_url: str, stage_id: int):
        """Delete a candidate stage from the CandidateStages table."""
        sql = "DELETE FROM CandidateStages WHERE candidate_phone = ? AND position_linkdin_url = ? AND stage_id = ?;"
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (candidate_phone, position_linkdin_url, stage_id))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting candidate stage: {e}")
            raise
        finally:
            conn.close()

    ########################################################################################################################

    def get_all_positions(self) -> List[Position]:
        """Get all positions from the Position table."""
        sql = "SELECT * FROM Position;"
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [Position(linkdin_url=row[0], name=row[1], open_by=row[2], company=row[3], location=row[4],
                             description=row[5]) for row in rows]
        except sqlite3.Error as e:
            print(f"Error retrieving positions: {e}")
            raise
        finally:
            conn.close()

    def get_all_interviewers(self) -> List[Interviewer]:
        """Get all interviewers from the Interviewer table."""
        sql = "SELECT * FROM Interviewer;"
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [Interviewer(user_name=row[0], password=row[1], name=row[2], company=row[3], phone=row[4],
                                email=row[5], type=row[6]) for row in rows]
        except sqlite3.Error as e:
            print(f"Error retrieving interviewers: {e}")
            raise
        finally:
            conn.close()

    def get_all_interviewer_type(self, type)-> List[InterviewerType]:
        """Get all interviewers from the Interviewer table."""
        sql = """SELECT * FROM InterviewerType;"""
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (type,))
            rows = cursor.fetchall()
            return [InterviewerType(type=row[0]) for row in rows]
        except sqlite3.Error as e:
            print(f"Error retrieving interviewers: {e}")
            raise
        finally:
            conn.close()

    def get_all_stages(self) -> List[Stage]:
        """Get all stages from the Stage table."""
        sql = "SELECT * FROM Stage;"
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [Stage(id=row[0], reviewer=row[1], summery=row[2], score=row[3], type=row[4]) for row in rows]
        except sqlite3.Error as e:
            print(f"Error retrieving stages: {e}")
            raise
        finally:
            conn.close()

    def get_all_candidates(self) -> List [Candidate]:
        """Get all candidates from the Candidate table."""
        sql = "SELECT * FROM Candidate;"
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [Candidate(name=row[0], email=row[1], phone=row[2], city=row[3], summery=row[4], bazz_words=row[5],
                              resume_url=row[6], linkdin_url=row[7], github_url=row[8]) for row in rows]
        except sqlite3.Error as e:
            print(f"Error retrieving candidates: {e}")
            raise
        finally:
            conn.close()

    def get_all_candidate_stages(self) -> List[Tuple[Stage, Candidate, Position]]:
        """Get all candidate stages from the CandidateStages table."""
        sql = "SELECT * FROM CandidateStages;"
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [(self.get_stage_by_id(row[2]), self.get_candidate_by_phone(row[0]),
                     self.get_position_by_linkedin_url(row[1])) for row in rows]
        except sqlite3.Error as e:
            print(f"Error retrieving candidate stages: {e}")
            raise
        finally:
            conn.close()

    def get_all_interviewer_positions(self) -> List[(Position, Interviewer)]:
        """Get all interviewer positions from the InterviewerPositions table."""
        sql = "SELECT * FROM InterviewerPositions;"
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [(self.get_position_by_linkedin_url(row[1]), self.get_interviewer_by_user_name(row[0])) for row in rows]
        except sqlite3.Error as e:
            print(f"Error retrieving interviewer positions: {e}")
            raise
        finally:
            conn.close()

    ########################################################################################################################

    def get_position_by_linkedin_url(self, linkedin_url: str) -> Position:
        """Get a position record from the Position table by linkedin_url."""
        sql = "SELECT * FROM Position WHERE linkedin_url = ?;"
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (linkedin_url,))
            row = cursor.fetchone()
            if row:
                column_names = [column[0] for column in cursor.description]
                data = dict(zip(column_names, row))
                return Position(**data)
            else:
                return None  # Return None if no record is found
        except sqlite3.Error as e:
            print(f"Error retrieving position: {e}")
            raise
        finally:
            conn.close()

    def get_interviewer_by_user_name(self, user_name: str) -> Interviewer:
        """Get an interviewer record from the Interviewer table by user_name."""
        sql = "SELECT * FROM Interviewer WHERE user_name = ?;"
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (user_name,))
            row = cursor.fetchone()
            if row:
                column_names = [column[0] for column in cursor.description]
                data = dict(zip(column_names, row))
                return Interviewer(**data)
            else:
                return None  # Return None if no record is found
        except sqlite3.Error as e:
            print(f"Error retrieving interviewer: {e}")
            raise
        finally:
            conn.close()

    def get_interviewer_positions(self, user_name: str) -> List[Position]:
        """Get all positions for an interviewer from the InterviewerPositions table."""
        sql = "SELECT * FROM InterviewerPositions WHERE interviewer_user_name = ?;"
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (user_name,))
            rows = cursor.fetchall()
            positions = []
            for row in rows:
                position = self.get_position_by_linkedin_url(row[1])
                positions.append(position)
            return positions
        except sqlite3.Error as e:
            print(f"Error retrieving interviewer positions: {e}")
            raise
        finally:
            conn.close()

    def get_candidate_by_phone(self, phone: str) -> Candidate:
        """Get a candidate record from the Candidate table by phone."""
        sql = "SELECT * FROM Candidate WHERE phone = ?;"
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (phone,))
            row = cursor.fetchone()
            if row:
                column_names = [column[0] for column in cursor.description]
                data = dict(zip(column_names, row))
                return Candidate(**data)
            else:
                return None  # Return None if no record is found
        except sqlite3.Error as e:
            print(f"Error retrieving candidate: {e}")
            raise
        finally:
            conn.close()

    def get_candidate_by_position(self, linkedin_url: str) -> List[Candidate]:
        """Get all stages for a candidate from the CandidateStages table."""
        sql = "SELECT * FROM CandidateStages WHERE position_linkedin_url = ?;"
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (linkedin_url))
            rows = cursor.fetchall()
            stages = []
            for row in rows:
                stage = self.get_stage_by_id(row[2])
                stages.append(stage)
            return stages
        except sqlite3.Error as e:
            print(f"Error retrieving candidate stages: {e}")
            raise
        finally:
            conn.close()
    def get_candidate_stages(self, phone: str, linkedin_url: str) -> List[Stage]:
        """Get all stages for a candidate from the CandidateStages table."""
        sql = "SELECT * FROM CandidateStages WHERE candidate_phone = ? AND position_linkedin_url = ?;"
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (phone, linkedin_url))
            rows = cursor.fetchall()
            stages = []
            for row in rows:
                stage = self.get_stage_by_id(row[2])
                stages.append(stage)
            return stages
        except sqlite3.Error as e:
            print(f"Error retrieving candidate stages: {e}")
            raise
        finally:
            conn.close()

    def get_stage_by_id(self, stage_id: int) -> Stage:
        """Get a stage record from the Stage table by id."""
        sql = "SELECT * FROM Stage WHERE id = ?;"
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (stage_id,))
            row = cursor.fetchone()
            if row:
                column_names = [column[0] for column in cursor.description]
                data = dict(zip(column_names, row))
                return Stage(**data)
            else:
                return None  # Return None if no record is found
        except sqlite3.Error as e:
            print(f"Error retrieving stage: {e}")
            raise
        finally:
            conn.close()

    def get_interviewer_type(self, type: str) -> InterviewerType:
        """Get an interviewer type record from the InterviewerType table by type."""
        sql = "SELECT * FROM InterviewerType WHERE type = ?;"
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (type,))
            row = cursor.fetchone()
            if row:
                column_names = [column[0] for column in cursor.description]
                data = dict(zip(column_names, row))
                return InterviewerType(**data)
            else:
                return None  # Return None if no record is found
        except sqlite3.Error as e:
            print(f"Error retrieving interviewer type: {e}")
            raise
        finally:
            conn.close()
