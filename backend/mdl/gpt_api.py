# -*- coding: utf-8 -*-
from openai import OpenAI
import json
import os

### 꼭 설정하기 ###
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment.")


def run_chatGPT(messages, model_id):
    print("....simple:model ->", model_id)
    print(f"Using API Key: {OPENAI_API_KEY}")
    print(f"Messages: {messages}")
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        result = client.chat.completions.create(
            model=model_id,
            messages=messages,
            stream=False,
        )
        print(f"API Response: {result}")  # API 응답 로깅
        return result
    except Exception as e:
        print(f"API 호출 중 오류 발생: {e}")  # 오류 로깅
        raise


def res_recipe(calorie_limit, ingredients_list, prompt):
    try:
        print(f"프롬프트: {prompt}")
        print(f"재료: {ingredients_list}, 칼로리 제한: {calorie_limit}")

        lstMessages = [
            {
                "role": "system",
                "content": (
                    "당신은 요리 컨설턴트입니다. 사용자가 제공한 재료와 조건에 따라 적절한 레시피를 JSON 형식으로 추천해주세요."
                    "JSON 응답에는 'title', 'ingredients', 'instructions' 키가 포함되어야 합니다."
                    "영어가 아닌 한국어로 추천해주세요."
                    "한국사람들에게 친근한 레시피를 추천해주세요."
                )
            },
            {"role": "user", "content": prompt},
        ]

        # GPT API 호출
        response = run_chatGPT(lstMessages, "gpt-4")
        print(f"GPT 응답: {response}")

        # 응답 파싱 및 JSON 확인
        content = response.choices[0].message.content.strip()
        print(f"GPT 응답 내용 (원본): {content}")

        # JSON 파싱 시도
        try:
            recipe_data = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"JSON 파싱 오류: {str(e)}")
            raise ValueError("올바르지 않은 JSON 형식입니다.")

        # 필수 키 검증
        required_keys = {"title", "ingredients", "instructions"}
        if not required_keys.issubset(recipe_data.keys()):
            raise ValueError(f"응답 데이터에 누락된 키가 있습니다: {recipe_data.keys()}")

        print(f"파싱된 레시피 데이터: {recipe_data}")
        return recipe_data

    except Exception as e:
        print(f"레시피 생성 중 오류 발생: {str(e)}")
        raise
