# st.title("_Streamlit_ is :blue[cool] :sunglasses:")

# multi = """If you end a line with two spaces,
# a soft return is used for the next line.

# Two (or more) newline characters in a row will result in a hard return.
# """
# st.markdown(multi)

# st.markdown("*Streamlit* is **really** ***cool***.")
# st.markdown(
#     """
#     :red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in]
#     :gray[pretty] :rainbow[colors] and :blue-background[highlight] text."""
# )
# st.markdown(
#     "Here's a bouquet &mdash;\
#             :tulip::cherry_blossom::rose::hibiscus::sunflower::blossom:"
# )

import streamlit as st
from langchain_core.messages.chat import ChatMessage

st.title("나만의 ChatGPT TEST")

if "messages" not in st.session_state:  # 처음 한번만 초기화
    st.session_state["messages"] = []  # 대화 저장하기 위한 용도


# 이전 대화 출력
def print_messages():
    """세션 상태의 메시지를 출력하는 함수"""
    for chat_message in st.session_state["messages"]:
        # st.write(f"{chat_message.role}: {chat_message.content}")
        st.chat_message(chat_message.role).write(chat_message.content)


# 새로운 메시지 추가
def add_message(role, message):
    st.session_state["messages"].append(
        ChatMessage(role=role, content=user_input)
    )  # 대화 기록 저장


print_messages()  # 이전 대화 출력

# 이전 저장된 메시지 출력
# for role, message in st.session_state["messages"]:  # 딕셔너리 안에서 튜플의 키, 값 조회
#     st.chat_message(role).write(message)  # 튜플의 키, 값을 찍어줌

# 사용자의 입력
user_input = st.chat_input("궁금한 내용을 물어보세요.")

# 사용자 입력이 들어오면,
if user_input:
    # with st.chat_message("user"):
    #     st.write(user_input)
    # 최초에 찍어주고,
    st.chat_message("user").write(user_input)  # with ~ 와 같은 의미
    st.chat_message("assistant").write(user_input)
    # 대화 기록 저장
    add_message("user", user_input)
    add_message("assistant", user_input)
    # st.session_state["messages"].append(("user", user_input))  # tuple 형식으로 저장
    # st.session_state["messages"].append(("assistant", user_input))
