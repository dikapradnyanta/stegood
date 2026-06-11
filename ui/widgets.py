"""
ui/widgets.py — Widget kustom bergaya Windows 95/XP untuk StegoodXP
Komponen: PixelButton, PixelFrame, StatusBar, ImagePreview, TabStrip
"""

import tkinter as tk
from ui.theme import COLOR, FONT_PIXEL, FONT_SMALL, FONT_TITLE, FONT_INPUT


class PixelButton(tk.Button):
    """
    Tombol bergaya Win95 dengan efek hover dan active state.
    
    Variant:
    - normal (default): bg #C0C0C0, relief raised
    - primary: bg #000080, fg white — untuk aksi utama (Encode/Decode)
    - danger: bg #800000, fg white — untuk aksi destruktif
    """

    def __init__(self, parent, variant="normal", **kwargs):
        # Styling berdasarkan variant
        if variant == "primary":
            defaults = {
                "bg":              COLOR["accent"],
                "fg":              COLOR["accent_txt"],
                "activebackground": "#0000A0",
                "activeforeground": COLOR["accent_txt"],
                "font":            FONT_PIXEL,
                "relief":          "raised",
                "bd":              2,
                "cursor":          "arrow",
                "padx":            10,
                "pady":            4,
            }
            self._hover_color   = "#0000A0"
            self._normal_color  = COLOR["accent"]
        else:
            defaults = {
                "bg":              COLOR["bg"],
                "fg":              COLOR["text"],
                "activebackground": "#A0A0A0",
                "activeforeground": COLOR["text"],
                "font":            FONT_PIXEL,
                "relief":          "raised",
                "bd":              2,
                "cursor":          "arrow",
                "padx":            8,
                "pady":            3,
            }
            self._hover_color   = "#D0D0D0"
            self._normal_color  = COLOR["bg"]

        # Gabungkan defaults dengan kwargs (kwargs override)
        for key, val in defaults.items():
            kwargs.setdefault(key, val)

        super().__init__(parent, **kwargs)
        self._variant = variant

        # Bind hover events
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, event):
        if str(self["state"]) != "disabled":
            self.config(bg=self._hover_color)

    def _on_leave(self, event):
        if str(self["state"]) != "disabled":
            self.config(bg=self._normal_color)


class PixelFrame(tk.LabelFrame):
    """
    LabelFrame bergaya Win95 — 'Group Box' dengan border groove.
    Label di-uppercase untuk keterbacaan di pixel font.
    """

    def __init__(self, parent, text="", **kwargs):
        defaults = {
            "text":   f" {text.upper()} " if text else "",
            "font":   FONT_PIXEL,
            "bg":     COLOR["bg"],
            "fg":     COLOR["text"],
            "bd":     2,
            "relief": "groove",
        }
        for key, val in defaults.items():
            kwargs.setdefault(key, val)

        super().__init__(parent, **kwargs)


class StatusBar(tk.Frame):
    """
    Status bar tiga panel di bagian bawah window.
    Panel: [status teks] [dimensi & format] [kapasitas]
    """

    def __init__(self, parent, **kwargs):
        kwargs.setdefault("bg", COLOR["bg"])
        kwargs.setdefault("bd", 1)
        kwargs.setdefault("relief", "sunken")
        super().__init__(parent, **kwargs)

        self._status_var   = tk.StringVar(value="Siap")
        self._info_var     = tk.StringVar(value="")
        self._capacity_var = tk.StringVar(value="")

        # Panel kiri — status utama
        self._lbl_status = tk.Label(
            self,
            textvariable=self._status_var,
            font=FONT_SMALL,
            bg=COLOR["bg"],
            fg=COLOR["status_info"],
            relief="sunken",
            bd=1,
            anchor="w",
            padx=4,
        )
        self._lbl_status.pack(side="left", fill="x", expand=True)

        # Panel tengah — dimensi + format
        self._lbl_info = tk.Label(
            self,
            textvariable=self._info_var,
            font=FONT_SMALL,
            bg=COLOR["bg"],
            fg=COLOR["text"],
            relief="sunken",
            bd=1,
            width=22,
            anchor="center",
        )
        self._lbl_info.pack(side="left")

        # Panel kanan — kapasitas
        self._lbl_capacity = tk.Label(
            self,
            textvariable=self._capacity_var,
            font=FONT_SMALL,
            bg=COLOR["bg"],
            fg=COLOR["text"],
            relief="sunken",
            bd=1,
            width=24,
            anchor="center",
        )
        self._lbl_capacity.pack(side="left")

    def set_status(self, text: str, kind: str = "info"):
        """
        Update status panel kiri.
        kind: 'info' | 'ok' | 'err'
        """
        self._status_var.set(text)
        color_map = {
            "info": COLOR["status_info"],
            "ok":   COLOR["status_ok"],
            "err":  COLOR["status_err"],
        }
        self._lbl_status.config(fg=color_map.get(kind, COLOR["status_info"]))

    def set_image_info(self, width: int, height: int, fmt: str):
        """Update panel tengah dengan dimensi dan format gambar."""
        self._info_var.set(f"{width}x{height} | {fmt}")

    def set_capacity(self, capacity: int):
        """Update panel kanan dengan kapasitas pesan."""
        self._capacity_var.set(f"Kapasitas: {capacity} char")

    def clear_image_info(self):
        """Reset panel tengah dan kanan."""
        self._info_var.set("")
        self._capacity_var.set("")


