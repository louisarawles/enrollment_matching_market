import requests
from bs4 import BeautifulSoup

course_forum_url = "https://thecourseforum.com"

def get_soup(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")

def get_soup_list(url, subject="CS"):
    soup = get_soup(url)

    pre = subject + " "
    soup_list = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(" ", strip=True)
        if "/course/" in href or text.startswith(pre):
            soup_list.append((text, href))

    return soup_list

def get_course_page_data(course_href):
    url = course_forum_url + course_href
    soup = get_soup(url)

    text_lines = [
        line.strip()
        for line in soup.get_text("\n").split("\n")
        if line.strip()
    ]

    return {
        "url": url,
        "title": text_lines,
        "soup": soup,
    }

def get_course_addrs(department="31"):
    courses_url = course_forum_url + "/department/" + department + "?page="
    course_links = []
    page = 1
    end = False
    while not end:
        # print("page: ", page)
        curr_course_url = courses_url + str(page)
        # print("courses_url: ", curr_course_url)
        course_list = get_soup_list(curr_course_url)

        # First pass: pull all links that look like course links
        for c in course_list:
            if c in course_links:
                # print("Course is in course links. Past max page.")
                end = True
                break
            # print("Adding course: ", c)
            # new_link = c + "?latest=false"
            course_links.append(c)

        # print(course_links)
        page += 1


    return course_links

def get_course_section_dict(course_links):
    course_section_dict = {}
    for item in course_links[:20]:
        # print(item)
        item_list = list(item)
        # print(f"href: {item_list[-1]}")

        sections_url = course_forum_url + item_list[-1] + "?latest=false"
        section_list = get_soup_list(sections_url)

        # First pass: pull all links that look like course links
        section_links = []
        for s in section_list:
            href = s[1]
            if not "?mode=clubs" in href and not href.startswith("/login"):
                # print("s: ",s)
                section_links.append(s)

        # for item in section_links[:20]:
            # print(item)
            # item_list = list(item)
            # print(f"href: {item_list[-1]}")

        course_section_dict[item_list[-1]] = section_links

    return course_section_dict



#
# ## code to get each of the course-section dictionaries for the given department:
# test_get_soup_list = get_soup_list(course_forum_url)
# test_get_course_addrs = get_course_addrs(department="31")
# test_get_course_section_dict = get_course_section_dict(test_get_course_addrs)
# # print(test_get_course_section_dict)
# test_list_course_section_dict = list(test_get_course_section_dict.values())
#
# value = test_list_course_section_dict[1]
# hrefs = list(test_get_course_section_dict.keys())
# href = hrefs[0]
# print("Tester href: ",href)
#
#
#
# ## get sections of each course
# test_sect_url = course_forum_url + href
# print(test_sect_url)
# course_soup = get_soup_list(test_sect_url)
# print(course_soup)
#
# tester = get_soup_list(test_sect_url)
# print(tester)