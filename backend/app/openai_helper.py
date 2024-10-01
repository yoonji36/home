import openai

openai.api_key = 'your-openai-api-key'

def generate_meal_plan(bmi, target_calories, blood_sugar):
    prompt = f"""
    사용자 정보: BMI는 {bmi}, 하루 섭취 칼로리 목표는 {target_calories} kcal입니다.
    혈당 수치는 {blood_sugar}이며, Glycemic Index(GI)가 55 이하인 음식으로 아침, 점심, 저녁 식단을 만들어 주세요.
    각각의 식단은 칼로리 목표에 맞춰 주세요.
    """

    response = openai.Completion.create(
        engine="gpt-4",  # 사용할 모델 버전
        prompt=prompt,
        max_tokens=300  # 응답 텍스트 길이 제한
    )

    # GPT가 생성한 식단 결과를 반환
    return response.choices[0].text.strip()