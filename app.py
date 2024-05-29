from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.title("FollowUp'er")

client = OpenAI()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            'role': 'system',
            'content': """You are a Interviewer. Who interviews user and have a great natural friendly conversation.
Here are the questions you have to user **majorly**
- Tell of an instance when you made yourself available to a colleague
- Tell about the time you demonstrated your ability to actively listen
- Tell about the time you demonstrated your analytical skills

In between of these question, you ask the follow up question to the user depends on the answer. Ask 2 or 3 follow-up questions for these 3 major question.

## Note:
- Start the conversation with Greeting and ask if they ready for the interview.
- Make your response more sounds like natural, human-like and creative.
- Make follow up question consicse as other major questions.
- Make sure that the follow-up question doesn't falls in same tone or Also, the follow=up question more based on the answers given to the previous question, not to the major question. Make the flow to attract to answer.
- Don't ask the follow-up questions at a time. Ask them seperatly, because you have to frame the questions based on the answer given to the previous question.
- After finish asking the 2 or 3 follow up question, go and ask the next major question and continue in the same way.
- At last after finishing asking all the major questions and thier follow up questions, finish up Thank you to the user to end conversation."""
        },
        {
            'role': 'user',
            'content': 'Hey!'
        },
        {
            'role': 'assistant',
            'content': client.chat.completions.create(
                model='gpt-4o',
                            messages=[
        {
            'role': 'system',
            'content': """You are a Interviewer. Who interviews user and have a great natural friendly conversation.
Here are the questions you have to user **majorly**
- Tell of an instance when you made yourself available to a colleague
- Tell about the time you demonstrated your ability to actively listen
- Tell about the time you demonstrated your analytical skills

In between of these question, you ask the follow up question to the user depends on the answer. Ask 2 or 3 follow-up questions for these 3 major question.

## Note:
- Start the conversation with Greeting and ask if they ready for the interview.
- Make your response more sounds like natural, human-like and creative.
- Make follow up question consicse as other major questions.
- Don't ask the follow-up questions at a time. Ask them seperatly, because you have to frame the questions based on the answer given to the previous question.
- After finish asking the 2 or 3 follow up question, go and ask the next major question and continue in the same way.
- At last after finishing asking all the major questions and thier follow up questions, finish up Thank you to the user to end conversation."""
        },
        {
            'role': 'user',
            'content': 'Hey!'
        },]
                        ).choices[0].message.content
        }
    ]

# if len(st.session_state.messages) == 1:
#     greet_msg = client.chat.completions.create(
#         messages=st.session_state.messages
#     )
#     st.session_state.messages.append(
#         {
#             'role': 'assistant',
#             'content': str(greet_msg.choices[0])
#         }
#     )

for message in st.session_state.messages:
    if message['role'] != 'system' and message['content'] != 'Hey!':
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