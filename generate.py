import time
import datetime
import os
import boto3
import requests
from wand.image import Image
from wand.image import Color
from wand.font import Font
from bs4 import BeautifulSoup

FONT = Font(path="./font.ttf", color=Color("#ffffff"))
# Script should run on mondays
WEEK = datetime.date.today().isocalendar()[1]

def set_text(img, txt, top):
    img.caption(
        text=txt,
        font=FONT,
        width=200,
        left=188,
        height=25,
        top=top,
        gravity='west'
    )

def set_up_text(last_week, today, diff):
    img = Image(filename="./img/up.png")

    set_text(img, today, 192)
    set_text(img, last_week, 218)
    set_text(img, diff, 244)

    img.save(filename="generated/up.png")

def set_down_text(last_week, today, diff):
    img = Image(filename="./img/down.png")

    set_text(img, today, 56)
    set_text(img, last_week, 82)
    set_text(img, diff, 108)

    img.save(filename="generated/down.png")

def set_intro_text():
    img = Image(filename="./img/intro.png")

    img.caption(
        text="Solfilm Week {}".format(WEEK),
        font=FONT,
        width=522,
        left=0,
        height=60,
        top=200,
        gravity='center'
    )

    img.save(filename="generated/intro.png")

def render_video():
    # command = "ffmpeg -y -i source.mp4 -i generated/intro.png -i generated/up.png -i generated/down.png -filter_complex \"[0:v][1:v] overlay=enable='between(t,0,6)' [tmp]; [tmp][2:v] overlay=enable='between(t,9,32)' [tmp2]; [tmp2][3:v] overlay=enable='between(t,33,49)'\" generated/output.mp4"
    command = [
        "ffmpeg -y -i source.mp4 -i generated/intro.png -i generated/up.png -i generated/down.png",
        "-filter_complex \"[0:v][1:v] overlay=enable='between(t,0,6)' [tmp];",
        "[tmp][2:v] overlay=enable='between(t,9,32)' [tmp2]; [tmp2][3:v] overlay=enable='between(t,33,49)'\"",
        "generated/output.mp4"
    ]

    os.system(" ".join(command))

def upload_video():
    s3 = boto3.client('s3')
    with open("./generated/output.mp4", "rb") as f:
        s3.upload_fileobj(f, "solfilm", "week-{}.mp4".format(WEEK), ExtraArgs={'ACL':'public-read'})

def scrape_data():
    today = datetime.datetime.today()
    last_week = today - datetime.timedelta(days=7)

    # if both year and month is same we only make one request
    same = (today.month == last_week.month) and (today.year == last_week.year)

    base = "https://www.timeanddate.com/sun/iceland/reykjavik?month={}&year={}"

    def scrape(month, year):
        url = base.format(month, year)
        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'html.parser')

        def extract(class_):
            result = soup.find_all('td', class_=class_)

            res = []

            for job_elem in result:
                if len(str(job_elem)) > 99:
                    res.append(job_elem.text[:5])

            return res


        sunrises = extract('c sep')
        sunsets = extract('sep c')

        return { 'sunrises': sunrises, 'sunsets': sunsets }

    months = {}

    months[last_week.month] = scrape(last_week.month, last_week.year)

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

def calc_diff(last_week, today):
    lw = datetime.datetime.strptime(last_week, '%H:%M')
    t = datetime.datetime.strptime(today, '%H:%M')
    delta_min = abs((t - lw).total_seconds() / 60)

    if delta_min == 0:
        return '-'

    prefix = '+'

    # this is a funny hack
    if datetime.datetime.now().month > 7:
        prefix = '-'

    stringified = str(int(delta_min))

    return "{}{}".format(prefix, stringified)

data = scrape_data()

set_up_text(
    data['last_week_sunrise'],
    data['todays_sunrise'],
    calc_diff(data['last_week_sunrise'], data['todays_sunrise'])
)
set_down_text(
    data['last_week_sunset'],
    data['todays_sunset'],
    calc_diff(data['last_week_sunset'], data['todays_sunset'])
)
set_intro_text()

render_video()

upload_video()

print("done")
