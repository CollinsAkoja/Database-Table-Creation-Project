"""
CRUD Operations Module
Implements Create, Read, Update, Delete operations for database management
"""

import sqlite3
from typing import List, Dict, Optional, Any
from database import Database


class CRUDOperations:
    """
    A class to perform CRUD operations on the database
    
    CRUD stands for:
    - Create: Insert new records
    - Read: Query and retrieve records
    - Update: Modify existing records
    - Delete: Remove records
    """
    
    def __init__(self, db: Database):
        """
        Initialize CRUD operations with a database instance
        
        Args:
            db (Database): Database instance for operations
        """
        self.db = db
    
    # CREATE Operations 
    
    def create_student(self, name: str, email: str, age: int, gpa: float, enrollment_date: str) -> bool:
        """
        INSERT: Add a new student to the database
        
        Args:
            name (str): Student's full name
            email (str): Student's email address
            age (int): Student's age
            gpa (float): Student's GPA
            enrollment_date (str): Enrollment date (format: YYYY-MM-DD)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            insert_query = """
            INSERT INTO students (name, email, age, gpa, enrollment_date)
            VALUES (?, ?, ?, ?, ?)
            """
            self.db.cursor.execute(insert_query, (name, email, age, gpa, enrollment_date))
            self.db.commit()
            print(f"✓ Student '{name}' created successfully (ID: {self.db.cursor.lastrowid})")
            return True
        except sqlite3.IntegrityError as e:
            print(f"✗ Error: {e} (Possibly duplicate email)")
            return False
        except sqlite3.Error as e:
            print(f"✗ Error creating student: {e}")
            return False
    
    def create_course(self, course_name: str, course_code: str, credits: int, instructor: str) -> bool:
        """
        INSERT: Add a new course to the database
        
        Args:
            course_name (str): Name of the course
            course_code (str): Course code (e.g., "CS101")
            credits (int): Number of credit hours
            instructor (str): Instructor's name
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            insert_query = """
            INSERT INTO courses (course_name, course_code, credits, instructor)
            VALUES (?, ?, ?, ?)
            """
            self.db.cursor.execute(insert_query, (course_name, course_code, credits, instructor))
            self.db.commit()
            print(f"✓ Course '{course_name}' ({course_code}) created successfully (ID: {self.db.cursor.lastrowid})")
            return True
        except sqlite3.IntegrityError:
            print(f"✗ Error: Course code '{course_code}' already exists")
            return False
        except sqlite3.Error as e:
            print(f"✗ Error creating course: {e}")
            return False
    
    def create_enrollment(self, student_id: int, course_id: int, enrollment_date: str, grade: str = "N/A") -> bool:
        """
        INSERT: Enroll a student in a course
        
        Args:
            student_id (int): ID of the student
            course_id (int): ID of the course
            enrollment_date (str): Enrollment date
            grade (str): Initial grade (default: "N/A")
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            insert_query = """
            INSERT INTO enrollments (student_id, course_id, enrollment_date, grade)
            VALUES (?, ?, ?, ?)
            """
            self.db.cursor.execute(insert_query, (student_id, course_id, enrollment_date, grade))
            self.db.commit()
            print(f"✓ Enrollment created (Student ID: {student_id}, Course ID: {course_id})")
            return True
        except sqlite3.Error as e:
            print(f"✗ Error creating enrollment: {e}")
            return False
    
    #  READ Operations 
    
    def read_all_students(self) -> List[Dict[str, Any]]:
        """
        SELECT: Retrieve all students from the database
        
        Returns:
            List[Dict]: List of student records
        """
        try:
            query = "SELECT id, name, email, age, gpa, enrollment_date FROM students"
            self.db.cursor.execute(query)
            students = self.db.cursor.fetchall()
            return [
                {
                    "id": s[0],
                    "name": s[1],
                    "email": s[2],
                    "age": s[3],
                    "gpa": s[4],
                    "enrollment_date": s[5]
                }
                for s in students
            ]
        except sqlite3.Error as e:
            print(f"✗ Error reading students: {e}")
            return []
    
    def read_student_by_id(self, student_id: int) -> Optional[Dict[str, Any]]:
        """
        SELECT: Retrieve a specific student by ID
        
        Args:
            student_id (int): ID of the student
            
        Returns:
            Dict: Student record or None if not found
        """
        try:
            query = "SELECT id, name, email, age, gpa, enrollment_date FROM students WHERE id = ?"
            self.db.cursor.execute(query, (student_id,))
            student = self.db.cursor.fetchone()
            
            if student:
                return {
                    "id": student[0],
                    "name": student[1],
                    "email": student[2],
                    "age": student[3],
                    "gpa": student[4],
                    "enrollment_date": student[5]
                }
            return None
        except sqlite3.Error as e:
            print(f"✗ Error reading student: {e}")
            return None
    
    def read_student_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        SELECT: Retrieve a student by email address
        
        Args:
            email (str): Student's email address
            
        Returns:
            Dict: Student record or None if not found
        """
        try:
            query = "SELECT id, name, email, age, gpa, enrollment_date FROM students WHERE email = ?"
            self.db.cursor.execute(query, (email,))
            student = self.db.cursor.fetchone()
            
            if student:
                return {
                    "id": student[0],
                    "name": student[1],
                    "email": student[2],
                    "age": student[3],
                    "gpa": student[4],
                    "enrollment_date": student[5]
                }
            return None
        except sqlite3.Error as e:
            print(f"✗ Error reading student by email: {e}")
            return None
    
    def read_all_courses(self) -> List[Dict[str, Any]]:
        """
        SELECT: Retrieve all courses from the database
        
        Returns:
            List[Dict]: List of course records
        """
        try:
            query = "SELECT id, course_name, course_code, credits, instructor FROM courses"
            self.db.cursor.execute(query)
            courses = self.db.cursor.fetchall()
            return [
                {
                    "id": c[0],
                    "name": c[1],
                    "code": c[2],
                    "credits": c[3],
                    "instructor": c[4]
                }
                for c in courses
            ]
        except sqlite3.Error as e:
            print(f"✗ Error reading courses: {e}")
            return []
    
    def read_student_enrollments(self, student_id: int) -> List[Dict[str, Any]]:
        """
        SELECT with JOIN: Retrieve all courses a student is enrolled in
        
        Args:
            student_id (int): ID of the student
            
        Returns:
            List[Dict]: List of enrollment records with course details
        """
        try:
            query = """
            SELECT e.id, c.course_name, c.course_code, e.grade, e.enrollment_date
            FROM enrollments e
            JOIN courses c ON e.course_id = c.id
            WHERE e.student_id = ?
            """
            self.db.cursor.execute(query, (student_id,))
            enrollments = self.db.cursor.fetchall()
            return [
                {
                    "enrollment_id": e[0],
                    "course_name": e[1],
                    "course_code": e[2],
                    "grade": e[3],
                    "enrollment_date": e[4]
                }
                for e in enrollments
            ]
        except sqlite3.Error as e:
            print(f"✗ Error reading enrollments: {e}")
            return []
    
    def read_top_students(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        SELECT with ORDER BY: Retrieve top students by GPA
        
        Args:
            limit (int): Number of top students to retrieve
            
        Returns:
            List[Dict]: List of top student records
        """
        try:
            query = """
            SELECT id, name, email, gpa FROM students
            ORDER BY gpa DESC
            LIMIT ?
            """
            self.db.cursor.execute(query, (limit,))
            students = self.db.cursor.fetchall()
            return [
                {
                    "id": s[0],
                    "name": s[1],
                    "email": s[2],
                    "gpa": s[3]
                }
                for s in students
            ]
        except sqlite3.Error as e:
            print(f"✗ Error reading top students: {e}")
            return []
    
    def read_students_by_age_range(self, min_age: int, max_age: int) -> List[Dict[str, Any]]:
        """
        SELECT with WHERE and comparison: Retrieve students within age range
        
        Args:
            min_age (int): Minimum age
            max_age (int): Maximum age
            
        Returns:
            List[Dict]: List of student records within age range
        """
        try:
            query = """
            SELECT id, name, email, age, gpa FROM students
            WHERE age BETWEEN ? AND ?
            ORDER BY age
            """
            self.db.cursor.execute(query, (min_age, max_age))
            students = self.db.cursor.fetchall()
            return [
                {
                    "id": s[0],
                    "name": s[1],
                    "email": s[2],
                    "age": s[3],
                    "gpa": s[4]
                }
                for s in students
            ]
        except sqlite3.Error as e:
            print(f"✗ Error reading students by age: {e}")
            return []
    
    # UPDATE Operations
    
    def update_student_gpa(self, student_id: int, new_gpa: float) -> bool:
        """
        UPDATE: Modify a student's GPA
        
        Args:
            student_id (int): ID of the student
            new_gpa (float): New GPA value
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            update_query = "UPDATE students SET gpa = ? WHERE id = ?"
            self.db.cursor.execute(update_query, (new_gpa, student_id))
            self.db.commit()
            
            if self.db.cursor.rowcount > 0:
                print(f"✓ Student (ID: {student_id}) GPA updated to {new_gpa}")
                return True
            else:
                print(f"✗ Student with ID {student_id} not found")
                return False
        except sqlite3.Error as e:
            print(f"✗ Error updating student GPA: {e}")
            return False
    
    def update_student_email(self, student_id: int, new_email: str) -> bool:
        """
        UPDATE: Change a student's email address
        
        Args:
            student_id (int): ID of the student
            new_email (str): New email address
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            update_query = "UPDATE students SET email = ? WHERE id = ?"
            self.db.cursor.execute(update_query, (new_email, student_id))
            self.db.commit()
            
            if self.db.cursor.rowcount > 0:
                print(f"✓ Student (ID: {student_id}) email updated to {new_email}")
                return True
            else:
                print(f"✗ Student with ID {student_id} not found")
                return False
        except sqlite3.IntegrityError:
            print(f"✗ Error: Email '{new_email}' already exists")
            return False
        except sqlite3.Error as e:
            print(f"✗ Error updating student email: {e}")
            return False
    
    def update_course_instructor(self, course_id: int, new_instructor: str) -> bool:
        """
        UPDATE: Change a course's instructor
        
        Args:
            course_id (int): ID of the course
            new_instructor (str): New instructor name
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            update_query = "UPDATE courses SET instructor = ? WHERE id = ?"
            self.db.cursor.execute(update_query, (new_instructor, course_id))
            self.db.commit()
            
            if self.db.cursor.rowcount > 0:
                print(f"✓ Course (ID: {course_id}) instructor updated to '{new_instructor}'")
                return True
            else:
                print(f"✗ Course with ID {course_id} not found")
                return False
        except sqlite3.Error as e:
            print(f"✗ Error updating course instructor: {e}")
            return False
    
    def update_enrollment_grade(self, enrollment_id: int, grade: str) -> bool:
        """
        UPDATE: Update a student's grade in a course
        
        Args:
            enrollment_id (int): ID of the enrollment record
            grade (str): New grade (e.g., "A", "B", "C")
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            update_query = "UPDATE enrollments SET grade = ? WHERE id = ?"
            self.db.cursor.execute(update_query, (grade, enrollment_id))
            self.db.commit()
            
            if self.db.cursor.rowcount > 0:
                print(f"✓ Enrollment (ID: {enrollment_id}) grade updated to '{grade}'")
                return True
            else:
                print(f"✗ Enrollment with ID {enrollment_id} not found")
                return False
        except sqlite3.Error as e:
            print(f"✗ Error updating enrollment grade: {e}")
            return False
    
    #  DELETE Operations 
    
    def delete_student(self, student_id: int) -> bool:
        """
        DELETE: Remove a student from the database
        
        Args:
            student_id (int): ID of the student to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            delete_query = "DELETE FROM students WHERE id = ?"
            self.db.cursor.execute(delete_query, (student_id,))
            self.db.commit()
            
            if self.db.cursor.rowcount > 0:
                print(f"✓ Student (ID: {student_id}) deleted successfully")
                return True
            else:
                print(f"✗ Student with ID {student_id} not found")
                return False
        except sqlite3.Error as e:
            print(f"✗ Error deleting student: {e}")
            return False
    
    def delete_course(self, course_id: int) -> bool:
        """
        DELETE: Remove a course from the database
        
        Args:
            course_id (int): ID of the course to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            delete_query = "DELETE FROM courses WHERE id = ?"
            self.db.cursor.execute(delete_query, (course_id,))
            self.db.commit()
            
            if self.db.cursor.rowcount > 0:
                print(f"✓ Course (ID: {course_id}) deleted successfully")
                return True
            else:
                print(f"✗ Course with ID {course_id} not found")
                return False
        except sqlite3.Error as e:
            print(f"✗ Error deleting course: {e}")
            return False
    
    def delete_all_students(self) -> bool:
        """
        DELETE: Remove all students from the database
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            delete_query = "DELETE FROM students"
            self.db.cursor.execute(delete_query)
            self.db.commit()
            print(f"✓ All students deleted ({self.db.cursor.rowcount} records removed)")
            return True
        except sqlite3.Error as e:
            print(f"✗ Error deleting all students: {e}")
            return False
    
    def print_all_students(self) -> None:
        """Display all students in a formatted table"""
        students = self.read_all_students()
        if not students:
            print("No students found.")
            return
        
        print("\n" + "="*120)
        print(f"{'ID':<5} {'Name':<20} {'Email':<30} {'Age':<5} {'GPA':<6} {'Enrollment Date':<15}")
        print("="*120)
        for student in students:
            print(f"{student['id']:<5} {student['name']:<20} {student['email']:<30} {student['age']:<5} {student['gpa']:<6.2f} {student['enrollment_date']:<15}")
        print("="*120 + "\n")
    
    def print_all_courses(self) -> None:
        """Display all courses in a formatted table"""
        courses = self.read_all_courses()
        if not courses:
            print("No courses found.")
            return
        
        print("\n" + "="*100)
        print(f"{'ID':<5} {'Course Name':<30} {'Code':<10} {'Credits':<10} {'Instructor':<30}")
        print("="*100)
        for course in courses:
            print(f"{course['id']:<5} {course['name']:<30} {course['code']:<10} {course['credits']:<10} {course['instructor']:<30}")
        print("="*100 + "\n")
