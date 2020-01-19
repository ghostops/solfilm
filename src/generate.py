import boto3
import datetime
import os

# internal packages
import scrape
import images
import helpers

SRC_DIR = 'source'
OUT_DIR = 'generated'
S3_BUCKET = 'solfilm'
# todays date, can also be replaced with a string for debugging
DATE = datetime.date.today().strftime("%d-%m-%Y")

today = datetime.datetime.strptime(DATE, '%d-%m-%Y').date()

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

    generator.set_intro_text("Solfilm Week {}".format(DATE))

def render_video():
    command = [
        "ffmpeg -y -i {0}/solfilmen.mp4 -i {1}/intro.png -i {1}/up.png -i {1}/down.png".format(SRC_DIR, OUT_DIR),
        "-filter_complex \"[0:v][1:v] overlay=enable='between(t,0,6)' [tmp];",
        "[tmp][2:v] overlay=enable='between(t,9,33)' [tmp2]; [tmp2][3:v] overlay=enable='between(t,34,53)'\"",
        "{}/output.mp4".format(OUT_DIR)
    ]

    os.system(" ".join(command))

def upload_video():
    s3 = boto3.client('s3')
    with open("{}/output.mp4".format(OUT_DIR), "rb") as f:
        s3.upload_fileobj(
            f,
            S3_BUCKET,
            "date-{}.mp4".format(DATE),
            ExtraArgs={'ACL':'public-read'}
        )

# create output folder
if not os.path.exists(OUT_DIR):
    os.mkdir(OUT_DIR)

# generate images with dynaic data used to render the video
generate_images(scrape.scrape_data(today))

# render the video with ffmpeg cli
render_video()

# upload the video to s3
upload_video()

print("Done")
