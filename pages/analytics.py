import streamlit as st
from openai import OpenAI
import json

client = OpenAI()

st.set_page_config(page_title="Analytics", page_icon="📈")

system_prompt = """You are a Analyst who make analysis such as sentiment analysis and finding insights in the data. The data that you will be deailing a text data. Given a text data, you have to analyse.
The data is regarding the interview process of a person which contains several questions and answers. From the answer given by the user, you gotta analyse the each of the answers and provide a consiced analysis.
Try to extract the following contents from the data:
\{
    "area_of_expertise": [
        \{
            "experitise": "<expertise1>",
            "level": "Bigginer/Intermediate/Advanced"
        \},
        \{
            "experitise": "<expertise2>",
            "level": "Bigginer/Intermediate/Advanced"
        \},
        ...
    ],
    "language": "<lang>",
    "sentiment_analysis": \{
        "intent": "<write contents abt the intent of the answers>",
        "subject": "<write contents abt the subject of the answers>",
        "temporal_analysis": "<write contents about analysis of the change in sentiment over time.>",
        "emotion": "<emotion of the user>"
    \},
    "summary": "<detailed summary of the overall conversation>"
\}

## Note:
- Make sure to use the proper JSON for response."""

def get_insights():
    data = open("interview_conv.txt", 'r').read()
    response = client.chat.completions.create(
        temperature=0.8,
        response_format={ "type": "json_object" },
        model='gpt-4o',
        messages=[
            {
                'role': 'system',
                'content': system_prompt
            },
            {
                'role': 'user',
                'content': f"Here is the data you have to analyse:\n{data}"
            }
        ]
    )
    return json.loads(response.choices[0].message.content)

def convert_to_markdown(data):
    response = client.chat.completions.create(
        temperature=0.8,
        model='gpt-4o',
        messages=[
            {
                'role': 'system',
                'content': "Given a RAW JSON object, you have to convert them into nice markdown rich text."
            },
            {
                'role': 'user',
                'content': f"Here is the data you have to convert to markdown:\n{data}."
            }
        ]
    )
    return response.choices[0].message.content

with st.spinner(text="Analysing the data..."):
    json_analysis = get_insights()
    st.json(json_analysis)
    st.markdown(convert_to_markdown(json_analysis))
