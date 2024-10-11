import streamlit as st
from PIL import Image
from langchain.chat_models import ChatOpenAI
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)

def main():
    llm = ChatOpenAI(temperature=0)
    st.set_page_config(
        page_title="TRIP PLANNER",
        page_icon="🧳"
    )
    st.header("trip planner")
    # チャット履歴の初期化
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a trip planner.You should think great trip plan.")
        ]
    st.text("・このサイトは、皆さんのバカンスを最高なものにするために開発されました。")
    st.text("・まずは目的地.グルメ.観光地などの気になる条件から入力してみましょう！")

    # Sidebarの選択肢を定義する
    options = ["MAP", "MEMO", "EXIT"]
    choice = st.sidebar.selectbox("Select an option", options)
    # Mainコンテンツの表示を変える
    if choice == "MAP":
        st.write("You selected MAP")
    elif choice == "MEMO":
        st.write("You selected MEMO")
    else:
        st.write("You selected EXIT")

    # ユーザーの入力を監視
    if user_input := st.chat_input("聞きたいことを入力してね！"):
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("ChatGPT is typing ..."):
            response = llm(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))

    # チャット履歴の表示
    messages = st.session_state.get('messages', [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message('assistant'):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message('user'):
                st.markdown(message.content)
        else:  # isinstance(message, SystemMessage):
            st.write(f"System message: {message.content}")

    image = Image.open('back.png')

    st.image(image, caption='In Liechtenstein',use_column_width=True)
    
if __name__ == '__main__':
    main()