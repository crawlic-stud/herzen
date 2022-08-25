import bs4
import requests

import re


BASE_URL = "https://guide.herzen.spb.ru"
SCHEDULE_URL = BASE_URL + "/static/schedule.php"


def get_schedule():
    req = requests.get(SCHEDULE_URL)
    if req.status_code != 200:
        return "Bad response"
    
    soup = bs4.BeautifulSoup(req.text, "html.parser")
    branches = soup.find_all("h3", class_=lambda x: x != "title")
    branches_names = [branch.getText() for branch in branches]

    lst_divs = soup.find_all("div", id=lambda x: x is not None and "lst" in x, class_=None)
    lst_divs_texts = [div.getText().replace("\xa0по датам", "") for div in lst_divs]
    lst_splitted =  [text.split("\n") for text in lst_divs_texts]
    lst_final = [list(filter(lambda x: len(x) > 1, lst)) for lst in lst_splitted]

    #uls = soup.find_all("ul")
    #uls_texts = [ul.getText() for ul in uls]
    #groups = soup.find_all("li", class_=lambda x: x == "ev" or x is None)
    #groups_texts = [group.getText() for group in groups]

    buttons = soup.find_all("button")
    buttons_commands = [button.get("onclick") for button in buttons if button.get("onclick") is not None]
    buttons_commands = list(filter(lambda x: "window.open" in x and "&sem=" in x, buttons_commands))

    print(len(branches_names), len(lst_divs_texts))
    print("\n".join(buttons_commands))
    #print(list(zip(lst_final[0], lst_final[0])))
    print("="*80)
    return zip(branches_names, lst_final)


if __name__ == "__main__":
    print(list(get_schedule())[0])
