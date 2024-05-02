import streamlit as st
from PIL import Image
import google.generativeai as genai

with open("key.txt") as f:
  key=f.read()
genai.configure(api_key=key)
def get_gemini_response(model_name,prompt, temperature, top_k,top_p):
    generation_config = {
        "temperature": temperature,
        "top_p": 1,
        "top_k": top_k,
        "max_output_tokens": 2048,
    }

    model = genai.GenerativeModel(model_name
                                  ,generation_config=generation_config
                                  )

    response = model.generate_content(prompt)
    return response.text

    # 初始化Streamlit應用
st.set_page_config(page_title="Gemini Image Chatbot")

# 定義各個頁面的功能
def home_page():
    st.header("Gemini應用")
    # 設置gemini 參數
    temperature = st.sidebar.slider('temperature', min_value=0.0, max_value=1.0, value=0.7)
    top_p = st.sidebar.slider('top_p', min_value=0.0, max_value=1.0, value=1.0)
    top_k = st.sidebar.number_input('Top K', min_value=1, max_value=10, value=1, step=1)
    # 設置聊天記錄
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # 聊天室佈局
    chat_container = st.container()

    # 創建form
    with st.form("chat_form", clear_on_submit=True):
        input_text = st.text_input("Your message:")
        uploaded_file = st.file_uploader("Upload an image (optional):", type=["jpg", "jpeg", "png"])
        submit_button = st.form_submit_button("Send")

        if uploaded_file is not None:
            # 顯示上傳完成提示
            st.success('Upload finished!')

        if submit_button and (input_text or uploaded_file):
            # submit且有內容
            if uploaded_file:
                # image and text
                image = Image.open(uploaded_file)
                response = get_gemini_response("gemini-pro-vision",[input_text, image],temperature,top_k,top_p)

            else:
                # only text
                response = get_gemini_response("gemini-1.0-pro",input_text,temperature,top_k,top_p)
                image = None

            # 新增至歷史紀錄
            st.session_state['chat_history'].append(("You", input_text, image))
            st.session_state['chat_history'].append(("Bot", response, None))


    with chat_container:
            for idx, (user, text, img) in enumerate(st.session_state['chat_history']):
                # 取得紀錄
                if user == "You":
                    # 用戶的訊息和圖標
                    st.markdown(f"<img src='https://w7.pngwing.com/pngs/722/101/png-transparent-computer-icons-user-profile-circle-abstract-miscellaneous-rim-account-thumbnail.png' class='icon' style='width: 50px; height: auto;'> **You (message {idx}):**", unsafe_allow_html=True)
                    st.markdown(f"{text}")
                else:
                    # 機器人的訊息和圖標
                    st.markdown(f"<img src='https://cdn-icons-png.flaticon.com/512/4712/4712035.png' class='icon' style='width: 50px; height: auto;'> **Bot replied (message {idx}):**", unsafe_allow_html=True)
                    st.markdown(f"{text}")
                if img is not None:
                    st.image(img, use_column_width=True)


    st.write("Welcome to the home page!")



def chatbot_page():
    st.title("Chatbot Page")
    st.write("Here you can interact with the chatbot.")

def settings_page():
    st.title("Settings Page")
    st.write("Adjust the application settings here.")

with st.sidebar:
    st.title("Navigation")
    page = st.radio("Choose a page:", ['Home', 'Chatbot', 'Settings'])

if page == 'Home':
    home_page()
elif page == 'Chatbot':
    chatbot_page()
elif page == 'Settings':
    settings_page()
