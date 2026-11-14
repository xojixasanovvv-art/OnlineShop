"""
auth_helpers.py — eski kod bilan moslik uchun wrapper
Yangi kod apps.dependencies dan foydalanadi.
"""
from apps.dependencies import get_current_user, require_admin

# eski nomlar saqlab qolindi — boshqa fayllar buzilmasligi uchun
check_admin = require_admin
