# setup_database.py

import sqlite3
import os

DB_PATH = "data/company.db"

os.makedirs("data", exist_ok=True)

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS STUDENT")
cursor.execute("DROP TABLE IF EXISTS COURSE")



# Table 1: STUDENT
table_info_student = """
Create table STUDENT(
    STUDENT_ID INT PRIMARY KEY,
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT
);
"""
cursor.execute(table_info_student)

# Insert data into STUDENT
cursor.execute('''Insert Into STUDENT values(1, 'Krish','Data Science','A',90) ''')
cursor.execute('''Insert Into STUDENT values(2, 'Sudhanshu','Data Science','B',100) ''')
cursor.execute('''Insert Into STUDENT values(3, 'Darius','Data Science','A',86) ''')
cursor.execute('''Insert Into STUDENT values(4, 'Vikash','DEVOPS','A',50) ''')
cursor.execute('''Insert Into STUDENT values(5, 'Dipes','DEVOPS','A',35) ''')

# Table 2: COURSE
table_info_course = """
Create table COURSE(
    COURSE_ID VARCHAR(25) PRIMARY KEY,
    COURSE_NAME VARCHAR(25),
    INSTRUCTOR VARCHAR(25)
);
"""
cursor.execute(table_info_course)

# Insert data into COURSE
cursor.execute('''Insert Into COURSE values('DS101', 'Data Science', 'Dr. Smith')''')
cursor.execute('''Insert Into COURSE values('DV101', 'DEVOPS', 'Mr. Jones')''')
cursor.execute('''Insert Into COURSE values('WD101', 'Web Dev', 'Ms. Ada')''')


print(f"Database '{DB_PATH}' created successfully with STUDENT and COURSE tables.")

print("\nSTUDENT Table:")
data = cursor.execute('''Select * From STUDENT''')
for row in data:
    print(row)

print("\nCOURSE Table:")
data = cursor.execute('''Select * From COURSE''')
for row in data:
    print(row)

# Close conneeeee
connection.commit()
connection.close()