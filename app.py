from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.title("FollowUp'er")

client = OpenAI()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            'role': 'system',
            'content': "you'll be give a question and the answer for that question by user.  you have to try to make a other new questions based on the topic the they are discussing. Generate a single further questions that continues in the flow of the Q&A. Try this for full conversation. Again, please generate only one follow up question for each conversation. Also make sure that you are returning **only the question**, do not include any other text like 'sure here is the question' or 'further question is below'. Don't include any other contents, just question."
        }
    ]

for message in st.session_state.messages:
    if message['role'] != 'system':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})