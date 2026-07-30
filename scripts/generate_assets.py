import os
from PIL import Image, ImageDraw, ImageFont

def generate_seal():
    # Generate authentic University Seal stamp (purple/violet stamp)
    size = (400, 400)
    seal = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(seal)
    
    purple = (75, 40, 130, 220) # Institutional purple/violet ink stamp
    
    # Outer circle
    draw.ellipse([20, 20, 380, 380], outline=purple, width=6)
    draw.ellipse([30, 30, 370, 370], outline=purple, width=2)
    
    # Inner box for date
    draw.rectangle([80, 150, 320, 250], outline=purple, width=3)
    
    # Text in stamp
    try:
        font_large = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)
        font_med = ImageFont.truetype("DejaVuSans-Bold.ttf", 16)
        font_small = ImageFont.truetype("DejaVuSans.ttf", 13)
    except:
        font_large = font_med = font_small = ImageFont.load_default()
        
    draw.text((200, 50), "ZAMBIAN OPEN UNIVERSITY", fill=purple, font=font_small, anchor="mm")
    draw.text((200, 75), "ACADEMIC AFFAIRS", fill=purple, font=font_med, anchor="mm")
    
    draw.text((200, 185), "OFFICIAL SEAL", fill=purple, font=font_large, anchor="mm")
    draw.text((200, 220), "SENATE SECRETARIAT", fill=purple, font=font_small, anchor="mm")
    
    draw.text((200, 290), "DESPATCHED EXAMINATIONS", fill=purple, font=font_small, anchor="mm")
    draw.text((200, 320), "P.O. BOX LUSAKA - ZAMBIA", fill=purple, font=font_small, anchor="mm")
    
    seal.save('assets/university_seal.png')
    print("Generated assets/university_seal.png")

def generate_signature():
    # Generate realistic Registrar signature
    size = (300, 100)
    sig = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(sig)
    
    dark_blue = (15, 30, 90, 240)
    # Draw cursive-like signature strokes
    points = [
        (30, 60), (45, 25), (60, 75), (80, 40), (95, 65),
        (110, 50), (130, 55), (150, 30), (170, 70), (190, 45),
        (210, 60), (240, 50), (270, 55)
    ]
    draw.line(points, fill=dark_blue, width=3, joint="curve")
    
    # Underline swirl
    swirl = [(25, 75), (80, 85), (180, 80), (275, 70)]
    draw.line(swirl, fill=dark_blue, width=2, joint="curve")
    
    sig.save('assets/registrar_signature.png')
    print("Generated assets/registrar_signature.png")

if __name__ == '__main__':
    os.makedirs('assets', exist_ok=True)
    generate_seal()
    generate_signature()
