from src.save_json import save_json
from src.scraper.courses_scraper import get_soup_list, get_course_addrs, get_course_section_dict, get_course_page_data

course_forum_url = "https://thecourseforum.com"
subject="CS"
department="31"

if __name__ == '__main__':
    ## code to get each of the course-section dictionaries for the given department:
    course_soup_list = get_soup_list(course_forum_url)
    course_addrs = get_course_addrs(department="31")
    # save_json(course_addrs, "course_links.json")
    course_section_dict = get_course_section_dict(course_addrs)
    # print(course_section_dict)
    # save_json(course_section_dict, "course_sections.json")



    list_course_section_dict = list(course_section_dict.values())

    href = course_addrs[0]
