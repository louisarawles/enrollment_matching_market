import json
from src.parser.parser import parse_course_lines, parse_class_size, parse_review_metrics, average_field, parse_avg_gpa, \
    get_global_course_list
from src.save_json import save_json
from src.scraper.courses_scraper import get_course_page_data

if __name__ == '__main__':
    all_courses = get_global_course_list()
    # save aggregated course data to json file
    save_json(all_courses, "processed_courses.json")

