from fastapi import HTTPException
from app.utils import get_s3_client
import os
import time


# Upload a file to a bucket
def upload_file(file, file_name='file'):
    # Get S3 client from utils.py
    s3_client = get_s3_client()
    if not s3_client:
        raise HTTPException(status_code=500, detail="S3 client not configured properly")
    bucket_name = os.getenv("LIARA_BUCKET_NAME")
    if not bucket_name:
        raise HTTPException(status_code=500, detail="Bucket name not configured")

    filename = file_name + "_" + str(int(time.time()))
    try:
        s3_client.upload_fileobj(file, bucket_name, filename)
        return filename
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {e}")
