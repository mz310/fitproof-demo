"""
QR код үүсгэх модуль
Төхөөрөмж бүрт өвөрмөц QR код үүсгэнэ
"""

import base64
from io import BytesIO

import qrcode


def generate_qr_code(data: str, size: int = 200) -> str:
    """
    QR код үүсгэж base64 форматаар буцаана

    Args:
        data: QR код дотор хадгалах өгөгдөл
        size: QR кодын хэмжээ (пиксел)

    Returns:
        Base64 кодлогдсон PNG зураг
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Resize if needed
    if size != 200:
        img = img.resize((size, size))

    # Convert to base64
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    return f"data:image/png;base64,{img_str}"


def generate_equipment_qr(equipment_id: int, equipment_name: str) -> str:
    """
    Төхөөрөмжийн QR код үүсгэх

    Args:
        equipment_id: Төхөөрөмжийн ID
        equipment_name: Төхөөрөмжийн нэр

    Returns:
        QR кодын утга (string)
    """
    # Format: EQ{id:03d}-{name_slug}
    name_slug = equipment_name.upper().replace(" ", "-")[:20]
    return f"EQ{equipment_id:03d}-{name_slug}"


if __name__ == "__main__":
    # Туршилт
    qr_code = generate_equipment_qr(1, "Treadmill 1")
    print(f"Generated QR code: {qr_code}")

    img_data = generate_qr_code(qr_code)
    print(f"Image data length: {len(img_data)}")
