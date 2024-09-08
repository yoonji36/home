from django.shortcuts import render, redirect
from django.core.files.storage import default_storage  # default_storage 임포트
from django.core.files.base import ContentFile

# Create your views here.

def main_page(request):
    return render(request, 'index.html')

def image_upload(request):
    if request.method == 'POST':
        image_file = request.FILES['image']
        # 이미지를 저장
        file_name = default_storage.save(image_file.name, image_file)
        image_path = default_storage.path(file_name)
        
        # mdl 앱으로 이미지 경로 전달
        return redirect('process_image', image_path=file_name)
    
    return render(request, 'image-upload.html')