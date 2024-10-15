from django.shortcuts import render, redirect
from django.core.files.storage import default_storage  # default_storage 임포트
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from login.models import Profile
from main.models import Myhistory
from main.gpt_api import res_recipe
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

@csrf_exempt
def make_recipe(request):
    if request.method == 'POST':
        ingredient_list = request.POST.getlist("ingredient-list")
        print("----make_recipe-----")
        print(ingredient_list)
        user = request.user    # 현재 로그인한 사용자정보를 확인
        print(user.id, user.username)
        profile = Profile.objects.get(user_id=user.id)
        print(profile)
        bmi_val = profile.bmi
        blood_pressure = profile.blood_pressure
        chatgpt_response = res_recipe(bmi_val, blood_pressure, ingredient_list)
        print(chatgpt_response)
        context = {"username": user.username,"res_recipe": chatgpt_response}
        str_ingredient = ''
        for ingredient in ingredient_list:
            str_ingredient += ingredient+","
        myHistory = Myhistory(user=user,ingredient_list=str_ingredient,chatgpt_response = chatgpt_response )
        myHistory.save()
    return render(request, 'recipes.html',context)