from PIL import Image, ImageDraw, ImageFont


def createimage(num_views):
    image = Image.open('thumbnail.png')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('muller.otf', size=170)
    (x, y) = (100, 200)
    message = "this video has"
    color = 'rgb(255, 255, 255)'
    draw.text((x, y), message, fill=color, font=font)

    (x, y) = (100, 400)
    views_text = str(num_views) + " views"
    draw.text((x, y), views_text, fill=color, font=font)

    image.save('final.png')