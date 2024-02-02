import datetime
import os
import secrets

from fastapi import FastAPI, UploadFile
from music_maker import make_music
from settings import make_file_name

app = FastAPI()

@app.get("/prompt")  #get으로 바꾸고 링크를 바디로 받으면 프롬프트 생성해서 반환하는 걸로 변경하기
async def upload_mp4(video_url: str):
    return make_music("./drive/MyDrive/Video2Text.pt", video_url)

@app.post("/mp4-upload")
async def upload_mp4(file: UploadFile):
    return make_file_name(file, ".mp4")

@app.post("/wav-upload")
async def upload_wav(file: UploadFile):
    return make_file_name(file, ".wav")
