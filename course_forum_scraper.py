import requests
from bs4 import BeautifulSoup

course_forum_url = "https://thecourseforum.com"

def get_soup_list(url, subject="CS"):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    pre = subject + " "
    soup_list = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(" ", strip=True)
        if "/course/" in href or text.startswith(pre):
            soup_list.append((text, href))

    return soup_list

def get_course_addrs(department="31"):
    courses_url = course_forum_url + "/department/" + department + "?page="
    course_links = []
    page = 1
    end = False
    while not end:
        print("page: ", page)
        curr_course_url = courses_url + str(page)
        print("courses_url: ", curr_course_url)
        course_list = get_soup_list(curr_course_url)

        # First pass: pull all links that look like course links
        for c in course_list:
            if c in course_links:
                print("Course is in course links. Past max page.")
                end = True
                break
            print("Adding course: ", c)
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

        section_url = course_forum_url + item_list[-1]
        section_list = get_soup_list(section_url)

        # First pass: pull all links that look like course links
        section_links = []
        for s in section_list:
            if not "?mode=clubs" in s.href and not s.href.startswith("/login"):
                section_links.append(s)

        for item in section_links[:20]:
            print(item)
            item_list = list(item)
            print(f"href: {item_list[-1]}")

        course_section_dict[item_list[-1]] = section_links

    return course_section_dict

# def get_course_reviews(course_section_dict):
#
# test_course_sect = course_section_dict[list(course_section_dict.keys())[0]]
# print(test_course_sect)
# value = test_course_sect[1]
# href = list(value)[-1]
# print(href)
#
# tester = get_soup_list(course_forum_url+href)
# print(tester)