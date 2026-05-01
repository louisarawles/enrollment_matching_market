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
    # TO BE ADDED here, adjust postfix to either "?latest=false&page=" or "?latest=false&page="
    courses_url = course_forum_url + "/department/" + department + "?page="
    course_links = []
    page = 1
    end = False
    while not end:
        curr_course_url = courses_url + str(page)
        course_list = get_soup_list(curr_course_url)
        # First pass: pull all links that look like course links
        for c in course_list:
            if c in course_links:
                end = True
                break
            # new_link = c + "?latest=false"
            course_links.append(c)

        # print(course_links)
        page += 1


    return course_links

def get_course_section_dict(course_links):
    course_section_dict = {}
    for item in course_links[:20]:
        info = item[0].split(" ")
        code = info[0] + " " + info[1]
        seasons = ["Fall", "Spring", "Summer", "Winter"]
        i = 2
        token = info[i]
        title = []
        while i < len(info) and token not in seasons:
            title.append(token)
            i += 1
            token = info[i]
        str_title = " ".join(title)
        course_key = code + ":" + str_title

        item_list = list(item)
        # TO BE ADDED: sections should be
        sections_url = course_forum_url + item_list[-1] + "?latest=false"
        section_list = get_soup_list(sections_url)

        # First pass: pull all links that look like course links
        section_links = []
        for s in section_list:
            href = s[1]
            if not "?mode=clubs" in href and not href.startswith("/login"):
                # print("s: ",s)
                section_links.append(s)

        course_section_dict[course_key] = section_links

    return course_section_dict