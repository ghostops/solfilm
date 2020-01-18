import datetime
import os
import boto3
from wand.image import Image
from wand.image import Color
from wand.font import Font

FONT = Font(path="./font.ttf", color=Color("#ffffff"))
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

def set_up_text():
    img = Image(filename="./img/up.png")

    set_text(img, "17:32", 192)
    set_text(img, "18:32", 218)
    set_text(img, "19:32", 244)

    img.save(filename="generated/up.png")

def set_down_text():
    img = Image(filename="./img/down.png")

    set_text(img, "17:32", 56)
    set_text(img, "18:32", 82)
    set_text(img, "19:32", 108)

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
        s3.upload_fileobj(f, "solfilm", "week-{}.mp4".format(WEEK))

# set_up_text()
# set_down_text()
set_intro_text()

# render_video()

upload_video()

print("done")
