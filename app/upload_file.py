import os
import time
import re
from fastapi import HTTPException, UploadFile
from app.utils import get_s3_client
import boto3

# Custom function to sanitize filenames (no need for werkzeug)
def sanitize_filename(filename):
    # Replace spaces with underscores and remove any special characters except for alphanumeric, underscores, and periods
    filename = filename.strip()  # Remove leading/trailing whitespaces
    filename = re.sub(r'[^A-Za-z0-9._-]', '_', filename)  # Replace non-alphanumeric characters with underscores
    return filename

# Upload a file to a bucket
async def upload_file(file: UploadFile, file_name='file', username=None):
    # Get S3 client from utils.py
    s3_client = get_s3_client()
    if not s3_client:
        raise HTTPException(status_code=500, detail="S3 client not configured properly")

    # Get bucket name from environment variables
    bucket_name = os.getenv("LIARA_BUCKET_NAME")
    if not bucket_name:
        raise HTTPException(status_code=500, detail="Bucket name not configured")

    # Sanitize the file name to make sure it's safe for use
    filename = sanitize_filename(file_name)

    # If username is provided, prepend it to the filename
    if username:
        filename = f"{username}_{filename}"

    # Add a timestamp to ensure uniqueness
    timestamp = str(int(time.time()))
    filename = f"{filename}_{timestamp}"

    try:
        # Upload the file to S3
        with open(f"/tmp/{filename}", "wb") as tmp_file:
            content = await file.read()
            tmp_file.write(content)

        # Upload the file from temporary storage to S3
        with open(f"/tmp/{filename}", "rb") as tmp_file:
            s3_client.upload_fileobj(tmp_file, bucket_name, filename)

        # Optionally remove the temporary file after upload
        os.remove(f"/tmp/{filename}")

        return generate_url(bucket_name, filename)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {e}")

def generate_url(bucket_name, filename):
    endpoint_url = os.getenv("LIARA_ENDPOINT_URL")
    if not endpoint_url:
        raise HTTPException(status_code=500, detail="Endpoint URL not configured")
    endpoint_url = endpoint_url.replace("https://", "").replace("http://", "")  
    return f"https://{bucket_name}.{endpoint_url}/{filename}"
