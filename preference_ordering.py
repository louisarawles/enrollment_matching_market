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
COURSE_DATA = "courseforum.csv"
NUM_STUDENTS = 2800


# map quota to size preference (i.e. raw quota to size preference 0-5)
def quota_to_size(quota: int) -> int:
    return min(5, round(quota / 8))

def score_student_preferences(students: pd.DataFrame, courses: pd.DataFrame) -> pd.DataFrame:
    """
    Build score matrix for students (vectorized).
    """
    c_size = np.array([quota_to_size(q) for q in courses['Quota'].values])[None, :]

    s_gpa  = students['GPA'].values[:, None]
    s_size = students['Size Preference'].values[:, None]
    s_read = students['Reading'].values[:, None]
    s_writ = students['Writing'].values[:, None]
    s_gw   = students['Group Work'].values[:, None]
    s_time = students['Time Commitment'].values[:, None]
    s_maj  = students['Major'].values[:, None]

    c_gpa  = courses['Avg GPA'].values[None, :]
    c_read = courses['Reading'].values[None, :]
    c_writ = courses['Writing'].values[None, :]
    c_gw   = courses['Group Work'].values[None, :]
    c_time = courses['Hours Needed'].values[None, :]
    c_dept = courses['Department'].values[None, :]

    scores  = np.zeros((len(students), len(courses)))
    scores -= np.abs(s_gpa - c_gpa) * 8
    scores += (s_maj == c_dept) * 10
    scores -= np.abs(s_size - c_size) * 1
    scores -= np.abs(s_read - c_read) * 1
    scores -= np.abs(s_writ - c_writ) * 1
    scores -= np.abs(s_gw - c_gw) * 1
    time_diff = c_time - s_time 
    scores -= np.where(time_diff > 0, time_diff * 0.5, 0)

    return pd.DataFrame(scores, index=students['Computing ID'], columns=courses['Course ID'])


def score_course_preferences(students: pd.DataFrame, courses: pd.DataFrame) -> pd.DataFrame:
    """
    Build score matrix for courses (vectorized).
    """
    s_maj  = students['Major'].values[:, None]
    s_year = students['Class Year'].values[:, None]
    s_gpa  = students['GPA'].values[:, None]
    s_time = students['Time Commitment'].values[:, None]
    s_read = students['Reading'].values[:, None]
    s_writ = students['Writing'].values[:, None]
    s_gw   = students['Group Work'].values[:, None]

    c_dept = courses['Department'].values[None, :]
    c_read = courses['Reading'].values[None, :]
    c_writ = courses['Writing'].values[None, :]
    c_gw   = courses['Group Work'].values[None, :]

    c_gpa  = courses['Avg GPA'].values[None, :]

    scores  = np.zeros((len(students), len(courses)))
    scores += (s_maj == c_dept) * 10
    scores += s_year * 4
    scores -= np.abs(s_gpa - c_gpa) * 3
    scores += s_time * 2
    scores -= np.abs(s_read - c_read) * 1.0
    scores -= np.abs(s_writ - c_writ) * 1.0
    scores -= np.abs(s_gw - c_gw) * 1.0

    return pd.DataFrame(scores, index=students['Computing ID'], columns=courses['Course ID'])


# convert scores to preference ordering
def scores_to_ranks(score_matrix: pd.DataFrame, ascending: bool = False, axis: int = 1) -> pd.DataFrame:
    return score_matrix.rank(axis=axis, ascending=ascending, method='first').astype(int) - 1


# turn the preferences into a neatly organized df to feed into the matching mechanism
def build_preference_dfs(student_data_file: str, course_data_file: str, num_students: int = None):
    students = pd.read_csv(student_data_file)
    courses  = pd.read_csv(course_data_file)

    if num_students is not None:
        students = students.head(num_students)

    print(f"Loaded {len(students)} students and {len(courses)} courses.")
    print("Computing student preference scores...")
    student_scores = score_student_preferences(students, courses)

    print("Computing course preference scores...")
    course_scores  = score_course_preferences(students, courses)

    # students_df: rank across courses for each student (axis=1) — lower = more preferred by student
    # courses_df:  rank across students for each course (axis=0) — lower = more preferred by course
    students_df = scores_to_ranks(student_scores, ascending=False, axis=1)
    courses_df  = scores_to_ranks(course_scores,  ascending=False, axis=0)

    courses_quota = dict(zip(courses['Course ID'], courses['Quota']))

    return students_df, courses_df, courses_quota


if __name__ == '__main__':
    students_df, courses_df, courses_quota = build_preference_dfs(STUDENT_DATA, COURSE_DATA, num_students=NUM_STUDENTS)
    print("\nstudents_df shape:", students_df.shape)
    print(students_df.iloc[:3, :5])
    print("\ncourses_df shape:", courses_df.shape)
    print(courses_df.iloc[:3, :5])
