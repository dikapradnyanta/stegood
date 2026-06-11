"""
stegoxp.py — StegoodXP v1.0
Aplikasi steganografi LSB + enkripsi ROT13 dengan estetika retro Windows 95/XP.

Entry point & Main Window.

Dependensi:
  pip install Pillow

Jalankan:
  python stegoxp.py
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

from PIL import Image, ImageTk

from ui.theme import (
    COLOR, FONT_PIXEL, FONT_SMALL, FONT_TITLE, FONT_INPUT,
    WINDOW_WIDTH, WINDOW_HEIGHT, TITLE_BAR_HEIGHT,
    PREVIEW_W, PREVIEW_H,
)
from ui.widgets import PixelButton, PixelFrame, StatusBar, ImagePreview, TabStrip
import steganography


# ─── Konstanta ────────────────────────────────────────────────────────────────
APP_TITLE   = "StegoodXP v1.0"
APP_VERSION = "1.0"
SUPPORTED_OPEN  = [("Image Files", "*.png *.bmp"), ("PNG Files", "*.png"), ("BMP Files", "*.bmp")]
SUPPORTED_SAVE  = [("PNG Files", "*.png")]


# ═══════════════════════════════════════════════════════════════════════════════
class TitleBar(tk.Frame):
    """
    Custom title bar bergaya Windows 95.
    Warna: navy #000080. Tombol: [_] [□] [X].
    Mendukung drag window (karena overrideredirect=True di MainWindow).
    """

    def __init__(self, parent, title: str, on_minimize, on_close, **kwargs):
        kwargs.setdefault("bg", COLOR["titlebar_bg"])
        kwargs.setdefault("height", TITLE_BAR_HEIGHT)
        super().__init__(parent, **kwargs)
        self.pack_propagate(False)

        # ── Ikon kecil pixel ──
        lbl_icon = tk.Label(
            self, text="[=]",
            font=FONT_SMALL,
            bg=COLOR["titlebar_bg"],
            fg=COLOR["titlebar_txt"],
        )
        lbl_icon.pack(side="left", padx=4)

        # ── Judul ──
        lbl_title = tk.Label(
            self, text=title,
            font=FONT_TITLE,
            bg=COLOR["titlebar_bg"],
            fg=COLOR["titlebar_txt"],
        )
        lbl_title.pack(side="left", padx=2)

        # ── Tombol window kanan ──
        btn_frame = tk.Frame(self, bg=COLOR["titlebar_bg"])
        btn_frame.pack(side="right", padx=2)

        for symbol, cmd in [("_", on_minimize), ("X", on_close)]:
            b = tk.Button(
                btn_frame, text=symbol,
                font=FONT_SMALL,
                bg=COLOR["bg"],
                fg=COLOR["text"],
                activebackground="#A0A0A0",
                relief="raised", bd=2,
                width=2,
                cursor="arrow",
                command=cmd,
            )
            b.pack(side="left", padx=1, pady=3)

        # ── Drag window ──
        self._drag_x = 0
        self._drag_y = 0
        for widget in (self, lbl_icon, lbl_title):
            widget.bind("<ButtonPress-1>",   self._drag_start)
            widget.bind("<B1-Motion>",       self._drag_move)

    def _drag_start(self, event):
        self._drag_x = event.x_root - self.winfo_toplevel().winfo_x()
        self._drag_y = event.y_root - self.winfo_toplevel().winfo_y()

    def _drag_move(self, event):
        root = self.winfo_toplevel()
        x = event.x_root - self._drag_x
        y = event.y_root - self._drag_y
        root.geometry(f"+{x}+{y}")



# ═══════════════════════════════════════════════════════════════════════════════
class EncodeTab(tk.Frame):
    """Tab Encode: pilih gambar → tulis pesan → ROT13+LSB → simpan PNG."""

    def __init__(self, parent, status_bar: StatusBar, **kwargs):
        kwargs.setdefault("bg", COLOR["bg"])
        super().__init__(parent, **kwargs)
        self._status = status_bar
        self._image_path = ""
        self._build_ui()

    def _build_ui(self):
        pad = {"padx": 8, "pady": 4}

        # ── Group: Pilih Gambar ──────────────────────────────────────────────
        grp_image = PixelFrame(self, text="Pilih Gambar")
        grp_image.pack(fill="x", **pad)

        # Baris path + browse
        row_path = tk.Frame(grp_image, bg=COLOR["bg"])
        row_path.pack(fill="x", padx=6, pady=(6, 4))

        tk.Label(row_path, text="Path:", font=FONT_PIXEL,
                 bg=COLOR["bg"], fg=COLOR["text"]).pack(side="left")

        self._path_var = tk.StringVar()
        self._entry_path = tk.Entry(
            row_path,
            textvariable=self._path_var,
            bg=COLOR["bg_light"],
            fg=COLOR["text"],
            insertbackground=COLOR["text"],
            relief="sunken", bd=2,
            font=FONT_INPUT,
            state="readonly",
        )
        self._entry_path.pack(side="left", fill="x", expand=True, padx=4)

        PixelButton(row_path, text="Browse...",
                    command=self._browse_image).pack(side="left")

        # Baris preview + info
        row_preview = tk.Frame(grp_image, bg=COLOR["bg"])
        row_preview.pack(fill="x", padx=6, pady=(0, 6))

        self._preview = ImagePreview(row_preview, width=PREVIEW_W, height=PREVIEW_H)
        self._preview.pack(side="left")

        # Info panel di samping preview
        info_frame = tk.Frame(row_preview, bg=COLOR["bg"])
        info_frame.pack(side="left", padx=10, anchor="nw")

        self._lbl_dim      = tk.Label(info_frame, text="", font=FONT_SMALL,
                                      bg=COLOR["bg"], fg=COLOR["text_dim"], anchor="w")
        self._lbl_fmt      = tk.Label(info_frame, text="", font=FONT_SMALL,
                                      bg=COLOR["bg"], fg=COLOR["text_dim"], anchor="w")
        self._lbl_capacity = tk.Label(info_frame, text="", font=FONT_SMALL,
                                      bg=COLOR["bg"], fg=COLOR["text_dim"], anchor="w")

        for lbl in (self._lbl_dim, self._lbl_fmt, self._lbl_capacity):
            lbl.pack(anchor="w", pady=2)

        # ── Group: Pesan Rahasia ─────────────────────────────────────────────
        grp_msg = PixelFrame(self, text="Pesan Rahasia (ROT13)")
        grp_msg.pack(fill="both", expand=True, **pad)

        self._text_msg = tk.Text(
            grp_msg,
            bg=COLOR["bg_light"],
            fg=COLOR["text"],
            insertbackground=COLOR["text"],
            relief="sunken", bd=2,
            font=FONT_INPUT,
            wrap="word",
            height=6,
        )
        self._text_msg.pack(fill="both", expand=True, padx=6, pady=6)

        # Counter karakter
        self._lbl_charcount = tk.Label(
            grp_msg, text="0 karakter",
            font=FONT_SMALL, bg=COLOR["bg"], fg=COLOR["text_dim"],
        )
        self._lbl_charcount.pack(anchor="e", padx=6, pady=(0, 4))
        self._text_msg.bind("<KeyRelease>", self._update_charcount)

        # ── Tombol aksi ──────────────────────────────────────────────────────
        btn_row = tk.Frame(self, bg=COLOR["bg"])
        btn_row.pack(fill="x", padx=8, pady=(2, 8))

        PixelButton(btn_row, text="RESET",
                    command=self._reset).pack(side="right", padx=(4, 0))
        PixelButton(btn_row, variant="primary", text="ENCODE",
                    command=self._encode).pack(side="right")

    # ── Aksi ──────────────────────────────────────────────────────────────────

    def _browse_image(self):
        path = filedialog.askopenfilename(
            title="Pilih Gambar Sumber",
            filetypes=SUPPORTED_OPEN,
        )
        if not path:
            return

        # Validasi format JPG
        p = Path(path)
        if p.suffix.lower() in (".jpg", ".jpeg"):
            messagebox.showerror(
                "Format Tidak Didukung",
                "Format JPG tidak didukung!\n\n"
                "JPG menggunakan kompresi lossy yang merusak bit LSB.\n"
                "Gunakan PNG atau BMP.",
            )
            return

        self._image_path = path
        self._path_var.set(path)
        self._load_preview(path)

    def _load_preview(self, path: str):
        try:
            info = steganography.get_image_info(path)
            img  = Image.open(path)

            self._preview.set_image(img)
            self._lbl_dim.config(text=f"Ukuran : {info['width']} x {info['height']} px")
            self._lbl_fmt.config(text=f"Format : {info['format']}")
            self._lbl_capacity.config(text=f"Kapasitas: {info['capacity']} char")

            self._status.set_image_info(info["width"], info["height"], info["format"])
            self._status.set_capacity(info["capacity"])
            self._status.set_status("Gambar dimuat.", "info")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuka gambar:\n{e}")
            self._reset()

    def _update_charcount(self, event=None):
        count = len(self._text_msg.get("1.0", "end-1c"))
        self._lbl_charcount.config(text=f"{count} karakter")

    def _encode(self):
        if not self._image_path:
            messagebox.showwarning("Peringatan", "Pilih gambar terlebih dahulu!")
            return

        message = self._text_msg.get("1.0", "end-1c").strip()
        if not message:
            messagebox.showwarning("Peringatan", "Tulis pesan rahasia terlebih dahulu!")
            return

        # Dialog simpan file
        out_path = filedialog.asksaveasfilename(
            title="Simpan Gambar Hasil Encode",
            defaultextension=".png",
            filetypes=SUPPORTED_SAVE,
            initialfile=Path(self._image_path).stem + "_stego.png",
        )
        if not out_path:
            return

        try:
            self._status.set_status("Sedang memproses...", "info")
            self.update()

            steganography.encode_message(self._image_path, message, out_path)

            self._status.set_status(
                f"Berhasil disimpan: {Path(out_path).name}", "ok"
            )
            messagebox.showinfo(
                "Encode Berhasil",
                f"Pesan berhasil disembunyikan!\n\n"
                f"File tersimpan:\n{out_path}",
            )
        except ValueError as e:
            self._status.set_status("Encode gagal.", "err")
            messagebox.showerror("Encode Gagal", str(e))
        except Exception as e:
            self._status.set_status("Error tidak terduga.", "err")
            messagebox.showerror("Error", f"Terjadi error:\n{e}")

    def _reset(self):
        self._image_path = ""
        self._path_var.set("")
        self._preview.clear()
        self._text_msg.delete("1.0", "end")
        self._lbl_dim.config(text="")
        self._lbl_fmt.config(text="")
        self._lbl_capacity.config(text="")
        self._lbl_charcount.config(text="0 karakter")
        self._status.set_status("Siap", "info")
        self._status.clear_image_info()


# ═══════════════════════════════════════════════════════════════════════════════
class DecodeTab(tk.Frame):
    """Tab Decode: pilih gambar stego → ekstrak LSB → dekripsi ROT13 → tampilkan."""

    def __init__(self, parent, status_bar: StatusBar, **kwargs):
        kwargs.setdefault("bg", COLOR["bg"])
        super().__init__(parent, **kwargs)
        self._status = status_bar
        self._image_path = ""
        self._build_ui()

    def _build_ui(self):
        pad = {"padx": 8, "pady": 4}

        # ── Group: Pilih Gambar ──────────────────────────────────────────────
        grp_image = PixelFrame(self, text="Pilih Gambar Stego")
        grp_image.pack(fill="x", **pad)

        row_path = tk.Frame(grp_image, bg=COLOR["bg"])
        row_path.pack(fill="x", padx=6, pady=(6, 4))

        tk.Label(row_path, text="Path:", font=FONT_PIXEL,
                 bg=COLOR["bg"], fg=COLOR["text"]).pack(side="left")

        self._path_var = tk.StringVar()
        self._entry_path = tk.Entry(
            row_path,
            textvariable=self._path_var,
            bg=COLOR["bg_light"],
            fg=COLOR["text"],
            insertbackground=COLOR["text"],
            relief="sunken", bd=2,
            font=FONT_INPUT,
            state="readonly",
        )
        self._entry_path.pack(side="left", fill="x", expand=True, padx=4)

        PixelButton(row_path, text="Browse...",
                    command=self._browse_image).pack(side="left")

        # Preview + info
        row_preview = tk.Frame(grp_image, bg=COLOR["bg"])
        row_preview.pack(fill="x", padx=6, pady=(0, 6))

        self._preview = ImagePreview(row_preview, width=PREVIEW_W, height=PREVIEW_H)
        self._preview.pack(side="left")

        info_frame = tk.Frame(row_preview, bg=COLOR["bg"])
        info_frame.pack(side="left", padx=10, anchor="nw")

        self._lbl_dim      = tk.Label(info_frame, text="", font=FONT_SMALL,
                                      bg=COLOR["bg"], fg=COLOR["text_dim"], anchor="w")
        self._lbl_fmt      = tk.Label(info_frame, text="", font=FONT_SMALL,
                                      bg=COLOR["bg"], fg=COLOR["text_dim"], anchor="w")
        self._lbl_capacity = tk.Label(info_frame, text="", font=FONT_SMALL,
                                      bg=COLOR["bg"], fg=COLOR["text_dim"], anchor="w")

        for lbl in (self._lbl_dim, self._lbl_fmt, self._lbl_capacity):
            lbl.pack(anchor="w", pady=2)

        # ── Group: Pesan Tersembunyi ─────────────────────────────────────────
        grp_result = PixelFrame(self, text="Pesan Tersembunyi")
        grp_result.pack(fill="both", expand=True, **pad)

        self._text_result = tk.Text(
            grp_result,
            bg=COLOR["bg_light"],
            fg=COLOR["text"],
            insertbackground=COLOR["text"],
            relief="sunken", bd=2,
            font=FONT_INPUT,
            wrap="word",
            height=6,
            state="disabled",
        )
        self._text_result.pack(fill="both", expand=True, padx=6, pady=6)

        # ── Tombol aksi ──────────────────────────────────────────────────────
        btn_row = tk.Frame(self, bg=COLOR["bg"])
        btn_row.pack(fill="x", padx=8, pady=(2, 8))

        PixelButton(btn_row, text="RESET",
                    command=self._reset).pack(side="right", padx=(4, 0))
        PixelButton(btn_row, variant="primary", text="DECODE",
                    command=self._decode).pack(side="right")

    # ── Aksi ──────────────────────────────────────────────────────────────────

    def _browse_image(self):
        path = filedialog.askopenfilename(
            title="Pilih Gambar Stego",
            filetypes=SUPPORTED_OPEN,
        )
        if not path:
            return

        self._image_path = path
        self._path_var.set(path)
        self._load_preview(path)

    def _load_preview(self, path: str):
        try:
            info = steganography.get_image_info(path)
            img  = Image.open(path)

            self._preview.set_image(img)
            self._lbl_dim.config(text=f"Ukuran : {info['width']} x {info['height']} px")
            self._lbl_fmt.config(text=f"Format : {info['format']}")
            self._lbl_capacity.config(text=f"Kapasitas: {info['capacity']} char")

            self._status.set_image_info(info["width"], info["height"], info["format"])
            self._status.set_capacity(info["capacity"])
            self._status.set_status("Gambar dimuat. Klik DECODE.", "info")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuka gambar:\n{e}")
            self._reset()

    def _decode(self):
        if not self._image_path:
            messagebox.showwarning("Peringatan", "Pilih gambar terlebih dahulu!")
            return

        try:
            self._status.set_status("Sedang mendekode...", "info")
            self.update()

            message = steganography.decode_message(self._image_path)

            # Tampilkan hasil
            self._text_result.config(state="normal")
            self._text_result.delete("1.0", "end")
            self._text_result.insert("1.0", message)
            self._text_result.config(state="disabled")

            self._status.set_status(
                f"Berhasil! Pesan ditemukan ({len(message)} karakter).", "ok"
            )
        except ValueError as e:
            self._status.set_status("Decode gagal.", "err")
            messagebox.showerror("Decode Gagal", str(e))
        except Exception as e:
            self._status.set_status("Error tidak terduga.", "err")
            messagebox.showerror("Error", f"Terjadi error:\n{e}")

    def _reset(self):
        self._image_path = ""
        self._path_var.set("")
        self._preview.clear()
        self._text_result.config(state="normal")
        self._text_result.delete("1.0", "end")
        self._text_result.config(state="disabled")
        self._lbl_dim.config(text="")
        self._lbl_fmt.config(text="")
        self._lbl_capacity.config(text="")
        self._status.set_status("Siap", "info")
        self._status.clear_image_info()


# ═══════════════════════════════════════════════════════════════════════════════
class MainWindow:
    """
    Window utama StegoodXP.
    Menggunakan overrideredirect(True) untuk custom title bar Win95.
    """

    def __init__(self):
        self.root = tk.Tk()
        self._setup_window()
        self._build_ui()

    def _setup_window(self):
        root = self.root
        root.overrideredirect(True)   # Hilangkan title bar OS native

        # Ukuran & posisi tengah layar
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        x  = (sw - WINDOW_WIDTH)  // 2
        y  = (sh - WINDOW_HEIGHT) // 2
        root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
        root.resizable(False, False)
        root.configure(bg=COLOR["bg"])

        # Ikon (jika ada)
        icon_path = Path(__file__).parent / "assets" / "icon.ico"
        if icon_path.exists():
            try:
                root.iconbitmap(str(icon_path))
            except Exception:
                pass

        # Border window luar (ridge/raised)
        root.configure(highlightbackground=COLOR["border_dk"],
                       highlightthickness=2)

    def _build_ui(self):
        root = self.root

        # ── Title Bar ────────────────────────────────────────────────────────
        self._title_bar = TitleBar(
            root,
            title=APP_TITLE,
            on_minimize=self._minimize,
            on_close=root.destroy,
        )
        self._title_bar.pack(fill="x", side="top")

        # ── Status Bar (bawah) ───────────────────────────────────────────────
        self._status_bar = StatusBar(root)
        self._status_bar.pack(fill="x", side="bottom")

        # ── Body ─────────────────────────────────────────────────────────────
        body = tk.Frame(root, bg=COLOR["bg"], padx=0, pady=0)
        body.pack(fill="both", expand=True)

        # Tab Strip
        self._tabs = TabStrip(body)
        self._tabs.pack(fill="both", expand=True, padx=6, pady=6)

        # Buat tab Encode dan Decode sebagai anak langsung dari _container
        # (HARUS dibuat sebelum add_tab dipanggil)
        self._encode_tab = EncodeTab(
            self._tabs._container,
            status_bar=self._status_bar,
        )
        self._decode_tab = DecodeTab(
            self._tabs._container,
            status_bar=self._status_bar,
        )

        # Daftarkan tab — add_tab akan otomatis tampilkan tab pertama
        self._tabs.add_tab("encode", "Encode", self._encode_tab)
        self._tabs.add_tab("decode", "Decode", self._decode_tab)

        # Status awal
        self._status_bar.set_status("Siap", "info")

    def _minimize(self):
        """Minimize window (perlu overrideredirect trick)."""
        self.root.overrideredirect(False)
        self.root.iconify()

        def restore(event=None):
            self.root.deiconify()
            self.root.overrideredirect(True)
            # Re-focus agar interaktif kembali
            self.root.after(10, lambda: self.root.focus_force())

        self.root.bind("<Map>", restore)

    def run(self):
        self.root.mainloop()


# ─── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = MainWindow()
    app.run()
