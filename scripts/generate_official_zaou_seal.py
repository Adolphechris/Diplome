import random
from PIL import Image, ImageDraw, ImageFont

def generate_official_zaou_seal(output_path="assets/university_seal.png"):
    w, h = 480, 300
    seal = Image.new('RGBA', (w, h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(seal)

    # Encre violette d'université
    ink_color = (43, 38, 104, 240)
    ink_light = (43, 38, 104, 180)

    try:
        font_header = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 15)
        font_sub    = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 13)
        font_box    = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        font_bot    = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 12)
    except Exception:
        font_header = font_sub = font_box = font_bot = ImageFont.load_default()

    cx, cy = w // 2, h // 2

    # 1. Bordures ovales parallèles
    draw.ellipse([cx - 225, cy - 135, cx + 225, cy + 135], outline=ink_color, width=4)
    draw.ellipse([cx - 217, cy - 127, cx + 217, cy + 127], outline=ink_color, width=2)
    draw.ellipse([cx - 155, cy - 80,  cx + 155, cy + 80],  outline=ink_light, width=1)

    # 2. En-tête : THE ZAMBIAN OPEN UNIVERSITY
    txt_univ = "THE ZAMBIAN OPEN UNIVERSITY"
    bbox = font_header.getbbox(txt_univ)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - 90), txt_univ, font=font_header, fill=ink_color)

    # 3. Sous-titre : ACADEMIC AFFAIRS
    txt_aff = "ACADEMIC AFFAIRS"
    bbox = font_sub.getbbox(txt_aff)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - 58), txt_aff, font=font_sub, fill=ink_color)

    # 4. Boîte rectangulaire centrale du Sénat
    bw, bh = 240, 46
    bx1, by1 = cx - bw // 2, cy - bh // 2
    bx2, by2 = cx + bw // 2, cy + bh // 2
    draw.rectangle([bx1, by1, bx2, by2], outline=ink_color, width=3)

    txt_sen = "SENATE SECRETARIAT"
    bbox = font_box.getbbox(txt_sen)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2 - 2), txt_sen, font=font_box, fill=ink_color)

    # 5. Mention : DESPATCHED EXAMINATIONS
    txt_des = "DESPATCHED EXAMINATIONS"
    bbox = font_bot.getbbox(txt_des)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy + 32), txt_des, font=font_bot, fill=ink_color)

    # 6. Pied : P.O. BOX LUSAKA - ZAMBIA
    txt_po = "P.O. BOX LUSAKA - ZAMBIA"
    bbox = font_sub.getbbox(txt_po)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy + 58), txt_po, font=font_sub, fill=ink_color)

    # 7. Points latéraux
    draw.ellipse([cx - 195, cy - 4, cx - 187, cy + 4], fill=ink_color)
    draw.ellipse([cx + 187, cy - 4, cx + 195, cy + 4], fill=ink_color)

    # 8. Imperfections d'encre de tampon
    random.seed(99)
    for _ in range(800):
        rx = random.randint(0, w - 1)
        ry = random.randint(0, h - 1)
        pix = seal.getpixel((rx, ry))
        if pix[3] > 40:
            reduction = random.randint(30, 150)
            seal.putpixel((rx, ry), (pix[0], pix[1], pix[2], max(0, pix[3] - reduction)))

    seal = seal.rotate(1.4, expand=False, resample=Image.BICUBIC)

    seal.save(output_path, "PNG")
    print(f"Tampon officiel ZAOU ajusté avec succès : {output_path}")

if __name__ == "__main__":
    generate_official_zaou_seal()
