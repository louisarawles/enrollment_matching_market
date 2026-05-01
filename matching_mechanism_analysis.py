# This file applies both RSD and DA to the preference ordering we derive and evaluates them based on stability, allocative efficiency, and student satisfaction

from deferred_acceptance import da
from random_serial_dictatorship import rsd
import pandas as pd
from preference_ordering import build_preference_dfs   

# Students are represented in a database with rows = students (based on computing id), columns = courses (based on course id) where student preference ranks (lower = more preferred)
# Courses are represented in a database with course's preferences (rows = courses, cols = students) course preference ranks over students (lower = more preferred)

STUDENT_DATA = "student_raw_data_updated.csv"
COURSE_DATA = "courses_simulated.csv"

students_df, courses_df, courses_quota = build_preference_dfs(student_data_file=STUDENT_DATA, course_data_file=COURSE_DATA) 

da_matching = da(students_df, courses_df, courses_quota)
rsd_matching = rsd(students_df, courses_quota)

def blocking_pairs(matching, students_df, courses_df, courses_quota):
    # Evaluate matching for blocking pairs, more relevant for RSD because DA is guaranteed to produce no blocking pairs
    enrolled = {}
    for student, course in matching.items():
        enrolled.setdefault(course, []).append(student)
 
    pairs = []
    for student in students_df.index:
        current_course = matching.get(student)
        current_rank = students_df.loc[student, current_course] if current_course else float('inf')
 
        for course in students_df.columns:
            if course == current_course:
                continue
            # Student must prefer this course over their current one
            if students_df.loc[student, course] >= current_rank:
                continue
            # Course has spare capacity — automatic blocking pair
            enrolled_in_course = enrolled.get(course, [])
            if len(enrolled_in_course) < courses_quota[course]:
                pairs.append((student, course))
            else:
                # Course is full — blocks if it prefers this student over its worst current enrolled student
                worst = max(enrolled_in_course, key=lambda s: courses_df.loc[s, course])
                if courses_df.loc[student, course] < courses_df.loc[worst, course]:
                    pairs.append((student, course))
    return pairs

def pareto_improving_swaps(matching, students_df):
    # check for swaps where students strictly prefer each other's assigned course
    students = list(matching.keys())
    swaps = []
    for i, s1 in enumerate(students):
        for s2 in students[i + 1:]:
            c1, c2 = matching[s1], matching[s2]
            if c1 == c2:
                continue
            if (students_df.loc[s1, c2] < students_df.loc[s1, c1] and
                    students_df.loc[s2, c1] < students_df.loc[s2, c2]):
                swaps.append((s1, s2))
    return swaps

def performance_summary(matching, students_df):
    # summarize performance relative to student preferences

    ranks = []
    top_choice = 0
    unmatched = []
 
    for student in students_df.index:
        course = matching.get(student)
        if course is None:
            unmatched.append(student)
            continue
        rank = students_df.loc[student, course]
        ranks.append(rank)
        if rank == students_df.loc[student].min():
            top_choice += 1
 
    n = len(students_df)
    return {
        "mean_rank":      round(sum(ranks) / len(ranks), 3) if ranks else None,
        "top_choice_pct": round(top_choice / n * 100, 1),
        "unmatched":      unmatched,
    }

rsd_blocking = blocking_pairs(rsd_matching, students_df, courses_df, courses_quota)
da_blocking  = blocking_pairs(da_matching,  students_df, courses_df, courses_quota)
 
rsd_swaps = pareto_improving_swaps(rsd_matching, students_df)
da_swaps  = pareto_improving_swaps(da_matching,  students_df)
 
rsd_satisfaction = performance_summary(rsd_matching, students_df)
da_satisfaction  = performance_summary(da_matching,  students_df)

print("=" * 50)
print(f"{'Metric':<30} {'RSD':>8} {'DA':>8}")
print("=" * 50)
print(f"{'Blocking pairs':<30} {len(rsd_blocking):>8} {len(da_blocking):>8}")
print(f"{'Pareto-improving swaps':<30} {len(rsd_swaps):>8} {len(da_swaps):>8}")
print(f"{'Mean preference rank':<30} {rsd_satisfaction['mean_rank']:>8} {da_satisfaction['mean_rank']:>8}")
print(f"{'Top choice %':<30} {rsd_satisfaction['top_choice_pct']:>7}% {da_satisfaction['top_choice_pct']:>7}%")
print(f"{'Unmatched students':<30} {len(rsd_satisfaction['unmatched']):>8} {len(da_satisfaction['unmatched']):>8}")
print("=" * 50)
 
if rsd_blocking:
    print(f"\nRSD blocking pairs: {rsd_blocking}")
if da_blocking:
    print(f"DA blocking pairs:  {da_blocking}")
if rsd_swaps:
    print(f"\nRSD Pareto-improving swaps: {rsd_swaps}")
if da_swaps:
    print(f"DA Pareto-improving swaps:  {da_swaps}")
 