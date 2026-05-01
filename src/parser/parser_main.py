import json
from datetime import date

from src.parser.parser import parse_course_lines, parse_class_size, parse_review_metrics, average_field
from src.save_json import save_json
from src.scraper.courses_scraper import get_course_page_data, get_soup

if __name__ == '__main__':

    all_courses = []
    with open('../scraper/data/raw/course_sections.json') as f:
        courses_data = json.load(f)
        count = 0
        for course in courses_data:
            # print(course)
            course_reviews = []
            sections = courses_data[course]
            sections = sections[1:]
            total_class_size = 0

            overview_data = get_course_page_data(course)
            parsed_course_lines = parse_course_lines(overview_data)
            course_code = parsed_course_lines.get("course_code")
            course_title = parsed_course_lines.get("course_title")


            for section in sections:
                print("Section: ", section)
                url = section[1]
                section_data = get_course_page_data(url)

                text_lines = []
                for i, line in enumerate(section_data["title"][:120]):
                    # print(i, line)
                    text_lines.append(line)
                print(text_lines)

                # parsed_course_lines = parse_course_lines(text_lines)
                # # list_lines = list(parsed_course_lines)[1]
                # # print("Parsed course lines at section loop:", parsed_course_lines)
                # print("Course", course, "class size:", parsed_course_lines.get("class_size"))
                course_reviews.extend(parse_review_metrics(text_lines))
                total_class_size += parse_class_size(text_lines)

            # average rating features for a course across sections
            features = {
                "avg_rating": average_field(course_reviews, "rating"),
                "avg_instructor": average_field(course_reviews, "instructor"),
                "avg_enjoyability": average_field(course_reviews, "enjoyability"),
                "avg_recommend": average_field(course_reviews, "recommend"),
                "avg_difficulty": average_field(course_reviews, "difficulty"),
                "avg_hours_per_week": average_field(course_reviews, "hours_per_week"),
                "num_reviews": len(course_reviews)
            }

            cleaned_course_data = {
                "course_code": course_code,
                "course_title": course_title,
                "class_size": total_class_size,
            }

            new_data = {**cleaned_course_data, **features}

            print(new_data)

            all_courses.append(new_data)

    print(all_courses)
    save_json(all_courses, "processed_courses.json")

    #     for section in sections:
    #         print("Sections: ", section)
    #     partial_links = [course for course in courses_data]
    #
    #     all_courses = []
    #
    #
    #     for link in partial_links:
    #         base_link = "https://thecourseforum.com" + link[1]
    #         print(base_link)
    #
    #         new_link = "https://thecourseforum.com" + link
    #         print(base_link)
    #         data = get_course_page_data(link)
    #
    #         soup = data['soup']
    #
    #
    #         text_lines = []
    #         for i, line in enumerate(data["title"][:120]):
    #             # print(i, line)
    #             text_lines.append(line)
    #
    #         reviews = aggregate_review_metrics(text_lines)
    #
    #         features = {
    #             "avg_rating": average_field(reviews, "rating"),
    #             "avg_instructor": average_field(reviews, "instructor"),
    #             "avg_enjoyability": average_field(reviews, "enjoyability"),
    #             "avg_recommend": average_field(reviews, "recommend"),
    #             "avg_difficulty": average_field(reviews, "difficulty"),
    #             "avg_hours_per_week": average_field(reviews, "hours_per_week"),
    #             "num_reviews": len(reviews),
    #         }
    #
    #
    #
    #         parsed_course_lines = parse_course_lines(text_lines)
    #
    #         course_data = {**parsed_course_lines, **features}
    #
    #         print(course_data)
    #
    #         all_courses.append(course_data)
    #
    # save_json(all_courses, "processed_courses.json")