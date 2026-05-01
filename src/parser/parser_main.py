import json

from src.parser.parser import parse_course_lines
from src.scraper.courses_scraper import get_course_page_data

if __name__ == '__main__':

    with open('../scraper/data/raw/course_sections.json') as f:
        course_links_data = json.load(f)
        for item in course_links_data:
            print(item)
        partial_links = [item for item in course_links_data]


        for link in partial_links:
            print("link: ", link)
            data = get_course_page_data(link)


            text_lines = []
            for i, line in enumerate(data["title"][:120]):
                # print(i, line)
                text_lines.append(line)

            parsed = parse_course_lines(text_lines)

            # print(parsed["course_code"])
            # print(parsed["course_title"])
            # print(parsed["instructor"])
            # print(parsed["sections"])
            print(parsed["review_summary"])