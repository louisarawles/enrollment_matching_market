import json
import sqlite3

from src.save_json import load_json


def create_db(conn):
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS courseforum (
    Course_ID	TEXT NOT NULL PRIMARY KEY,
    Course_Name	TEXT,
    Department	TEXT,
    Quota	    INTEGER,
    Avg_GPA	    REAL,
    Reading	    REAL,
    Writing	    REAL,
    Group_Work	REAL,
    Hours_Needed REAL)
    ''')

    conn.commit()

def insert_courses(conn, courses):
    cursor = conn.cursor()
    for c in courses:
        cursor.execute("""
        INSERT INTO courseforum (
        Course_ID, Course_Name, Department, Quota, Avg_GPA, Reading,
        Writing, Group_Work, Hours_Needed
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            c.get('course_code'),
            c.get('course_title'),
            c.get("department"),
            c.get("class_size"),
            c.get("avg_gpa"),
            c.get("reading"),
            c.get("writing"),
            c.get("group_work"),
            c.get("avg_hours_per_week")
        ))

    conn.commit()


if __name__ == '__main__':
    conn = sqlite3.connect('courseforum.db')
    create_db(conn)

    with open("./parser/data/raw/processed_courses.json") as f:
        courses = json.load(f)
        insert_courses(conn, courses)

    conn.close()