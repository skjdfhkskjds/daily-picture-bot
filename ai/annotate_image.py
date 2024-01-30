from PIL import Image, ImageFont, ImageDraw

def annotate_image(path, face_data):
    TINT_COLOR = (180, 180, 180)

    img = Image.open(path).convert("RGBA")
    font = ImageFont.truetype("ShareTechMono.ttf", 40)
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
    
    img.save("/home/hello/Documents/Projects/faces/test.png", "PNG")

def main():
    TEST_PATH = "/home/hello/Downloads/test.jpg"
    TEST_DATA = [{'faceid': 'd56d8bee-4464-49b0-82e2-15c907bd8f43', 'box': {'Width': 0.2081323266029358, 'Height': 0.3753466308116913, 'Left': 0.7869119644165039, 'Top': 0.45688894391059875}, 'userid': 'chauvin'}, {'faceid': '729d879c-9dc9-4106-a8ae-50e785f7ba83', 'box': {'Width': 0.12813244760036469, 'Height': 0.17957811057567596, 'Left': 0.8237026333808899, 'Top': 0.2509934604167938}, 'userid': 'ocean'}, {'faceid': '53917b90-fe59-467d-add0-833996918147', 'box': {'Width': 0.113661989569664, 'Height': 0.19403177499771118, 'Left': 0.03759138658642769, 'Top': 0.3346938490867615}, 'userid': None}, {'faceid': 'bc00e047-2ece-4537-b9e7-e8be15597065', 'box': {'Width': 0.1008516252040863, 'Height': 0.16246967017650604, 'Left': 0.7045372724533081, 'Top': 0.28291812539100647}, 'userid': 'justin'}, {'faceid': '9194adfa-3a23-49b4-857b-b3e1d016b224', 'box': {'Width': 0.08790697902441025, 'Height': 0.1647626906633377, 'Left': 0.23839350044727325, 'Top': 0.284637451171875}, 'userid': 'nolan'}, {'faceid': '15fdcb57-32e1-4d0b-839c-afaaa0145531', 'box': {'Width': 0.06529473513364792, 'Height': 0.11129532754421234, 'Left': 0.687730610370636, 'Top': 0.16116802394390106}, 'userid': 'angela'}, {'faceid': '8e82e486-b9ad-4b00-8d40-8fef193a9f1f', 'box': {'Width': 0.06591024994850159, 'Height': 0.09590703994035721, 'Left': 0.3311034142971039, 'Top': 0.2432669848203659}, 'userid': 'jaidyn'}, {'faceid': '02f405fe-7b6b-431d-9925-cdff54fa35d0', 'box': {'Width': 0.048563506454229355, 'Height': 0.07794459909200668, 'Left': 0.42806586623191833, 'Top': 0.21031402051448822}, 'userid': 'marco'}, {'faceid': '1eda6b1a-86a6-4605-9844-074eeb58c7e2', 'box': {'Width': 0.044252775609493256, 'Height': 0.06737646460533142, 'Left': 0.5076159238815308, 'Top': 0.16542604565620422}, 'userid': 'andie'}, {'faceid': 'd2f6d43c-8c3d-46c6-b6fc-834bee7229f9', 'box': {'Width': 0.021102501079440117, 'Height': 0.06272727251052856, 'Left': 0.08038347959518433, 'Top': 0.17823679745197296}, 'userid': None}]

    annotate_image(TEST_PATH, TEST_DATA)

if __name__ == "__main__":
    main()