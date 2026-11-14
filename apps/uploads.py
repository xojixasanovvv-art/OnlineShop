"""
uploads.py — rasm fayllarini xavfsiz qabul qilish.

Fayl kengaytmasi va Content-Type mijozdan kelgani uchun ularga ishonib
bo'lmaydi. Shuning uchun format fayl mazmuni (magic bytes) orqali
aniqlanadi. SVG/HTML kabi bajariladigan fayllar rad etiladi.
"""
from fastapi import HTTPException, UploadFile

from apps.i18n import t

MAX_IMAGE_BYTES = 5 * 1024 * 1024          # avatar, mahsulot rasmi — 5 MB
MAX_SCREENSHOT_BYTES = 10 * 1024 * 1024    # to'lov cheki — 10 MB

# (magic bytes, MIME, xavfsiz kengaytma)
_SIGNATURES = (
    (b"\xff\xd8\xff", "image/jpeg", ".jpg"),
    (b"\x89PNG\r\n\x1a\n", "image/png", ".png"),
    (b"GIF87a", "image/gif", ".gif"),
    (b"GIF89a", "image/gif", ".gif"),
)


def detect_image_type(data: bytes) -> tuple[str, str] | None:
    """Baytlar bo'yicha rasm formatini aniqlaydi. Rasm bo'lmasa None."""
    for signature, mime, ext in _SIGNATURES:
        if data.startswith(signature):
            return mime, ext
    # WEBP: RIFF....WEBP
    if len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "image/webp", ".webp"
    return None


def validate_image(data: bytes, max_bytes: int, lang: str = "uz") -> tuple[str, str]:
    """Hajm va formatni tekshiradi. (mime, ext) qaytaradi, xato bo'lsa HTTPException."""
    if len(data) > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=t("imageTooLarge", lang, max_mb=max_bytes // (1024 * 1024)),
        )
    detected = detect_image_type(data)
    if not detected:
        raise HTTPException(status_code=400, detail=t("imageTypeInvalid", lang))
    return detected


def read_image(file: UploadFile, max_bytes: int, lang: str = "uz") -> tuple[bytes, str, str]:
    """Sinxron endpointlar uchun: faylni limit bilan o'qib, tekshiradi."""
    data = file.file.read(max_bytes + 1)
    mime, ext = validate_image(data, max_bytes, lang)
    return data, mime, ext
