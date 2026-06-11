"""
ui/theme.py — Konstanta warna, font, dan style untuk StegoodXP
Estetika: Windows 95/XP pixel-art retro
"""

# ─── Palette Warna ───────────────────────────────────────────────────────────
# Semua warna hardcoded. Tidak mengikuti dark/light mode sistem.

COLOR = {
    # Permukaan utama
    "bg":            "#C0C0C0",   # abu-abu silver — body window
    "bg_dark":       "#808080",   # abu-abu gelap — sunken panel
    "bg_light":      "#FFFFFF",   # putih — input field, text area

    # Title bar
    "titlebar_bg":   "#000080",   # biru navy klasik
    "titlebar_txt":  "#FFFFFF",   # putih

    # Border 3D (raised/sunken)
    "border_lt":     "#FFFFFF",   # tepi atas + kiri (highlight)
    "border_dk":     "#404040",   # tepi bawah + kanan (shadow)
    "border_mid":    "#808080",   # tepi tengah (untuk sunken)

    # Aksen
    "accent":        "#000080",   # biru navy — tombol primary, seleksi
    "accent_txt":    "#FFFFFF",   # teks di atas tombol primary

    # Teks
    "text":          "#000000",   # hitam — teks utama
    "text_dim":      "#404040",   # abu gelap — label sekunder
    "text_disabled": "#808080",   # abu — elemen disabled

    # Status
    "status_ok":     "#008000",   # hijau — berhasil
    "status_err":    "#FF0000",   # merah — error
    "status_info":   "#000080",   # biru — informasi / idle
}

# ─── Tipografi ────────────────────────────────────────────────────────────────
# Fixedsys: bitmap font Windows asli, tidak anti-aliased
# Courier: fallback monospace untuk input area

FONT_PIXEL = ("Fixedsys", 10)           # label umum
FONT_SMALL = ("Fixedsys", 8)            # status bar
FONT_TITLE = ("Fixedsys", 10, "bold")   # title bar, heading tab
FONT_INPUT = ("Courier", 9)             # textarea input/output

# ─── Dimensi Window ──────────────────────────────────────────────────────────
WINDOW_WIDTH  = 640
WINDOW_HEIGHT = 500   # sedikit lebih tinggi dari 480 untuk kenyamanan konten
TITLE_BAR_HEIGHT = 28

# ─── Preview Thumbnail ────────────────────────────────────────────────────────
PREVIEW_W = 160
PREVIEW_H = 120
