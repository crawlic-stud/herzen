# STRUCTURE:
#   div
#    |
#    |
#    |-- header
#    | 
#    |-- ul
#    |    |          
#    |    |--li
#    |    |  |
#    |    |  |-- button


def get_divs(soup):
    return soup.find_all("div", id=lambda x: x is not None and "lst" in x, class_=None)


def get_h4_headers(div):
    return div.find_all("h4")


def get_uls(div):
    return div.find_all("ul")


def get_lis(ul):
    return ul.find_all("li")


def get_buttons(li):
    return li.find_all("button", onclick=lambda c: c is not None, text=lambda t: "по датам" not in t)


def extract_full_link(js_command):
    return js_command[13:js_command.index(",")-1]


def extract_base_link(js_command):
    return f"{js_command[13:js_command.index('&')]}"


def construct_date_link(link, date1, date2):
    pass
