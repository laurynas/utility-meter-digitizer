from PIL import ImageDraw, ImageFont

def draw_objects(image, objects, color='blue'):
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    offset = font.size + 3

    for obj in objects:
        draw.rectangle(obj.box, outline=color)
        position = obj.box[0], obj.box[1] - offset
        draw.text(position, str(obj.class_id), fill=color, font=font)

    return image
