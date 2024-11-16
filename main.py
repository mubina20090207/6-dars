import sqlite3

conn = sqlite3.connect(':memory:')  
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER CHECK(age > 0),
    email TEXT UNIQUE NOT NULL
)
''')

cursor.execute('''
CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code TEXT UNIQUE NOT NULL,
    course_name TEXT NOT NULL,
    credits INTEGER CHECK(credits BETWEEN 1 AND 5)
)
''')

cursor.execute('''
CREATE TABLE enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    course_id INTEGER,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE SET NULL
)
''')

cursor.execute('''
CREATE TABLE teachers (
    teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    experience_years INTEGER CHECK(experience_years >= 0)
)
''')

cursor.execute('''
CREATE TABLE course_assignments (
    assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER DEFAULT NULL,
    course_id INTEGER,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE SET DEFAULT,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
)
''')

conn.commit()

students_data = [
    ("Ali", 20, "ali@gmail.com"),
    ("Vali", 22, "vali@gmail.com"),
    ("Hasan", 21, "hasan@gmail.com"),
    ("Husan", 23, "husan@gmail.com"),
    ("Sara", 19, "sara@gmail.com"),
    ("Nodira", 24, "nodira@gmail.com"),
    ("Aziz", 18, "aziz@gmail.com")
]
cursor.executemany('''
INSERT INTO students (name, age, email) VALUES (?, ?, ?)
''', students_data)

courses_data = [
    ("CS101", "Computer Science", 3),
    ("MATH202", "Mathematics", 4),
    ("ENG303", "English Literature", 2)
]
cursor.executemany('''
INSERT INTO courses (course_code, course_name, credits) VALUES (?, ?, ?)
''', courses_data)

teachers_data = [
    ("Akmal", 5),
    ("Begzod", 3)
]
cursor.executemany('''
INSERT INTO teachers (name, experience_years) VALUES (?, ?)
''', teachers_data)

course_assignments_data = [
    (1, 1), 
    (2, 2)   
]
cursor.executemany('''
INSERT INTO course_assignments (teacher_id, course_id) VALUES (?, ?)
''', course_assignments_data)

conn.commit()

cursor.execute("ALTER TABLE students RENAME TO learners")

cursor.execute("ALTER TABLE learners RENAME COLUMN name TO full_name")

conn.commit()

cursor.execute("UPDATE learners SET age = 25 WHERE student_id = 1")
cursor.execute("UPDATE learners SET age = 26 WHERE student_id = 2")

conn.commit()

cursor.execute("DELETE FROM learners WHERE student_id = 3")
cursor.execute("DELETE FROM learners WHERE student_id = 4")

conn.commit()

cursor.execute("SELECT * FROM learners")
students = cursor.fetchall()

print("Updated Students Data:")
for student in students:
    print(student)

cursor.execute("SELECT * FROM courses")
courses = cursor.fetchall()

print("\nCourses Data:")
for course in courses:
    print(course)

cursor.execute('''
SELECT t.name, c.course_name
FROM teachers t
JOIN course_assignments ca ON t.teacher_id = ca.teacher_id
JOIN courses c ON ca.course_id = c.course_id
''')
assignments = cursor.fetchall()

print("\nCourse Assignments:")
for assignment in assignments:
    print(assignment)
