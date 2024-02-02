import os
import uuid
from google.cloud import storage

def make_file_name(file, extenstion_name):
    KEY_PATH = "${KEY_PATH}"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY_PATH

    storage_client = storage.Client()

    # 서비스 계정 생성한 bucket 이름 입력
    bucket_name = 'diony'
    # 블랍 이름
    destination_blob_name = f"{uuid.uuid1()}{extenstion_name}"
    # 버킷 선택
    bucket = storage_client.get_bucket(bucket_name)
    # 블랍 객체 생성
    blob = bucket.blob(destination_blob_name)
    # 파일 업로드
    blob.upload_from_file(file.file)
    return blob.public_url
