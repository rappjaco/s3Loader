import boto3
import os

s3 = boto3.client("s3")
BUCKET = "s3loader-app"
SCAN_DIR = "/tmp/scan_dir/"


def write_file_shared_storage(data, file_name):
    try:
        os.makedirs(SCAN_DIR, exist_ok=True)
        with open(f"{SCAN_DIR}{file_name}", "wb") as f:
            f.write(data)
        return f"{file_name} successfully upload to share drive"
    except Exception as e:
        return f"error: {e}"


def list_bucket_files():
    try:
        return s3.list_objects_v2(Bucket=BUCKET)["Contents"]
    except Exception as e:
        return f"error: {e}"


def upload_file_s3(filename):
    try:
        response = s3.upload_file(f"{SCAN_DIR}{filename}", BUCKET, filename)
        print(f"UPLOADED: {filename}")
        return response
    except Exception as e:
        return {f"error: {e}"}

