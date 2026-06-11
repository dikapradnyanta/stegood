"""
generate_icon.py — Script bantu untuk convert PNG ke ICO
Jalankan sekali untuk membuat assets/icon.ico dari stegoxp_icon.png

Usage:
  python generate_icon.py
"""
from PIL import Image
from pathlib import Path

# Path ke file PNG yang diunduh/dibuat
# Ganti dengan path PNG pixel-art icon 32x32
SRC_PNG = Path(__file__).parent.parent / "stegoxp_icon.png"
DST_ICO = Path(__file__).parent / "icon.ico"

def convert():
    if not SRC_PNG.exists():
        print(f"ERROR: File tidak ditemukan: {SRC_PNG}")
        print("Letakkan file PNG icon 32x32 di:", SRC_PNG)
        return

    img = Image.open(SRC_PNG).convert("RGBA")
    img = img.resize((32, 32), Image.NEAREST)
    img.save(DST_ICO, format="ICO", sizes=[(32, 32), (16, 16)])
    print(f"Icon berhasil dibuat: {DST_ICO}")

if __name__ == "__main__":
    convert()
