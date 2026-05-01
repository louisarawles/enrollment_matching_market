import json
from src.parser.parser import parse_course_lines, parse_class_size, parse_review_metrics, average_field, parse_avg_gpa
from src.save_json import save_json
from src.scraper.courses_scraper import get_course_page_data

if __name__ == '__main__':
    # global list of all courses covering all sections
    all_courses = []
    with open('../scraper/data/raw/course_sections.json') as f:
        courses_data = json.load(f)
        for course_key, sections in courses_data.items():
            # course overview / general data
            raw_course_key = course_key.split(":")
            course_code = raw_course_key[0]
            department = course_code.split(" ")[0]
            course_title = raw_course_key[1]

            course_reviews = []
            total_class_size = 0

            # aggregate course data from all sections for average ratings and total class size
            sections = sections[1:]
            for section in sections:
                url = section[1]
                section_data = get_course_page_data(url)
                # structure web page data lines for parsing
                text_lines = []
                for i, line in enumerate(section_data["title"][:120]):
                    text_lines.append(line)
                # extract section review information
                course_reviews.extend(parse_review_metrics(text_lines))
                # update course's total class size
                total_class_size += parse_class_size(text_lines)
            # average rating features for a course across sections
            # temporary hard-coded reading/writing/groupwork data (ultimately still using course forum) because of javascript issues
            features = {
                "avg_gpa": parse_avg_gpa(sections),
                "avg_rating": average_field(course_reviews, "rating"),
                "avg_instructor": average_field(course_reviews, "instructor"),
                "avg_enjoyability": average_field(course_reviews, "enjoyability"),
                "avg_recommend": average_field(course_reviews, "recommend"),
                "avg_difficulty": average_field(course_reviews, "difficulty"),
                "avg_hours_per_week": average_field(course_reviews, "hours_per_week"),
                "num_reviews": len(course_reviews),
                "reading": 0.0,
                "writing": 0.0,
                "group_work": 0.0,
            }
            # cleaned course data including class size
            cleaned_course_data = {
                "department": department,
                "course_code": course_code,
                "course_title": course_title,
                "class_size": total_class_size,
            }

            # combine review data and course data
            new_data = {**cleaned_course_data, **features}
            # add to all courses list
            all_courses.append(new_data)
    # save aggregated course data to json file
    save_json(all_courses, "processed_courses.json")
