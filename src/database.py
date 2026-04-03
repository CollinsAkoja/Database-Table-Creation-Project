"""
Database Initialization Module
Handles database connection and table creation with SQLite
"""

import sqlite3
import os
from typing import Optional


class Database:
    """
    A class to manage SQLite database connections and table creation
    
    Attributes:
        db_path (str): Path to the SQLite database file
        connection (sqlite3.Connection): Active database connection
        cursor (sqlite3.Cursor): Database cursor for executing commands
    """
    
    def __init__(self, db_path: str = "database.db"):
        """
        Initialize database connection
        
        Args:
            db_path (str): Path to store the SQLite database file
        """
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None
    
    def connect(self) -> None:
        """
        Establish connection to the SQLite database
        Creates the database file if it doesn't exist
        """
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            print(f"✓ Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            print(f"✗ Error connecting to database: {e}")
            raise
    
    def disconnect(self) -> None:
        """Close the database connection"""
        if self.connection:
            self.connection.close()
            print("✓ Disconnected from database")
    
    def commit(self) -> None:
        """Commit changes to the database"""
        if self.connection:
            self.connection.commit()
    
    def create_students_table(self) -> None:
        """
        Create a 'students' table with proper schema
        
        Table Schema:
        - id: INTEGER PRIMARY KEY (auto-incrementing unique identifier)
        - name: TEXT NOT NULL (student name, required)
        - email: TEXT UNIQUE (student email, must be unique)
        - age: INTEGER (student age)
        - gpa: REAL (grade point average)
        - enrollment_date: TEXT (date of enrollment)
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            age INTEGER,
            gpa REAL,
            enrollment_date TEXT
        )
        """
        try:
            self.cursor.execute(create_table_sql)
            self.connection.commit()
            print("✓ 'students' table created successfully")
        except sqlite3.Error as e:
            print(f"✗ Error creating 'students' table: {e}")
    
    def create_courses_table(self) -> None:
        """
        Create a 'courses' table with proper schema
        
        Table Schema:
        - id: INTEGER PRIMARY KEY (unique course identifier)
        - course_name: TEXT NOT NULL (name of the course)
        - course_code: TEXT UNIQUE NOT NULL (course code, e.g., "CS101")
        - credits: INTEGER (number of credit hours)
        - instructor: TEXT (name of the instructor)
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL,
            course_code TEXT UNIQUE NOT NULL,
            credits INTEGER,
            instructor TEXT
        )
        """
        try:
            self.cursor.execute(create_table_sql)
            self.connection.commit()
            print("✓ 'courses' table created successfully")
        except sqlite3.Error as e:
            print(f"✗ Error creating 'courses' table: {e}")
    
    def create_enrollments_table(self) -> None:
        """
        Create an 'enrollments' table to link students and courses
        
        Table Schema:
        - id: INTEGER PRIMARY KEY
        - student_id: INTEGER FOREIGN KEY (references students table)
        - course_id: INTEGER FOREIGN KEY (references courses table)
        - grade: TEXT (student's grade in the course)
        - enrollment_date: TEXT (when the student enrolled in the course)
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            grade TEXT,
            enrollment_date TEXT,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
        """
        try:
            self.cursor.execute(create_table_sql)
            self.connection.commit()
            print("✓ 'enrollments' table created successfully")
        except sqlite3.Error as e:
            print(f"✗ Error creating 'enrollments' table: {e}")
    
    def drop_table(self, table_name: str) -> None:
        """
        Drop a table from the database
        
        Args:
            table_name (str): Name of the table to drop
        """
        try:
            self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            self.connection.commit()
            print(f"✓ Table '{table_name}' dropped")
        except sqlite3.Error as e:
            print(f"✗ Error dropping table '{table_name}': {e}")
    
    def get_table_info(self, table_name: str) -> None:
        """
        Display schema information for a table
        
        Args:
            table_name (str): Name of the table
        """
        try:
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            columns = self.cursor.fetchall()
            
            if not columns:
                print(f"✗ Table '{table_name}' does not exist")
                return
            
            print(f"\n📋 Schema for table '{table_name}':")
            print(f"{'Column':<20} {'Type':<15} {'Not Null':<10} {'Primary Key':<12}")
            print("-" * 60)
            
            for column in columns:
                col_name, col_type, not_null, pk = column[1:5] if len(column) >= 5 else column[1:4] + (None,)
                print(f"{col_name:<20} {col_type:<15} {'Yes' if not_null else 'No':<10} {'Yes' if pk else 'No':<12}")
        except sqlite3.Error as e:
            print(f"✗ Error retrieving table info: {e}")
    
    def get_all_tables(self) -> list:
        """
        Retrieve list of all tables in the database
        
        Returns:
            list: List of table names
        """
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = self.cursor.fetchall()
            return [table[0] for table in tables]
        except sqlite3.Error as e:
            print(f"✗ Error retrieving tables: {e}")
            return []
    
    def execute_query(self, query: str) -> list:
        """
        Execute a SELECT query and return results
        
        Args:
            query (str): SQL SELECT query
            
        Returns:
            list: Query results
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"✗ Error executing query: {e}")
            return []
    
    def close_database(self) -> None:
        """Close database and clean up resources"""
        if self.connection:
            self.connection.close()
