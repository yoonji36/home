import torch
from PIL import Image
from torchvision import transforms

# 모델을 로드하는 함수
def load_model(model_path):
    model = torch.load(model_path)  # 모델 파일 로드
    model.eval()  # 추론 모드로 설정
    return model