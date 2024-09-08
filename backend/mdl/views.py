from django.shortcuts import render
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from ultralytics import YOLO
import pathlib
import torch  # YOLOv5 사용
import os

# 임시로 PosixPath를 WindowsPath로 변경
pathlib.PosixPath = pathlib.WindowsPath

# YOLOv5 모델 로드 (torch.hub 사용) # ★★★★★
model = torch.hub.load('C:/home/backend/yolov5', 'custom', path='C:/home/best.pt', source='local', force_reload=True)  # ★★★★★

def process_image(request, image_path):
    # YOLOv5 모델을 이용한 객체 인식
    full_image_path = os.path.join(default_storage.location, image_path)
    results = model(full_image_path)
    ingredients = results.pandas().xyxy[0]['name'].unique().tolist()  # 인식된 객체 이름 추출

    # ingredients.html로 식재료 리스트 전달
    return render(request, 'ingredients.html', {'ingredients': ingredients})