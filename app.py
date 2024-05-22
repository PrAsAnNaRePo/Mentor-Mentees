from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.title("FollowUp'er")

client = OpenAI()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo-0125"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            'role': 'system',
            'content': """You are a AI chatbot.
Here are the questions you have to user **majorly**
- Tell of an instance when you made yourself available to a colleague
- Tell about the time you demonstrated your ability to actively listen
- Tell about the time you demonstrated your analytical skills

In between of these question, you ask the follow up question to the user depends on the answer. Ask 2 or 3 follow-up questions for these 3 major question.

## Note:
- Don't include any other random text/content, just write question.
- Make follow up question consicse as other major questions.
- Don't ask the follow-up questions at a time. Ask them seperatly, because you have to frame the questions based on the answer given to the above question.
- After finish asking the 2 or 3 follow up question, go and ask the next major question and continue in the same way.
- At last after finishing asking all the major questions and thier follow up questions, finish up Thank you to the user to end conversation."""
        },
        {
            'role': 'assistant',
            'content': 'Tell of an instance when you made yourself available to a colleague'
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