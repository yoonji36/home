from django.db import models

import xml.etree.ElementTree as ET

def parse_recipe_xml(xml_data):
    # XML 데이터를 파싱합니다.
    root = ET.fromstring(xml_data)

    # 필요한 데이터 추출
    recipe_name = root.find('.//RCP_NM').text
    ingredients = root.find('.//RCP_PARTS_DTLS').text
    manual_steps = [manual.text for manual in root.findall('.//MANUAL') if manual.text]
    
    # 새로운 항목 추가
    main_image_url = root.find('.//ATT_FILE_NO_MAIN').text
    mk_image_url = root.find('.//ATT_FILE_NO_MK').text

    return {
        "recipe_name": recipe_name,
        "ingredients": ingredients,
        "manual_steps": manual_steps,
        "main_image_url": main_image_url,  # 추가된 이미지 URL
        "mk_image_url": mk_image_url,      # 추가된 이미지 URL
    }

# 조리방법 JSON으로 저장
class Recipe(models.Model):
    name = models.CharField(max_length=255)
    image_url = models.URLField()
    ingredients = models.TextField()
    cooking_steps = models.JSONField()  # 조리 방법을 JSON으로 저장