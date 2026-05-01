from datetime import date

from src.scraper.courses_scraper import get_course_page_data




def parse_course_lines(lines):
    data = {
        "course_code": None,
        "course_title": None,
        "instructor": None,
        "last_taught": None,
        "sections": [],
        "review_summary": None,
        "review_count": None,
        "class_size": 0,
    }

    # basic course metadata
    data["course_code"] = lines[20]
    data["course_title"] = lines[21]
    data["instructor"] = lines[22]


    if lines[23].startswith("Last taught:"):
        data["last_taught"] = lines[23].replace("Last taught:", "").strip()


    # sections
    i = 0
    while i < len(lines):
        if lines[i] == "Review Summary":
            break

        if lines[i].startswith("Section "):
            section = {
                "section_number": lines[i].replace("Section ", "").strip(),
                "type": lines[i + 1] if i + 1 < len(lines) else None,
                "units": lines[i + 2].replace("(", "").replace(")", "") if i + 2 < len(lines) else None,
                "time": lines[i + 3] if i + 3 < len(lines) else None,
                "enrolled": None,
                "waitlist": None,
                "class_size": 0,
            }

            j = i + 1

            while j < len(lines):
                if lines[j].startswith("Section ") or lines[j] == "Review Summary":
                    break

                if j + 1 < len(lines) and lines[j] == "Enrolled:":
                    section["enrolled"] = lines[j + 1]

                    if '/' in section["enrolled"]:
                        current, capacity = section["enrolled"].split("/")
                        section["class_size"] = int(capacity)

                if j + 1 < len(lines) and lines[j] == "Waitlist:":
                    section["waitlist"] = lines[j + 1]

                j += 1



            data["sections"].append(section)
            i = j
        else:
            i += 1



    # review summary
    if "Review Summary" in lines:
        idx = lines.index("Review Summary")

        if idx + 2 < len(lines):
            data["review_summary_updated"] = lines[idx + 1]
            data["review_summary"] = lines[idx + 2]

        if idx + 3 < len(lines) and "Reviews" in lines[idx + 3]:
            data["review_count"] = lines[idx + 3]

    for section in data["sections"]:
        data["class_size"] += section["class_size"]

    return data


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



