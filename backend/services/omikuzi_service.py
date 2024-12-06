from PIL import Image, ImageDraw, ImageFont
#縦向きの文字を追加
def add_text_to_image_vertical(img, text, position, font_path, font_size, text_color=(0, 0, 0)):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, font_size)
    draw.text(position, text, fill=text_color, font=font,direction='ttb')
    return img
#横向きの文字を追加
def add_text_to_image_horizontal(img, text, position, font_path, font_size, text_color=(0, 0, 0)):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, font_size)
    draw.text(position, text, fill=text_color, font=font)
    return img
#画像を追加
def add_image_to_image(base_img,add_img ,position, size):
    base_img.paste(add_img.resize(size), position)
    return base_img