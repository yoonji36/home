import torch
import torch.onnx

# YOLOv5 모델 로드 (여기서는 'yolov5s'를 사용)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.eval()
# 로컬 경로에서 모델 불러오기
# model = torch.hub.load('/yolov5', 'custom', path='path/to/best.pt', source='local')
# model.eval()

# 더미 입력 데이터 생성 (모델의 입력 형식에 맞춤)
dummy_input = torch.randn(1, 3, 640, 640)

# 모델을 ONNX 형식으로 내보내기
torch.onnx.export(model, dummy_input, "yolov5s.onnx", opset_version=12)

print("모델이 성공적으로 ONNX 형식으로 변환되었습니다.")