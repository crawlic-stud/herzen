import requests
import bs4

from datetime import datetime, timedelta

from utils import get_random_emoji

from . import parser


MSG_END = "msgend"


def get_full_schedule_link(branch, study_form, group):
    return parser.get_schedule_data()[branch][study_form][group]["полное расписание"]


def get_date_schedule_link(branch, study_form, group):
    return parser.get_schedule_data()[branch][study_form][group]["расписание по датам"]


def construct_one_day_link(base_link, date):
    return f"{base_link}&date1={date.strftime('%Y-%m-%d')}&date2={date.strftime('%Y-%m-%d')}"


def get_today_link(base_link): 
    return construct_one_day_link(base_link, datetime.now())


def get_tomorrow_link(base_link):
    return construct_one_day_link(base_link, datetime.now() + timedelta(days=1))


def process_row(row):
    row_text = ""
    ths = [t.getText().strip() for t in row.find_all("th")]
    tds = [t.getText().strip().replace("                          ", "\n") for t in row.find_all("td")]
    a_tags = row.find_all("a")
    a_texts = [t.getText().strip() for t in a_tags]

    # если дисциплин больше одной в списке, значит разделено на группы
    if len(tds) > 1:
        tds = [f"{i + 1} группа: \n\t\t{t}" for i, t in enumerate(tds)]

    # если есть <a> в списке дисциплин
    for a_tag, a_text in zip(a_tags, a_texts):
        tds = [td.replace(a_text, f"<i>{str(a_tag)}</i>") for td in tds]

    # если есть неделя с временем
    if len(ths) > 1:
        row_text += f"\n<pre>{ths[0]}</pre>\n<b>неделя</b>: {ths[1]}" if ths[1] else f"\n<pre>{ths[0]}</pre>\n"
    
    # если есть неделя, но нет времени
    elif any(len(th) < 2 for th in ths):
        row_text += f"\n<b>неделя</b>: {ths[0]}"

    # если только время
    elif any("—" in th for th in ths):
        row_text += f"\n<pre>{ths[0]}</pre>\n"

    # если день недели
    else:
        row_text += f"\n{MSG_END}<u><b>\n{ths[0].upper()}</b></u>\n"

    # добавляются дисциплины если есть
    if tds:
        row_text += "\t\t" + "\n".join(tds) + "\n" \
            if not any("группа" in td for td in tds) else "\n".join(tds) + "\n"
    return row_text


def get_table_from_link(link):
    req = requests.get(link)
    if req.status_code != 200:
        return "Bad response"

    soup = bs4.BeautifulSoup(req.text, "html.parser")
    table = soup.find("table", class_="schedule")
    if table is None:
        return [f"<a href='{link}'>Расписание</a> не найдено :("]

    body = table.find("tbody")
    rows = body.find_all("tr")

    text = ""
    for row in rows:
        text += process_row(row)
    text += f"\n*расписание взято с <a href='{link}'>оф. сайта {get_random_emoji()}</a>\n"
    texts = list(filter(lambda x: x and len(x) > 1, text.split(MSG_END)))
    return texts


if __name__ == "__main__":
    pass
