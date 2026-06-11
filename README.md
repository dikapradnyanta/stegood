# 🔒 StegoodXP v1.0

> Aplikasi steganografi desktop bergaya **Windows 95/XP retro pixel-art** — sembunyikan pesan rahasia di dalam gambar menggunakan metode **LSB (Least Significant Bit)** dikombinasikan dengan enkripsi **ROT13**.

---

## 📸 Tampilan Aplikasi

Antarmuka StegoodXP sengaja didesain menyerupai aplikasi era Windows 95/XP:
- Title bar navy `#000080` dengan tombol `[_] [X]`
- Border 3D raised/sunken tanpa border-radius
- Font bitmap `Fixedsys` yang tidak anti-aliased
- Palette warna solid, kontras tinggi

---

## ✨ Fitur

### Tab Encode (Sembunyikan Pesan)
- Browse file gambar sumber (PNG / BMP)
- Preview thumbnail gambar (resize NEAREST, pixel-art style)
- Info otomatis: dimensi, format, kapasitas maksimum karakter
- Counter karakter real-time saat mengetik pesan
- Proses: pesan → ROT13 → LSB embed → simpan PNG (dialog Save As)
- Tombol **RESET** untuk membersihkan semua input

### Tab Decode (Baca Pesan)
- Browse file gambar yang sudah di-encode
- Ekstrak bit LSB → dekripsi ROT13 otomatis
- Tampilkan pesan asli di area teks (read-only)
- Tombol **RESET**

### Status Bar (3 Panel)
| Panel | Konten |
|---|---|
| Kiri | Status teks (🔵 info / 🟢 berhasil / 🔴 error) |
| Tengah | Dimensi & format gambar |
| Kanan | Kapasitas pesan (karakter) |

---

## 🏗️ Struktur Proyek

```
stegood/
│
├── stegoxp.py           ← Entry point & Main Window
├── steganography.py     ← Logika LSB encode / decode
├── crypto.py            ← Enkripsi / dekripsi ROT13
├── requirements.txt     ← Dependensi Python
│
├── ui/
│   ├── __init__.py
│   ├── theme.py         ← Konstanta warna, font, dimensi
│   └── widgets.py       ← Widget kustom bergaya Win95
│
└── assets/
    ├── icon.ico         ← Ikon pixel-art padlock 32×32
    └── generate_icon.py ← Helper convert PNG → ICO
```

---

## 🚀 Cara Menjalankan

### 1. Prasyarat
- Python 3.8 atau lebih baru
- Tkinter (sudah built-in di Python)

### 2. Install dependensi
```bash
pip install -r requirements.txt
```

atau langsung:
```bash
pip install Pillow
```

### 3. Jalankan aplikasi
```bash
python stegoxp.py
```

---

## 🔧 Cara Pakai

### Encode (Sembunyikan Pesan)
1. Buka aplikasi → pastikan tab **Encode** aktif
2. Klik **Browse...** → pilih file PNG atau BMP
3. Periksa info kapasitas di panel kanan dan di samping preview
4. Tulis pesan rahasia di area teks
5. Klik **ENCODE** → pilih lokasi & nama file output
6. File PNG hasil tersimpan dengan pesan tersembunyi

### Decode (Baca Pesan)
1. Buka tab **Decode**
2. Klik **Browse...** → pilih file PNG hasil encode
3. Klik **DECODE**
4. Pesan asli ditampilkan di area teks

---

## ⚙️ Cara Kerja Teknis

### Alur Encode
```
Input pesan
  ↓
ROT13 encrypt
  ↓
Tambah delimiter "|||END|||"
  ↓
Konversi setiap karakter → 8 bit binary
  ↓
Sisipkan ke bit LSB channel R, G, B setiap pixel
  ↓
Simpan sebagai PNG (lossless)
```

### Alur Decode
```
Buka gambar PNG
  ↓
Ekstrak bit LSB dari channel R, G, B setiap pixel
  ↓
Rekonstruksi karakter (setiap 8 bit = 1 karakter)
  ↓
Cari delimiter "|||END|||"
  ↓
ROT13 decrypt
  ↓
Tampilkan pesan asli
```

### Kapasitas Pesan
```
Kapasitas (karakter) = (lebar × tinggi × 3) ÷ 8 − len("|||END|||")
```
Contoh: gambar 320×240 px → kapasitas ≈ 2.880 karakter

---

## 🎨 Design System

### Palette Warna

| Nama | Kode Hex | Penggunaan |
|---|---|---|
| `bg` | `#C0C0C0` | Background utama window |
| `bg_dark` | `#808080` | Sunken panel, tab non-aktif |
| `bg_light` | `#FFFFFF` | Input field, text area |
| `titlebar_bg` | `#000080` | Title bar (navy klasik) |
| `titlebar_txt` | `#FFFFFF` | Teks di title bar |
| `border_lt` | `#FFFFFF` | Tepi atas + kiri (highlight 3D) |
| `border_dk` | `#404040` | Tepi bawah + kanan (shadow 3D) |
| `border_mid` | `#808080` | Tepi tengah (sunken) |
| `accent` | `#000080` | Tombol primary, seleksi |
| `accent_txt` | `#FFFFFF` | Teks di atas tombol primary |
| `text` | `#000000` | Teks utama |
| `text_dim` | `#404040` | Label sekunder |
| `text_disabled` | `#808080` | Elemen disabled |
| `status_ok` | `#008000` | Status berhasil (hijau) |
| `status_err` | `#FF0000` | Status error (merah) |
| `status_info` | `#000080` | Status idle / info (navy) |

