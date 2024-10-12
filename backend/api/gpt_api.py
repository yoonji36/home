import os, sys
import openai, json
from openai import OpenAI
import os,sys
dirname = os.path.dirname
#sys.path.append( dirname(dirname(dirname(__file__))))
#import config as config

open_api_key = os.getenv('OPENAI_API_KEY')

#        Model-id 는 아래중 한개임
# RUN_MODEL = "gpt-3.5-turbo"  # max 3017 words
# RUN_MODEL = "gpt-4"  # max 6144 words

def run_chatGPT(messages,model_id):
    print("....simple:model ->",model_id)
    print("....simple:messages ->", messages)
    try:

        client = OpenAI(api_key=open_api_key)
        chunked_result_list = client.chat.completions.create(
            model=model_id,
            messages=messages,
            stream=False,
        )
        return chunked_result_list
    except Exception as e:
        raise str(e)

def test_gpt4():
    sQuestionContent = "나는 172센티에 65킬로그램정도의 체중을 가지고 있어. 하루에 물을 몇 리터정도 마시면 적당할까?"

    lstMessages = [
        {"role": "system", "content": " 당신은 건강 컨설턴트 입니다. 사용자의 답변에 전문가로서 답변해주세요."},
        {"role": "user", "content": f"{sQuestionContent}"}
    ]

    model_id='gpt-4'
    chunked_result_list = run_chatGPT(lstMessages, model_id)
    print(chunked_result_list.choices[0].message.content)
    return

if __name__ == "__main__":
    test_gpt4()
