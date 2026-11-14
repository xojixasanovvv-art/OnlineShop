"""
i18n.py — Backend multilanguage (UZ/RU/EN)
Accept-Language header yoki ?lang=uz|ru|en orqali til tanlanadi.
locale/*.json fayllardan yuklanadi.
"""
import json
from pathlib import Path
from fastapi import Request, Query
from typing import Optional

LOCALE_DIR = Path(__file__).parent.parent / "locale"
SUPPORTED = {"uz", "ru", "en"}
_cache: dict[str, dict[str, str]] = {}

def _load(lang: str) -> dict[str, str]:
    if lang in _cache:
        return _cache[lang]
    path = LOCALE_DIR / f"{lang}.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        _cache[lang] = data
        return data
    except Exception:
        return {}

def get_lang(request: Request, lang: Optional[str] = Query(default=None, description="uz|ru|en")) -> str:
    """Dependency — tilni aniqlaydi: ?lang > Accept-Language > uz"""
    if lang and lang in SUPPORTED:
        return lang
    # Accept-Language: ru, en;q=0.9, uz;q=0.8
    header = request.headers.get("accept-language", "")
    for part in header.split(","):
        code = part.split(";")[0].strip().split("-")[0].lower()
        if code in SUPPORTED:
            return code
    return "uz"

def t(key: str, lang: str = "uz", **kwargs) -> str:
    """Kalit bo'yicha tarjima, kwargs bilan format"""
    data = _load(lang)
    # fallback uz
    if key not in data:
        data = _load("uz")
    text = data.get(key, key)
    try:
        return text.format(**kwargs)
    except Exception:
        return text
