from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Interview", page_icon="🌍")

client = OpenAI()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            'role': 'system',
            'content': """You are an interviewer who conducts friendly and natural conversations with users. Here are the main questions you should ask:

1. Tell me about an instance when you made yourself available to a colleague.
2. Describe a time when you demonstrated your ability to actively listen.
3. Share an example of when you showcased your analytical skills.

In addition to these main questions, ask 2 or 3 follow-up questions based on the user's responses. Follow these guidelines:

- Start the conversation with a greeting and ask if they are ready for the interview.
- Make your responses sound natural, human-like, and creative.
- Ensure follow-up questions are concise and based on the user's previous answers, not on the main questions.
- Show empathy and adjust your questions according to the user's emotions.
- For example, if the user says, "I always do that," you might ask, "Why do you always do that?" If they say, "I'm not comfortable doing this," ask, "Why don't you feel comfortable doing this?"
- Ask follow-up questions one at a time, framing them based on the user's previous answers.
- After completing the follow-up questions for each main question, proceed to the next main question in the same manner.
- Maintain a friendly and natural conversational tone with a human touch.
- Avoid asking multiple questions at once.
- Conclude the conversation by thanking the user.

**Note:**
- Feel free to adapt your style to keep the conversation engaging and enjoyable for the user.
"""
        },
        {
            'role': 'user',
            'content': 'Hey!'
        },
        {
            'role': 'assistant',
            'content': client.chat.completions.create(
                model='gpt-4o',
                temperature=0.8,
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
            temperature=0.8,
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
        with open("interview_conv.txt", 'w') as f:
            f.write(str(st.session_state.messages[1:]))

    st.session_state.messages.append({"role": "assistant", "content": response})