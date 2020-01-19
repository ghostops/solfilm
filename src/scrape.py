import datetime
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.timeanddate.com/sun/iceland/reykjavik?month={}&year={}"

def extract(soup, class_):
    result = soup.find_all('td', class_=class_)

    res = []

    for elem in result:
        # hack alert:
        # if the lenght of the string is "large" it contains a span element
        # and if it contains said span element it is the column we are looking for
        if len(str(elem)) > 99:
            res.append(elem.text[:5])

    return res

def scrape(month, year):
    url = BASE_URL.format(month, year)
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    # class names makes little sense to me
    sunrises = extract(soup, 'c sep')
    sunsets = extract(soup, 'sep c')

    return { 'sunrises': sunrises, 'sunsets': sunsets }

def scrape_data():
    today = datetime.datetime.today()
    last_week = today - datetime.timedelta(days=7)

    # if both year and month is same we only make one request
    same = (today.month == last_week.month) and (today.year == last_week.year)

    months = {}

    months[last_week.month] = scrape(last_week.month, last_week.year)

    # if the weeks are not same month/year we need to do an additional scrape
    # to obtain the data for that specific month
    if not same:
        months[today.month] = scrape(today.month, today.year)

    todays_sunrise = months[today.month]['sunrises'][today.day - 1]
    todays_sunset = months[today.month]['sunsets'][today.day - 1]

    last_week_sunrise = months[today.month]['sunrises'][last_week.day - 1]
    last_week_sunset = months[today.month]['sunsets'][last_week.day - 1]

    return {
        'last_week_sunrise': last_week_sunrise,
        'last_week_sunset': last_week_sunset,
        'todays_sunrise': todays_sunrise,
        'todays_sunset': todays_sunset
    }
