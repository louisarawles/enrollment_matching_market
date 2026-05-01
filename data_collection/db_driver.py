import json
import sqlite3

HARDCODED = {
    "CS 1110": {
        "reading": 0.5,
        "writing": 0.8,
        "group_work": 0.8,
    },
    "CS 1112": {
        "reading": 0.1,
        "writing": 0.5,
        "group_work": 0.3,
    },
    "CS 2100": {
        "reading": 0.6,
        "writing":1.4,
        "group_work":0.2,
    },
    "CS 2120": {
        "reading":1.3,
        "writing":3.3,
        "group_work":0.0,
    },
    "CS 2130": {
        "reading":2.2,
        "writing":1.8,
        "group_work":0.8,
    },
    "CS 2910": {
        "reading": 0.0,
        "writing":0.0,
        "group_work":0.0,
    },
    "CS 3100": {
        "reading":1.5,
        "writing":2.4,
        "group_work":0.7,
    },
    "CS 3120": {
        "reading":1.6,
        "writing":1.1,
        "group_work":3.3,
    },
    "CS 3130": {
        "reading":2.2,
        "writing":4.5,
        "group_work":0.5,
    },
    "CS 3140": {
        "reading":0.0,
        "writing":0.0,
        "group_work":6.0,
    },
    "CS 3205": {
        "reading":2.0,
        "writing":1.5,
        "group_work":6.1,
    },
    "CS 3240": {
        "reading":0.3,
        "writing":0.6,
        "group_work":3.6,
    },
    "CS 3250": {
        "reading":0.3,
        "writing":0.3,
        "group_work":0.5,
    },
    "CS 3710": {
        "reading":0.2,
        "writing":0.8,
        "group_work":0.0,
    },
    "CS 4444": {
        "reading":1.0,
        "writing":0.0,
        "group_work":0.0
    },
    "CS 4457": {
        "reading":1.0,
        "writing":0.0,
        "group_work":0.0
    },
    "CS 4501": { # note that this value is used for simulation purposes but given this course has multiple topics and professors, these values vary significantly b/w sections
        "reading":3.3,
        "writing":5.7,
        "group_work":3.3,
    },
    "CS 4620": {
        "reading":2.0,
        "writing":1.0,
        "group_work":4.0,
    },
    "CS 4630": {
        "reading":0.0,
        "writing":8.0,
        "group_work":0.0,
    },
    "CS 4710": {
        "reading":1.0,
        "writing":0.0,
        "group_work":2.0,
    },
}


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
        code = c.get('course_code')
        extras = HARDCODED.get(code, {})
        cursor.execute("""
        INSERT INTO courseforum (
        Course_ID, Course_Name, Department, Quota, Avg_GPA, Reading,
        Writing, Group_Work, Hours_Needed
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            code,
            c.get('course_title'),
            c.get("department"),
            c.get("class_size"),
            c.get("avg_gpa"),
            extras.get("reading"),
            extras.get("writing"),
            extras.get("group_work"),
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