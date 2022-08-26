import pandas as pd
import requests
import bs4

from datetime import datetime, timedelta

import parser


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
    
    # если дисциплин больше одной в списке, значит разделено на группы
    if len(tds) > 1:
        tds = [f"{i + 1} группа: {t}" for i, t in enumerate(tds)]

    # если есть неделя с датой
    if len(ths) > 1:
        row_text += f"\n{ths[0]}\nнеделя: {ths[1]}" if ths[1] else f"\n{ths[0]}"
    
    # если есть неделя, но нет даты
    elif any(len(th) < 2 for th in ths):
        row_text += f"\nнеделя: {ths[0]}"
    
    # если день недели
    else:
        row_text += f"\n<strong>{ths[0].upper()}</strong>\n"

    # добавляются дисциплины если есть
    if tds:
        row_text += "\n" + "\n".join(tds) + "\n"
    return row_text


def get_table_from_link(link):
    print(link)
    req = requests.get(link)
    if req.status_code != 200:
        return "Bad response"

    soup = bs4.BeautifulSoup(req.text, "html.parser")
    table = soup.find("table", class_="schedule")
    if table is None:
        return "Расписание не найдено."

    body = table.find("tbody")
    rows = body.find_all("tr")

    text = ""
    for row in body.find_all("tr"):
        text += process_row(row)
    print(text)

if __name__ == "__main__":
    data = [
        "факультет биологии",
        "очная форма обучения",
        "бакалавриат, 1 курс, группа 1об БИО 1"
    ]
    base_link = get_date_schedule_link(*data)
    date_link = construct_one_day_link(base_link, datetime.now() + timedelta(days=10))
    all_link = get_full_schedule_link(*data)
    test_link = "https://guide.herzen.spb.ru/static/schedule_view.php?id_group=16680&sem=1"
    get_table_from_link(test_link)