### Tipografi

| Peran | Font | Ukuran |
|---|---|---|
| Label umum | Fixedsys | 10 |
| Status bar | Fixedsys | 8 |
| Title bar / tab heading | Fixedsys bold | 10 |
| Input / textarea | Courier | 9 |

> **Mengapa Fixedsys?**
> Fixedsys adalah bitmap font asli Windows yang tidak di-antialiased — memberikan tampilan pixel-art yang autentik tanpa blur.

### Prinsip Desain

| Prinsip | Detail |
|---|---|
| **Pixel-first** | Semua elemen menggunakan pixel font, tidak ada border-radius |
| **3D flat illusion** | Border raised/sunken: terang di atas-kiri, gelap di bawah-kanan |
| **Teks sebagai ornamen** | Tidak ada ikon dekoratif, emoji, atau ilustrasi |
| **Warna solid** | Palette flat kontras tinggi, bukan pastel atau gradient |
| **No animation** | Komputer jadul tidak kenal transisi — semua instan |
| **Fixed size** | 640×500 px, `resizable(False)` — presisi tata letak pixel |

### Dilarang (by Design)

| Dilarang | Alasan |
|---|---|
| border-radius | Merusak estetika pixel-art |
| Gradient warna | Terlalu modern |
| Drop shadow / glow | Tidak ada di Win95 asli |
| Emoji / ikon SVG | Tidak cocok dengan pixel font |
| `ttk` themed widgets | Tampilannya terlalu flat/modern |
| Font sans-serif halus | Anti-aliased, merusak vibe retro |
| Window resizable | Pixel layout harus presisi |
| Animasi / transisi | Tidak ada di era komputer jadul |

---

## 🧩 Komponen UI (`ui/widgets.py`)

### `PixelButton`
Tombol bergaya Win95 dengan dua variant:

```
Normal:   [ Browse...  ]   ← bg #C0C0C0, hover #D0D0D0, relief raised
Primary:  [ ENCODE     ]   ← bg #000080, fg white, hover #0000A0
```

### `PixelFrame`
`LabelFrame` bergaya Win95 sebagai "Group Box":
- Relief `groove`, border 2px
- Label di-uppercase otomatis
- Font Fixedsys

### `StatusBar`
Tiga `Label` panel terpisah di bagian bawah window:
```
┌─────────────────┬──────────────────┬──────────────────────┐
│ Siap            │ 320x240 | PNG    │ Kapasitas: 2880 char │
└─────────────────┴──────────────────┴──────────────────────┘
```

### `ImagePreview`
Label hitam (`#000000`) sunken — menampilkan thumbnail gambar yang di-resize menggunakan `Image.NEAREST` (menjaga estetika pixel-art, bukan blur seperti LANCZOS).

### `TabStrip`
Custom tab — **bukan** `ttk.Notebook`:
```
[ Encode ] [ Decode ]
────────────
```
- Tab aktif: `relief="ridge"`, bg silver
- Tab non-aktif: `relief="raised"`, bg `#808080`

---

## 📋 Batasan Teknis

| Batasan | Keterangan |
|---|---|
| Format input | PNG, BMP (JPG ditolak — kompresi lossy merusak LSB) |
| Format output | Selalu PNG |
| Enkripsi | ROT13 (bukan enkripsi kriptografis kuat) |
| Platform | Windows, Linux, macOS (Python 3.8+) |
| Ukuran window | Fixed 640×500 px |

---

## 📦 Dependensi

| Package | Versi | Fungsi |
|---|---|---|
| `Pillow` | ≥ 9.0.0 | Baca, tulis, manipulasi gambar |
| `tkinter` | built-in | GUI framework |
| `codecs` | built-in | ROT13 via `codecs.encode(text, 'rot_13')` |

---

## ⚠️ Catatan Penting

- **ROT13 bukan enkripsi yang kuat** — hanya digunakan sebagai lapisan obfuskasi sederhana untuk tujuan edukasi
- **Selalu gunakan PNG sebagai output** — format lossless wajib agar bit LSB tidak rusak
- **Jangan konversi hasil ke JPG** — akan merusak data yang tersembunyi
- **Kapasitas terbatas** — pesan sangat panjang membutuhkan gambar yang besar

---

## 👤 Target Pengguna

Mahasiswa, penggemar keamanan informasi, dan siapa saja yang ingin bereksperimen dengan konsep **steganografi digital** secara visual dan interaktif.

---

## 📚 Referensi

- [LSB Steganography](https://en.wikipedia.org/wiki/Steganography#Digital) — Wikipedia
- [ROT13](https://en.wikipedia.org/wiki/ROT13) — Wikipedia
- [Windows 95 UI Guidelines](https://web.archive.org/web/19980709154836/http://www.microsoft.com/win32dev/uiguide/) — Microsoft (1995)
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [Press Start 2P Font](https://fonts.google.com/specimen/Press+Start+2P) — Google Fonts (referensi visual)

---

*StegoodXP — Proyek edukasi steganografi. Bukan untuk produksi.*
