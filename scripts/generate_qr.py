import io
import base64
import qrcode
from qrcode.image.pil import PilImage

def generate_verification_qr_data_uri(student_id, sha256_hash):
    """
    Generates a dynamic QR code containing the official verification URL
    and returns a base64 Data URI for inline embedding in HTML templates.
    """
    verify_url = f"https://verify.zaou.ac.zm/transcript?student_id={student_id}&hash={sha256_hash}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=6,
        border=2,
    )
    qr.add_data(verify_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    b64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return f"data:image/png;base64,{b64_str}"

if __name__ == '__main__':
    data_uri = generate_verification_qr_data_uri("ZOU/2012/0482", "a1b2c3d4e5f67890")
    print("QR Code Data URI generated successfully (length:", len(data_uri), ")")
