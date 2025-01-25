import base64
import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
load_dotenv('/home/ubuntu/project/.env')  # .env 파일을 로드

def clear_input():
    st.session_state["user_input"] = ""

# api key 가져오기기
client = os.getenv("OPENAI_API_KEY")

if client:
    print("API 키를 성공적으로 가져왔습니다.")
else:
    raise ValueError("API 키를 가져오지 못했습니다. .env 파일을 확인하세요.")

    
st.title("duhyeon chat Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []
    
images = st.file_uploader(
    "이미지를 업로드 해주세요", type=['png','jpg','jpeg'], accept_multiple_files = True 
)# 여러 이미지 불러오기

if images:
    st.write("### 업로드된 이미지")
    
    chat = ChatOpenAI(model="gpt-4o-mini", max_tokens=300)
    content = []

    
    for upload_image in images:
        st.image(upload_image, caption=upload_image.name, use_container_width=True)
        image_data = base64.b64encode(upload_image.read()).decode("utf-8")
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
        })
        
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("궁금한 점을 입력하세요:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
  
  
      
        try:
            messages = [HumanMessage(content=[
            {"type": "text", "text": prompt},
            *content
            ])]

            response = chat.invoke(messages)
            assistant_response = response.content

            with st.chat_message("assistant"):
                    st.markdown(assistant_response)
            

            st.session_state.messages.append({"role": "assistant", "content": assistant_response})


        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")