class ImagePreview(tk.Label):
    """
    Widget preview gambar di dalam kotak hitam sunken.
    Gambar di-resize ke PREVIEW_W x PREVIEW_H menggunakan NEAREST (pixel-art).
    """

    def __init__(self, parent, width=160, height=120, **kwargs):
        kwargs.setdefault("bg", "#000000")
        kwargs.setdefault("relief", "sunken")
        kwargs.setdefault("bd", 2)
        kwargs.setdefault("width", width)
        kwargs.setdefault("height", height)
        kwargs.setdefault("text", "[NO IMAGE]")
        kwargs.setdefault("fg", COLOR["bg_dark"])
        kwargs.setdefault("font", FONT_SMALL)
        super().__init__(parent, **kwargs)
        self._photo = None
        self._pw = width
        self._ph = height

    def set_image(self, pil_image):
        """Tampilkan PIL Image di preview (resize NEAREST)."""
        from PIL import Image, ImageTk
        thumb = pil_image.copy()
        thumb.thumbnail((self._pw, self._ph), Image.NEAREST)
        self._photo = ImageTk.PhotoImage(thumb)
        self.config(image=self._photo, text="")

    def clear(self):
        """Reset preview ke placeholder."""
        self._photo = None
        self.config(image="", text="[NO IMAGE]")


class TabStrip(tk.Frame):
    """
    Custom tab strip bergaya Win95 — bukan ttk.Notebook.
    Gunakan add_tab() untuk mendaftarkan tab setelah inisialisasi.

    Cara pakai:
        strip = TabStrip(parent)
        strip.pack(fill="both", expand=True)
        strip.add_tab("encode", "Encode", encode_frame)
        strip.add_tab("decode", "Decode", decode_frame)
    """

    def __init__(self, parent, **kwargs):
        kwargs.setdefault("bg", COLOR["bg"])
        super().__init__(parent, **kwargs)

        self._buttons  = {}   # key -> tk.Button
        self._frames   = {}   # key -> tk.Frame (konten tab)
        self._active   = None

        # Baris tombol tab
        self._strip = tk.Frame(self, bg=COLOR["bg"])
        self._strip.pack(side="top", fill="x")

        # Separator
        tk.Frame(self, bg=COLOR["border_dk"], height=2).pack(side="top", fill="x")

        # Container konten — semua frame tab hidup di sini sebagai anak langsung
        self._container = tk.Frame(self, bg=COLOR["bg"])
        self._container.pack(side="top", fill="both", expand=True)

    def add_tab(self, key: str, label: str, frame: tk.Frame):
        """
        Daftarkan tab.
        frame HARUS sudah dibuat dengan self._container sebagai parent.
        """
        btn = tk.Button(
            self._strip,
            text=f"  {label}  ",
            font=FONT_PIXEL,
            bg=COLOR["bg_dark"],
            fg=COLOR["text"],
            activebackground=COLOR["bg"],
            activeforeground=COLOR["text"],
            relief="raised",
            bd=2,
            cursor="arrow",
            command=lambda k=key: self.switch(k),
        )
        btn.pack(side="left", padx=(2, 0), pady=(4, 0))

        self._buttons[key] = btn
        self._frames[key]  = frame

        # Aktifkan tab pertama secara otomatis
        if self._active is None:
            self.switch(key)

    def switch(self, key: str):
        """Tampilkan tab dengan key tertentu, sembunyikan yang lain."""
        # Sembunyikan semua
        for k, f in self._frames.items():
            f.pack_forget()

        # Reset semua tombol ke non-aktif
        for k, b in self._buttons.items():
            b.config(bg=COLOR["bg_dark"], relief="raised", bd=1)

        # Tampilkan tab aktif
        self._frames[key].pack(fill="both", expand=True)
        self._buttons[key].config(bg=COLOR["bg"], relief="ridge", bd=2)
        self._active = key
