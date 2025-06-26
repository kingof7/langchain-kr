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
from langchain_core.prompts import ChatPromptTemplate
from langchain_upstage import ChatUpstage
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

st.title("나만의 ChatGPT TEST")

if "messages" not in st.session_state:  # 처음 한번만 초기화
    st.session_state["messages"] = []  # 대화 저장하기 위한 용도

# 사이드 바 생성
with st.sidebar:
    # 초기화 버튼 생성
    clear_btn = st.button("대화 초기화")
    if clear_btn:
        st.session_state["messages"] = []


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


def create_chain():
    # 프롬프트 템플릿 생성
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "당신은 친절한 AI 어시스턴트입니다."),
            ("user", "#Question:\n{question}"),
        ]
    )
    # GPT
    llm = ChatUpstage(temperature=0)
    # 출력 파서
    output_parser = StrOutputParser()
    # 체인 생성
    chain = prompt | llm | output_parser
    return chain


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

    # 사용자의 입력 프린트
    st.chat_message("user").write(user_input)  # with ~ 와 같은 의미
    # 체인을 생성
    chain = create_chain()
    # ai_answer = chain.invoke({"question": user_input})  # 체인 실행
    # st.chat_message("assistant").write(ai_answer)

    # stream 사용법
    response = chain.stream({"question": user_input})  # 스트림으로 출력
    with st.chat_message("assistant"):
        # 빈 공간(컨테이너)를 만들어서, 여기에 토큰을 스트리밍 출력
        container = st.empty()  # 메시지가 나올 껍데기 생성
        ai_answer = ""
        for token in response:
            print(f"token: {token}")
            # 토큰을 컨테이너에 추가
            ai_answer += token
            container.markdown(ai_answer)

    # 대화 기록 저장
    add_message("user", user_input)
    add_message("assistant", ai_answer)
    # st.session_state["messages"].append(("user", user_input))  # tuple 형식으로 저장
    # st.session_state["messages"].append(("assistant", user_input))
