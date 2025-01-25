import base64
import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv('/home/ubuntu/project/.env')  # .env 파일을 로드
import openai

# api key 가져오기기
client = os.getenv("OPENAI_API_KEY")

if client:
    print("API 키를 성공적으로 가져왔습니다.")
else:
    raise ValueError("API 키를 가져오지 못했습니다. .env 파일을 확인하세요.")


def clear_input():
    st.session_state["user_input"] = ""

def image_response(base64_image):
    response = openai.chat.completions.create(
        model = "gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "해당 이미지는 어떤 음식이야?, 음식 이름만으로 대답해줘",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
    )

    food_name = response.choices[0].message.content
    return food_name.strip()

def generate_prompt(food_name):
    prompt = (
        f"제일처음에 {food_name}을 먼저 알려주고 시작해"
        f"'{food_name}'에 대한 자세한 정보를 알려줘. "
        f"이 음식의 칼로리는 얼마이고 다이어트에 어떤 좋은효과나 부정적 효과가 있는지 설명해줘 "
        f"추가적으로 영양 성분, 탄수화물, 단백질, 지방 함량도 알려줘"
    )
    return prompt

def query_llm(prompt):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.7
    )
    return  response

    
st.title("음식정보 chat Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []
    
images = st.file_uploader(
    "음식 이미지를 업로드 해주세요", type=['png','jpg','jpeg'] 
)

if images:
    st.write("### 업로드된 이미지")
    
    st.image(images, caption=images.name, use_container_width=True)
    image_data = base64.b64encode(images.read()).decode("utf-8")
    
    result_food_name = image_response(image_data)
    
    prompt = generate_prompt(result_food_name)
    if not any("assistant" in msg["role"] for msg in st.session_state.messages):

        llm_response = query_llm(prompt)
        result_response = llm_response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": result_response.strip()})

    # 이전 대화 내역 표시 (최초 렌더링)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        

if user_input := st.chat_input("추가로 궁금한 점을 입력하세요:"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)

    followup_response = query_llm(user_input)
    next_response = followup_response.choices[0].message.content
   
    st.session_state.messages.append({"role": "assistant", "content": next_response.strip()})
    with st.chat_message("assistant"):
        st.markdown(next_response.strip())



