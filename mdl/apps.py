from django.apps import AppConfig

import torch

# Python 코드

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.eval()
dummy_input = torch.randn(1, 3, 640, 640)  # 더미 입력
torch.onnx.export(model, dummy_input, "yolov5s.onnx", opset_version=12)

class MdlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mdl'
