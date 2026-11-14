"""
minio_client.py — MinIO S3 bilan ishlash
MINIO_ENDPOINT bo'sh bo'lsa yoki ulanmasa fallback static/media ga saqlaydi.
Bucket public qilinadi, URL: http://endpoint/bucket/key yoki https
"""
import os
import io
from typing import Optional

from apps.config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET, MINIO_SECURE

_client = None

def get_minio_client():
    global _client
    if _client is not None:
        return _client
    if not MINIO_ENDPOINT:
        return None
    try:
        from minio import Minio
        _client = Minio(
            MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=MINIO_SECURE,
        )
        # bucket borligini tekshirish / yaratish
        try:
            if not _client.bucket_exists(MINIO_BUCKET):
                _client.make_bucket(MINIO_BUCKET)
                # public policy
                policy = f'{{"Version":"2012-10-17","Statement":[{{"Effect":"Allow","Principal":"*","Action":["s3:GetObject"],"Resource":["arn:aws:s3:::{MINIO_BUCKET}/*"]}}]}}'
                _client.set_bucket_policy(MINIO_BUCKET, policy)
        except Exception as e:
            print(f"[MinIO] bucket check failed: {e}")
        return _client
    except Exception as e:
        print(f"[MinIO] init failed: {e}")
        return None

def upload_bytes(data: bytes, key: str, content_type: str = "image/jpeg") -> Optional[str]:
    """Bytes ni MinIO ga yuklaydi, URL qaytaradi. Xato bo'lsa None."""
    client = get_minio_client()
    if not client:
        return None
    try:
        client.put_object(MINIO_BUCKET, key, io.BytesIO(data), length=len(data), content_type=content_type)
        # public URL — brauzer uchun localhost ga aylantiramiz (docker da minio:9000 → localhost:9000)
        scheme = "https" if MINIO_SECURE else "http"
        public_endpoint = MINIO_ENDPOINT.replace("minio:", "localhost:") if "minio:" in MINIO_ENDPOINT else MINIO_ENDPOINT
        return f"{scheme}://{public_endpoint}/{MINIO_BUCKET}/{key}"
    except Exception as e:
        print(f"[MinIO] upload failed {key}: {e}")
        return None

def upload_fileobj(file_obj, key: str, content_type: str = "image/jpeg") -> Optional[str]:
    data = file_obj.read()
    # file_obj may be SpooledTemporaryFile after read, reset not needed after
    return upload_bytes(data, key, content_type)

def ensure_bucket():
    c = get_minio_client()
    return c is not None
