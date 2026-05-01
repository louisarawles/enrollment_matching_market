"""
This code maps from the data gathered about courses and students to preference ordering based on established rules:

Course Features
- Prefer student in same department
- Prefer older students 
- Prefer higher GPA
- Prefer student willing to put more time in 
- Prefer student with less difference between course r/w/groupwork score

Student Features
- Prefer minimal difference between their GPA and course GPA
- Prefer courses in their major 
- Match course size preference
- Match reading, writing, groupwork preferences
- Match amount of time willing to put in, or less

Output dfs with preferences, and a quota dataframe
"""

import pandas as pd
import numpy as np

#FILE NAMES (update whenever we change the file)

STUDENT_DATA = "student_raw_data_updated.csv"
COURSE_DATA = "courses_simulated.csv"


# map quota to size preference (i.e. raw quota to size preference 0-5)
def quota_to_size(quota: int) -> int:
    return min(5, round(quota / 8))

def score_student_preferences(students: pd.DataFrame, courses: pd.DataFrame) -> pd.DataFrame:
    """
    Build score matrix for students
    """
    scores = pd.DataFrame(index=students['Computing ID'], columns=courses['Course ID'], dtype=float)
 
    
    course_sizes = courses.set_index('Course ID')['Quota'].apply(quota_to_size)
 
    for _, student in students.iterrows():
        sid = student['Computing ID']
        for _, course in courses.iterrows():
            cid = course['Course ID']
            s = 0.0
 
            # GPA match — penalize difference (scaled so a 1-point gap costs 2 points)
            s -= abs(student['GPA'] - course['Avg GPA']) * 2
 
            # Major / department match bonus
            if student['Major'] == course['Department']:
                s += 3
 
            # Size preference match
            s -= abs(student['Size Preference'] - course_sizes[cid])
 
            # Learning style match
            s -= abs(student['Reading']    - course['Reading'])
            s -= abs(student['Writing']    - course['Writing'])
            s -= abs(student['Group Work'] - course['Group Work'])
 
            # Time commitment — double-penalize if course demands more than student offers
            time_diff = course['Hours Needed'] - student['Time Commitment']
            if time_diff > 0:
                s -= time_diff * 2
 
            scores.loc[sid, cid] = s
 
    return scores


def score_course_preferences(students: pd.DataFrame, courses: pd.DataFrame) -> pd.DataFrame:
    """
    Build score matrix for courses
    """
    scores = pd.DataFrame(index=students['Computing ID'], columns=courses['Course ID'], dtype=float)
 
    for _, course in courses.iterrows():
        cid = course['Course ID']
        for _, student in students.iterrows():
            sid = student['Computing ID']
            s = 0.0
 
            # Department match bonus
            if student['Major'] == course['Department']:
                s += 3
 
            # Prefer older students
            s += student['Class Year']
 
            # Prefer higher GPA
            s += student['GPA']
 
            # Prefer students willing to commit more time
            s += student['Time Commitment'] * 0.5
 
            # Prefer students whose learning style fits the course
            s -= abs(student['Reading']    - course['Reading'])    * 0.5
            s -= abs(student['Writing']    - course['Writing'])    * 0.5
            s -= abs(student['Group Work'] - course['Group Work']) * 0.5
 
            scores.loc[sid, cid] = s
 
    return scores

# convert scores to preference ordering
def scores_to_ranks(score_matrix: pd.DataFrame, ascending: bool = False) -> pd.DataFrame:
    return score_matrix.rank(axis=1, ascending=ascending, method='first').astype(int) - 1

# turn the preferences into a neatly organized df to feed into the matching mechanism
def build_preference_dfs(student_data_file: str, course_data_file: str):
    students = pd.read_csv(student_data_file)
    courses  = pd.read_csv(course_data_file)
 
    print(f"Loaded {len(students)} students and {len(courses)} courses.")
    print("Computing student preference scores...")
    student_scores = score_student_preferences(students, courses)
 
    print("Computing course preference scores...")
    course_scores  = score_course_preferences(students, courses)
 
    # Rank: rank 0 = most preferred (highest score → lowest rank)
    students_df = scores_to_ranks(student_scores, ascending=False)
    courses_df  = scores_to_ranks(course_scores,  ascending=False)
 
    courses_quota = dict(zip(courses['Course ID'], courses['Quota']))
 
    return students_df, courses_df, courses_quota
 
 
if __name__ == '__main__':
    students_df, courses_df, courses_quota = build_preference_dfs(STUDENT_DATA, COURSE_DATA)
    print("\nstudents_df shape:", students_df.shape)
    print(students_df.iloc[:3, :5])
    print("\ncourses_df shape:", courses_df.shape)
    print(courses_df.iloc[:3, :5])



