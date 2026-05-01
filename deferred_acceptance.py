# This project includes code from deferred_acceptance_school_choice by Kyosuke Morita
# (https://github.com/kyosek/deferred_acceptance_school_choice/tree/master)
# Copyright (c) 2022 Kyosuke Morita
# Licensed under the MIT License

from collections import Counter
from copy import copy
from typing import Optional

import pandas as pd


def da(
    students_df: pd.DataFrame,
    courses_df: pd.DataFrame,
    courses_quota: dict,
    verbose: Optional[int] = 0,
) -> dict:
    """
    Deferred Acceptance (student-proposing) for student-course matching.
 
    Args:
        students_df:    DataFrame[students × courses] — student preference ranks
                        (lower = more preferred).
        courses_df:     DataFrame[students × courses] — course preference ranks
                        over students (lower = more preferred).
        courses_quota:  Dict mapping each course to its capacity (int).
        verbose:        0 = silent; any other value prints iteration count.
 
    Returns:
        Dict mapping each student to their assigned course: {student: course, ...}.
    """

    # Create the initial environments for matching
    available_course = {
        student: list(students_df.columns.values)
        for student in list(students_df.index.values)
    }
    unassigned_students = []
    matches = {}
    itr_count = 0

    # Start matching
    while len(unassigned_students) < len(students_df):
        for student in students_df.index:
            if student not in unassigned_students:
                course = available_course[student]
                remaining = students_df.loc[student][students_df.loc[student].index.isin(course)]
                if remaining.empty:
                    unassigned_students.append(student)
                    continue
                best_choice = remaining.idxmin()
                matches[(student, best_choice)] = (
                    students_df.loc[student][best_choice],
                    courses_df.loc[student][best_choice],
                )

        # Count applications in school
        courses_applications = Counter([key[1] for key in matches.keys()])

        for course in courses_applications.keys():
            if courses_applications[course] > courses_quota[course]:
                pairs_to_drop = sorted(
                    {
                        pair: matches[pair] for pair in matches.keys() if course in pair
                    }.items(),
                    key=lambda x: x[1][1],
                )[courses_quota[course]:]

                for p_to_drop in pairs_to_drop:
                    del matches[p_to_drop[0]]
                    _course = copy(available_course[p_to_drop[0][0]])
                    _course.remove(p_to_drop[0][1])
                    available_course[p_to_drop[0][0]] = _course

        unassigned_students = [student[0] for student in matches.keys()]
        itr_count += 1

    if verbose != 0:
        print(f"Number of iterations: {itr_count}")

    return {student: course for student, course in matches.keys()}