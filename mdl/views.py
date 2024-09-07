from django.shortcuts import render

# Create your views here.
from django.core.files.storage import default_storage
from openvino.inference_engine import IECore
import cv2
import numpy as np
import os

# Inference Engine 초기화
ie = IECore()
model_path = 'path/to/openvino_model/yolov5s.xml'
weights_path = 'path/to/openvino_model/yolov5s.bin'
net = ie.read_network(model=model_path, weights=weights_path)
exec_net = ie.load_network(network=net, device_name='CPU')  # GPU를 사용할 경우 'GPU'

def image_upload_view(request): # llm에 넣어도 됨
    if request.method == 'POST' and request.FILES['image']:
        image_file = request.FILES['image']
        file_path = default_storage.save('uploads/' + image_file.name, image_file)
        
        # 이미지 로드 및 전처리
        image = cv2.imread(file_path)
        input_blob = next(iter(net.input_info))
        output_blob = next(iter(net.outputs))
        n, c, h, w = net.input_info[input_blob].input_data.shape

        image_resized = cv2.resize(image, (w, h))
        input_data = np.expand_dims(image_resized.transpose(2, 0, 1), axis=0)
        
        # 모델 추론
        res = exec_net.infer(inputs={input_blob: input_data})
        
        # 결과 후처리 및 텍스트로 변환 (추론 결과에 따라 적절히 처리)
        # 여기에 YOLOv5 결과 처리 코드를 추가하세요.
        detected_objects = process_results(res, output_blob)  # 예시 함수
        
        # 업로드된 파일 삭제
        os.remove(file_path)
        
        return render(request, 'result.html', {'detected_objects': detected_objects})
    return render(request, 'upload.html')