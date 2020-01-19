from wand.image import Image
from wand.image import Color
from wand.font import Font

class Generator:
    def __init__(self, src_dir, out_dir):
        self.src = src_dir
        self.out = out_dir

        self.FONT = Font(path="{}/font.ttf".format(src_dir), color=Color("#ffffff"))

    def set_text(self, img, txt, top):
        img.caption(
            text=txt,
            font=self.FONT,
            width=200,
            left=194,
            height=22,
            top=top,
            gravity='west'
        )

    def set_up_text(self, last_week, today, diff):
        img = Image(filename="{}/up.png".format(self.src))

        self.set_text(img, today, 196)
        self.set_text(img, last_week, 222)
        self.set_text(img, diff, 249)

        img.save(filename="{}/up.png".format(self.out))

    def set_down_text(self, last_week, today, diff):
        img = Image(filename="{}/down.png".format(self.src))

        self.set_text(img, today, 60)
        self.set_text(img, last_week, 86)
        self.set_text(img, diff, 112)

        img.save(filename="{}/down.png".format(self.out))

    def set_intro_text(self, txt):
        img = Image(filename="{}/blank.png".format(self.src))

        img.caption(
            text=txt,
            font=self.FONT,
            width=522,
            left=0,
            height=60,
            top=200,
            gravity='center'
        )

        img.save(filename="{}/intro.png".format(self.out))
