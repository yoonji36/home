# -*- coding: utf-8 -*-
from openai import OpenAI
import json
import os

### 꼭 설정하기 ###
OPENAI_API_KEY = os.getenv("OPEN_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment.")

def run_chatGPT(messages, model_id):
    print("....simple:model ->", model_id)
    print("....simple:messages ->", messages)
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        result = client.chat.completions.create(
            model=model_id,
            messages=messages,
            stream=False,
        )
        return result
    except Exception as e:
        raise Exception(f"API 호출 중 오류 발생: {e}")

def res_recipe(calorie_limit, ingredients_list):
    # 재료를 문자열로 변환
    sStuff = ", ".join(ingredients_list)

    # GPT에게 보낼 질문 템플릿
    sQuestionContent = (
        f"{sStuff}를 재료로 최대 {calorie_limit} 칼로리 이하의 요리 레시피를 추천해줘. "
        "레시피 제목, 이미지 URL, 사용된 재료, 그리고 만드는 법을 알려줘. "
        "JSON 형식으로 응답해줘."
    )

    # 메시지 구성
    lstMessages = [
        {
            "role": "system",
            "content": "당신은 요리 컨설턴트입니다. 사용자가 제공한 재료와 조건에 따라 적절한 레시피를 JSON 형식으로 추천해주세요. "
                    "JSON 응답에는 'title', 'image', 'ingredients', 'instructions' 키가 포함되어야 합니다."
        },
        {"role": "user", "content": sQuestionContent},
    ]

    # 모델 호출
    model_id = "gpt-4"
    response = run_chatGPT(lstMessages, model_id)

    # JSON으로 파싱
    try:
        recipe_data = json.loads(response.choices[0].message.content)
        return recipe_data
    except json.JSONDecodeError as e:
        raise Exception(f"JSON 파싱 오류: {e}")

# def test_recipe():
#     # 샘플 테스트: BMI, 혈압, 최대 칼로리와 재료 리스트
#     res = res_recipe(21, 137, 500, ['계란', '상추', '식초', '사과', '양배추', '올리브'])
#     print(res)
#     return

# if __name__ == "__main__":
#     test_recipe()
