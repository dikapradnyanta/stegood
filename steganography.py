"""
steganography.py — Modul LSB Steganografi untuk StegoodXP
Menyembunyikan dan mengekstrak pesan dari bit LSB pixel gambar.
"""

from PIL import Image
from crypto import rot13_encode, rot13_decode

# Delimiter penanda akhir pesan
DELIMITER = "|||END|||"


def get_capacity(image_path: str) -> int:
    """
    Hitung kapasitas maksimum pesan (dalam karakter) untuk gambar tertentu.
    Kapasitas = (lebar x tinggi x 3 channel) / 8 bit per karakter
    Dikurangi panjang delimiter.
    """
    img = Image.open(image_path)
    width, height = img.size
    max_bits = width * height * 3
    max_chars = max_bits // 8
    return max(0, max_chars - len(DELIMITER))


def get_image_info(image_path: str) -> dict:
    """Ambil info gambar: dimensi, format, dan kapasitas."""
    img = Image.open(image_path)
    width, height = img.size
    fmt = img.format if img.format else "PNG"
    capacity = get_capacity(image_path)
    return {
        "width": width,
        "height": height,
        "format": fmt,
        "capacity": capacity,
    }


def encode_message(image_path: str, message: str, output_path: str) -> None:
    """
    Sisipkan pesan ke dalam gambar menggunakan metode LSB.

    Alur:
    1. Enkripsi pesan dengan ROT13
    2. Tambahkan delimiter |||END||| di akhir
    3. Konversi ke bit string
    4. Sisipkan ke bit LSB setiap channel pixel (R, G, B)
    5. Simpan sebagai PNG

    Raises:
        ValueError: Jika pesan terlalu panjang untuk gambar
        ValueError: Jika format gambar tidak didukung (JPG/JPEG)
    """
    # Validasi format
    img = Image.open(image_path)
    if img.format in ("JPEG", "JPG"):
        raise ValueError(
            "Format JPG tidak didukung!\n"
            "JPG menggunakan kompresi lossy yang merusak bit LSB.\n"
            "Gunakan PNG atau BMP."
        )

    img = img.convert("RGB")
    width, height = img.size
    pixels = list(img.getdata())

    # Kapasitas maksimum dalam karakter
    max_chars = (width * height * 3) // 8 - len(DELIMITER)
    if len(message) > max_chars:
        raise ValueError(
            f"Pesan terlalu panjang!\n"
            f"Pesan: {len(message)} karakter\n"
            f"Kapasitas gambar: {max_chars} karakter\n"
            f"Pilih gambar yang lebih besar atau perpendek pesan."
        )

    # Enkripsi ROT13 lalu tambahkan delimiter
    encrypted = rot13_encode(message) + DELIMITER

    # Konversi ke bit string
    bit_string = ''.join(format(ord(c), '08b') for c in encrypted)
    total_bits = len(bit_string)

    # Validasi kapasitas bit
    if total_bits > width * height * 3:
        raise ValueError("Pesan tidak muat dalam gambar ini.")

    # Sisipkan bit ke pixel
    new_pixels = []
    bit_index = 0

    for pixel in pixels:
        r, g, b = pixel
        channels = [r, g, b]
        new_channels = []

        for ch in channels:
            if bit_index < total_bits:
                # Ganti bit LSB channel dengan bit pesan
                new_ch = (ch & 0xFE) | int(bit_string[bit_index])
                bit_index += 1
            else:
                new_ch = ch
            new_channels.append(new_ch)

        new_pixels.append(tuple(new_channels))

    # Buat gambar baru dengan pixel yang sudah dimodifikasi
    new_img = Image.new("RGB", (width, height))
    new_img.putdata(new_pixels)
    new_img.save(output_path, "PNG")


def decode_message(image_path: str) -> str:
    """
    Ekstrak dan dekripsi pesan tersembunyi dari gambar.

    Alur:
    1. Ekstrak bit LSB dari setiap channel pixel (R, G, B)
    2. Kelompokkan 8 bit menjadi 1 karakter
    3. Cari delimiter |||END|||
    4. Dekripsi ROT13

    Raises:
        ValueError: Jika tidak ditemukan pesan tersembunyi (tidak ada delimiter)
    """
    img = Image.open(image_path).convert("RGB")
    pixels = list(img.getdata())

    # Ekstrak semua bit LSB
    bits = []
    for pixel in pixels:
        for channel in pixel:
            bits.append(channel & 1)

    # Rekonstruksi karakter dari setiap 8 bit
    extracted_text = ""
    for i in range(0, len(bits) - 7, 8):
        byte = bits[i:i + 8]
        char_code = int(''.join(str(b) for b in byte), 2)
        # Batasi ke karakter ASCII yang valid (bukan null byte)
        if char_code == 0:
            break
        extracted_text += chr(char_code)

        # Cek delimiter secara bertahap (optimasi: berhenti saat ditemukan)
        if extracted_text.endswith(DELIMITER):
            break

    # Cari delimiter
    if DELIMITER not in extracted_text:
        raise ValueError(
            "Tidak ditemukan pesan tersembunyi dalam gambar ini.\n"
            "Pastikan gambar sudah diproses oleh StegoodXP."
        )

    # Ekstrak pesan sebelum delimiter
    encrypted_message = extracted_text[:extracted_text.index(DELIMITER)]

    # Dekripsi ROT13
    return rot13_decode(encrypted_message)
