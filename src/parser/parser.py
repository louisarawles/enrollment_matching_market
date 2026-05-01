from datetime import date

from src.save_json import load_json
from src.scraper.courses_scraper import get_course_page_data




def parse_course_lines(lines):
    data = {
        "course_code": None,
        "course_title": None,
        "instructor": None,
    }
    # print(lines)
    # basic course metadata
    for i, line in enumerate(lines):
        if line.startswith("CS ") and i + 2 < len(lines):
            data["course_code"] = line.strip()
            if i + 1 < len(lines):
                data["course_title"] = lines[i+1]
            if i + 2 < len(lines):
                data["instructor"] = lines[i+2]
            break

    return data

def parse_class_size(lines):
    total = 0
    i = 0
    current_type = None

    while i < len(lines):
        if lines[i] in ("Lecture", "Seminar"):
            current_type = lines[i]

        if lines[i] == "Enrolled:" and i+1 < len(lines):
            val = lines[i + 1]
            if '/' in val:
                try:
                    _, capacity = val.split("/")
                    total += int(capacity.strip())
                except ValueError:
                    pass
        i += 1

    return total

def parse_avg_gpa(sections):
    gpas = []
    for section in sections:
        text = section[0]
        parts = text.split(" ")

        gpa = parts[len(parts) - 2]
        if gpa != '\u2014':
            val = float(gpa)
            if val > 0.0:
                gpas.append(val)

    return float(sum(gpas)) / float(len(gpas))


FIELDS = {
    "Rating": "rating",
    "Difficulty": "difficulty",
    "GPA": "gpa",
    "Enjoyability": "enjoyability",
    "Recommend": "recommend",
    "Reading": "reading",
    "Writing": "writing",
    "Groupwork": "groupwork",
    "Total Hours": "total_hours",
}

# def section_review_metrics(file):
#     with open('../scraper/data/raw/course_sections.json') as f:


def parse_review_metrics(lines):
    reviews = []
    current = None

    for i, line in enumerate(lines):
        # Start of a review: semester, then score, then "Average"
        # print(i, line)
        if i + 2 < len(lines) and lines[i + 2] == "Average":
            if current:
                reviews.append(current)

            current = {
                "semester": line,
                "rating": float(lines[i + 1]),
                "instructor": None,
                "enjoyability": None,
                "recommend": None,
                "difficulty": None,
                "hours_per_week": None,
            }

        if current:
            if line == "Instructor":
                if (i + 1) >= len(lines):
                    val = 0
                else:
                    val = float(lines[i + 1])
                current["instructor"] = val
            elif line == "Enjoyability":
                if (i + 1) >= len(lines):
                    val = 0
                else:
                    val = float(lines[i + 1])
                current["enjoyability"] = val
            elif line == "Recommend":
                if (i + 1) >= len(lines):
                    val = 0
                else:
                    val = float(lines[i + 1])
                current["recommend"] = val
            elif line == "Difficulty":
                if (i + 1) >= len(lines):
                    val = 0
                else:
                    val = float(lines[i + 1])
                current["difficulty"] = val
            elif line == "Hours/Week":
                if (i + 1) >= len(lines):
                    val = 0
                else:
                    val = float(lines[i + 1])
                current["hours_per_week"] = val

    if current:
        reviews.append(current)

    return reviews

def average_field(reviews, field):
    vals = [r[field] for r in reviews if r.get(field) is not None]
    return round(sum(vals) / len(vals), 4) if vals else None



