from PIL import Image, ImageFont, ImageDraw

def annotate_image(path, face_data):
    TINT_COLOR = (180, 180, 180)

    img = Image.open(path).convert("RGBA")
    font = ImageFont.truetype("/home/ec2-user/daily-picture-bot/ai/ShareTechMono.ttf", 100)
    width, height = img.size

    for f in face_data:
        overlay = Image.new("RGBA", img.size, TINT_COLOR + (0,))
        draw = ImageDraw.Draw(overlay)

        _, _, r, b = draw.textbbox(
            (f["box"]["Left"] * width + 20, f["box"]["Top"] * height + 20),
            f["userid"] if f["userid"] else "<unknown>",
            font=font,
        )

        draw.rounded_rectangle(
            (
                f["box"]["Left"] * width,
                f["box"]["Top"] * height,
                max((f["box"]["Left"] + f["box"]["Width"]) * width, r + 20),
                max((f["box"]["Top"] + f["box"]["Height"]) * height, b + 20),
            ),
            fill=TINT_COLOR + (100,),
            radius=20,
        )

        draw.text(
            (f["box"]["Left"] * width + 20, f["box"]["Top"] * height + 20),
            f["userid"] if f["userid"] else "<unknown>",
            font=font,
        )

        img = Image.alpha_composite(img, overlay)
   
    new_path = '_annotated.'.join(path.rsplit(".", 1))
    img.save(new_path, "PNG")
