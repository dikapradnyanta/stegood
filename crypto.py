"""
crypto.py — Modul enkripsi ROT13 untuk StegoodXP
ROT13 adalah cipher substitusi sederhana: setiap huruf digeser 13 posisi.
Karena alfabet memiliki 26 huruf, fungsi encode dan decode identik.
"""

import codecs


def rot13_encode(text: str) -> str:
    """Enkripsi teks menggunakan ROT13."""
    return codecs.encode(text, 'rot_13')


def rot13_decode(text: str) -> str:
    """Dekripsi teks ROT13 (identik dengan encode karena ROT13 simetris)."""
    return codecs.encode(text, 'rot_13')
