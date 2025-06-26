import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_upstage import ChatUpstage
from langchain_core.output_parsers import StrOutputParser
from langchain_teddynote.prompts import load_prompt
from dotenv import load_dotenv
from langchain import hub

load_dotenv()

st.title("나만의 ChatGPT TEST")

if "messages" not in st.session_state:  # 처음 한번만 초기화
    st.session_state["messages"] = []  # 대화 저장하기 위한 용도

# 사이드 바 생성
with st.sidebar:
    # 초기화 버튼 생성
    clear_btn = st.button("대화 초기화")

    selected_prompt = st.selectbox(
        "프롬프트 선택", ("기본모드", "SNS 게시글", "요약"), index=0
    )

    # if clear_btn:
    #     st.session_state["messages"] = []


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


def create_chain(prompt_type):
    # 프롬프트 템플릿 생성
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "당신은 친절한 AI 어시스턴트입니다."),
            ("user", "#Question:\n{question}"),
        ]
    )
    if prompt_type == "SNS 게시글":
        # Windows 오류 잡은 함수
        prompt = load_prompt("prompts/sns.yaml", encoding="utf8")
    elif prompt_type == "요약":
        prompt = hub.pull("teddynote/chain-of-density-korean")

    # GPT
    llm = ChatUpstage(temperature=0)
    # 출력 파서
    output_parser = StrOutputParser()
    # 체인 생성
    chain = prompt | llm | output_parser
    return chain


print_messages()  # 이전 대화 출력

# 사용자의 입력
user_input = st.chat_input("궁금한 내용을 물어보세요.")

# 사용자 입력이 들어오면,
if user_input:
    # 사용자의 입력 프린트
    st.chat_message("user").write(user_input)  # with ~ 와 같은 의미
    # 체인을 생성
    chain = create_chain(selected_prompt)

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
