# StegoodXP - Keamanan Data dan Informasi (KDI)

StegoodXP adalah aplikasi desktop berbasis Python untuk menyembunyikan pesan rahasia di dalam file gambar digital. Aplikasi ini dikembangkan sebagai proyek pembelajaran mata kuliah **Keamanan Data dan Informasi (KDI)**, yang mendemonstrasikan penerapan teknik steganografi **Least Significant Bit (LSB)** yang dikombinasikan dengan algoritma enkripsi tersandi **ROT13**.

Antarmuka pengguna (GUI) dikembangkan menggunakan library Tkinter dengan mengadopsi elemen desain antarmuka klasik dari era Windows 95/XP.

## Fitur Utama

- **Penyandian Pesan (Encode):** Membaca gambar berformat PNG/BMP dan menyisipkan teks rahasia ke dalam bit LSB dari piksel gambar. Pesan terlebih dahulu dienkripsi menggunakan ROT13 sebelum disisipkan.
- **Ekstraksi Pesan (Decode):** Mengekstrak data bit yang tersembunyi dari gambar stego dan merekonstruksinya menjadi teks asli melalui dekripsi ROT13.
- **Deteksi Kapasitas Otomatis:** Menghitung jumlah maksimum karakter yang dapat ditampung oleh gambar sebelum proses penyisipan dimulai.
- **Validasi Format Lossless:** Memaksa penggunaan format gambar tanpa kompresi (lossless) seperti PNG dan BMP untuk menghindari kerusakan data akibat kompresi lossy (seperti format JPG/JPEG).

## Alur Kerja

Proses penyisipan dan ekstraksi pesan beroperasi melalui alur berikut:

### Alur Enkripsi (Encode)
1. **Input:** Membaca pesan teks rahasia dan gambar sumber (berformat PNG atau BMP).
2. **Enkripsi:** Mengenkripsi teks pesan menggunakan cipher substitusi dasar ROT13.
3. **Pembatasan:** Menambahkan tanda delimiter khusus (`|||END|||`) di bagian belakang pesan terenkripsi sebagai penanda akhir pesan.
4. **Konversi Biner:** Mengubah setiap karakter dari pesan tersebut ke dalam wujud biner (8-bit).
5. **Penyisipan (Embedding):** Menyisipkan urutan bit pesan ke dalam Least Significant Bit (LSB) pada saluran warna Merah (R), Hijau (G), dan Biru (B) pada setiap piksel gambar.
6. **Output:** Menyimpan gambar stego yang telah dimodifikasi ke dalam format lossless (PNG) guna mencegah hilangnya data akibat kompresi.

### Alur Dekripsi (Decode)
1. **Input:** Membaca gambar stego (hasil proses encode) yang berisi pesan.
2. **Ekstraksi:** Mengambil Least Significant Bit (LSB) dari saluran R, G, B setiap piksel gambar.
3. **Rekonstruksi:** Mengumpulkan setiap 8 bit yang terekstrak secara berurutan dan merekonstruksinya menjadi karakter teks.
4. **Pendeteksian Batas:** Menghentikan proses ekstraksi secara otomatis ketika delimiter `|||END|||` ditemukan di dalam teks.
5. **Dekripsi:** Mendekripsi pesan hasil ekstraksi tersebut menggunakan ROT13.
6. **Output:** Menampilkan teks pesan rahasia orisinal ke antarmuka pengguna.

## Spesifikasi Teknis

- **Metode Steganografi:** Least Significant Bit (LSB) Substitution.
- **Kapasitas Pesan:** `((Lebar x Tinggi x 3) / 8) - Panjang Delimiter` (dalam karakter).
- **Format Input:** PNG, BMP.
- **Format Output:** PNG (wajib).
- **Enkripsi:** ROT13 (Caesar Cipher dengan pergeseran 13 karakter). *Catatan: ROT13 digunakan untuk tujuan obfuskasi dasar dan demonstrasi, bukan sebagai lapisan keamanan kriptografis tingkat tinggi.*

## Struktur Direktori

```text
stegood/
├── stegoxp.py           # Entry point aplikasi (Main Window)
├── steganography.py     # Modul inti pemrosesan LSB
├── crypto.py            # Modul enkripsi/dekripsi ROT13
├── requirements.txt     # Dependensi library
├── ui/
│   ├── theme.py         # Konfigurasi palet warna dan tipografi
│   └── widgets.py       # Komponen widget kustom Tkinter
└── assets/
    └── icon.ico         # Ikon aplikasi
```

## Prasyarat dan Instalasi

Pastikan sistem Anda telah terinstal **Python 3.8** atau yang lebih baru.

1. **Clone repository:**
   ```bash
   git clone https://github.com/dikapradnyanta/stegood.git
   cd stegood
   ```

2. **Instalasi dependensi:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Dependensi utama yang dibutuhkan adalah `Pillow` untuk pemrosesan gambar).*

3. **Menjalankan aplikasi:**
   ```bash
   python stegoxp.py
   ```

## Batasan Sistem

Penting untuk diperhatikan bahwa metode LSB sangat rentan terhadap kompresi lossy. Apabila gambar output diubah formatnya menjadi JPG/JPEG atau dikirim melalui platform yang mengompresi gambar (seperti WhatsApp), data LSB akan rusak dan pesan tidak dapat diekstrak kembali. Oleh karena itu, selalu simpan dan distribusikan gambar stego dalam format PNG.

---
*Proyek ini dikembangkan untuk education purpose.*
