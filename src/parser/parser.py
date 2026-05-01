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
    }

    # basic course metadata
    data["course_code"] = lines[20]
    data["course_title"] = lines[21]
    data["instructor"] = lines[22]

    if lines[23].startswith("Last taught:"):
        data["last_taught"] = lines[23].replace("Last taught:", "").strip()

    # sections
    i = 56
    while i < len(lines):
        if lines[i] == "Review Summary":
            break

        if lines[i].startswith("Section "):
            section = {
                "section_number": lines[i].replace("Section ", "").strip(),
                "type": lines[i + 1],
                "units": lines[i + 2].replace("(", "").replace(")", ""),
                "time": lines[i + 3],
                "enrolled": None,
                "waitlist": None,
                "rating": None,
                "enjoyability": None,
                "difficulty": None,
                "recommend": None,
                "reading": None,
                "writing": None,
                "groupwork": None,
                "total_hours": None,
                "average_gpa": None,
            }

            if i + 5 < len(lines) and lines[i + 4] == "Enrolled:":
                section["enrolled"] = lines[i + 5]

            if i + 7 < len(lines) and lines[i + 6] == "Waitlist:":
                section["waitlist"] = lines[i + 7]

            data["sections"].append(section)
            i += 8
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

    return data