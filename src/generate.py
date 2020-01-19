import datetime
import os
import boto3

# internal packages
import scrape
import images
import helpers

# Script should run on mondays
WEEK = datetime.date.today().isocalendar()[1]
SRC_DIR = 'source'
OUT_DIR = 'generated'

def generate_images(data):
    generator = images.Generator(SRC_DIR, OUT_DIR)

    generator.set_up_text(
        data['last_week_sunrise'],
        data['todays_sunrise'],
        helpers.calc_diff(data['last_week_sunrise'], data['todays_sunrise'])
    )

    generator.set_down_text(
        data['last_week_sunset'],
        data['todays_sunset'],
        helpers.calc_diff(data['last_week_sunset'], data['todays_sunset'])
    )

    generator.set_intro_text("Solfilm Week {}".format(WEEK))

def render_video():
    # command = "ffmpeg -y -i source.mp4 -i generated/intro.png -i generated/up.png -i generated/down.png -filter_complex \"[0:v][1:v] overlay=enable='between(t,0,6)' [tmp]; [tmp][2:v] overlay=enable='between(t,9,32)' [tmp2]; [tmp2][3:v] overlay=enable='between(t,33,49)'\" generated/output.mp4"
    command = [
        "ffmpeg -y -i source/solfilmen.mp4 -i generated/intro.png -i generated/up.png -i generated/down.png",
        "-filter_complex \"[0:v][1:v] overlay=enable='between(t,0,6)' [tmp];",
        "[tmp][2:v] overlay=enable='between(t,9,32)' [tmp2]; [tmp2][3:v] overlay=enable='between(t,33,49)'\"",
        "{}/output.mp4".format(OUT_DIR)
    ]

    os.system(" ".join(command))

def upload_video():
    s3 = boto3.client('s3')
    with open("./generated/output.mp4", "rb") as f:
        s3.upload_fileobj(f, "solfilm", "week-{}.mp4".format(WEEK), ExtraArgs={'ACL':'public-read'})


if not os.path.exists(OUT_DIR):
    os.mkdir(OUT_DIR)

generate_images(scrape.scrape_data())

render_video()

# upload_video()

print("done")
