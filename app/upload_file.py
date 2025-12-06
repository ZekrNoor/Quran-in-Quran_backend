import os
import time
import re
from fastapi import HTTPException, UploadFile
from app.utils import get_s3_client
import boto3


def sanitize_filename(filename):
    filename = filename.strip()
    filename = re.sub(r"[^A-Za-z0-9._-]", "_", filename)
    return filename


async def upload_file(file: UploadFile, file_name="file", username=None):
    s3_client = get_s3_client()
    if not s3_client:
        raise HTTPException(status_code=500, detail="S3 client not configured properly")

    bucket_name = os.getenv("LIARA_BUCKET_NAME")
    if not bucket_name:
        raise HTTPException(status_code=500, detail="Bucket name not configured")

    # ←←← MINIMAL FIXES START HERE (only 3 lines added/changed) ←←←

    # 1. Always keep the real extension from the uploaded file
    _, original_ext = os.path.splitext(file.filename or "")
    original_ext = original_ext.lower() or ""  # safety

    # 2. Use original filename when the caller passes the default 'file'
    base_name = file_name if file_name != "file" else (file.filename or "file")
    filename = sanitize_filename(base_name)

    if username:
        filename = f"{username}_{filename}"

    # 3. Define timestamp (this line was missing!)
    timestamp = str(int(time.time()))

    # Now add timestamp + original extension
    filename = f"{filename}_{timestamp}{original_ext}"

    # ←←← END OF FIXES ←←←

    tmp_path = f"/tmp/{filename}"
    try:
        with open(tmp_path, "wb") as f:
            f.write(await file.read())

        with open(tmp_path, "rb") as f:
            s3_client.upload_fileobj(f, bucket_name, filename)

        os.remove(tmp_path)
        return generate_url(bucket_name, filename)

    except Exception as e:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise HTTPException(status_code=500, detail=f"Error uploading file: {e}")


def generate_url(bucket_name, filename):
    endpoint_url = os.getenv("LIARA_ENDPOINT_URL")
    if not endpoint_url:
        raise HTTPException(status_code=500, detail="Endpoint URL not configured")
    endpoint_url = endpoint_url.replace("https://", "").replace("http://", "")
    return f"https://{bucket_name}.{endpoint_url}/{filename}"
