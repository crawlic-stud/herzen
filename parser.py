import bs4
import requests

import re
import json

from get_elements import *


BASE_URL = "https://guide.herzen.spb.ru"
SCHEDULE_URL = BASE_URL + "/static/schedule.php"


def get_schedule_data():
    req = requests.get(SCHEDULE_URL)
    if req.status_code != 200:
        return "Bad response"
    
    soup = bs4.BeautifulSoup(req.text, "html.parser")

    # all branches names from page
    branches = soup.find_all("h3", class_=None)
    branches_names = [branch.getText().strip() for branch in branches]

    divs = get_divs(soup)
    schedule_data = {}
    for branch, div in zip(branches_names, divs):
        study_forms = [h4.getText().strip() for h4 in get_h4_headers(div)]
        uls = get_uls(div)
        
        schedule_data[branch] = {form: None for form in study_forms} 

        for study_form, ul in zip(study_forms, uls):
            lis = get_lis(ul)
            study_groups = [li.find(text=True, recursive=False).strip() for li in lis]
            
            schedule_data[branch][study_form] = {group: None for group in study_groups}

            for study_group, li in zip(study_groups, lis):
                buttons = get_buttons(li)
                full_links = [BASE_URL + extract_full_link(btn.get("onclick")) for btn in buttons]
                base_links = [BASE_URL + extract_base_link(btn.get("onclick")) for btn in buttons]

                schedule_data[branch][study_form][study_group] = {
                    type_: link
                    for link_type in zip(full_links, base_links) 
                    for type_, link in zip(("полное расписание", "базовая ссылка"), link_type) 
                } 
                    

    print(json.dumps(schedule_data["Выборгский филиал"], indent=4, ensure_ascii=False))
    return schedule_data


if __name__ == "__main__":
    schedule = get_schedule_data()
