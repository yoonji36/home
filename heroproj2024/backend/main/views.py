from django.shortcuts import render

def main_page(request):
    return render(request, 'index.html')

def my_records(request):
    return render(request, 'my_records.html')

def create_recipe(request):
    return render(request, 'create_recipe.html')
