import random
from typing import Optional
 
import pandas as pd

def rsd(
    students_df: pd.DataFrame,
    courses_quota: dict,
    verbose: Optional[int] = 0,
) -> dict:
    """
    Random Serial Dictatorship for student-course matching.
 
    A single random ordering of students is drawn; each student in turn
    picks their most-preferred course that still has remaining capacity.
 
    Args:
        students_df:    DataFrame where rows=students, columns=courses,
                        cell values are preference ranks (lower = more preferred, 0-indexed).
        courses_quota:  Dict mapping each course identifier to its capacity (int).
        seed:           Optional random seed for reproducibility.
        verbose:        0 = silent; any other value prints the drawn ordering.
 
    Returns:
        Dict mapping each student to their assigned course: {student: course, ...}.
        Students with no available course in their preference list are omitted.
    """
    
    ordering = list(students_df.index)
    random.shuffle(ordering)
 
    if verbose != 0:
        print(f"Student ordering: {ordering}")
 
    remaining_quota = courses_quota.copy()
    matches = {}
 
    for student in ordering:
        prefs = students_df.loc[student].sort_values()
        for course in prefs.index:
            if remaining_quota.get(course, 0) > 0:
                matches[student] = course
                remaining_quota[course] -= 1
                break
 
    return matches
