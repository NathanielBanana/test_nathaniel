import streamlit as st
import json
from openai import OpenAI
from st_chat_message import message

client = OpenAI(
    api_key = "._/-./.....---__/="
)

system_prompt = """
You are Spongebob Squarepants. You must constantly remind the user that you are Spongebob Squarepants
as if they have no idea. Otherwise, you do everything ChatGPT normally does. Exclaimer
"""

if 'convo' not in st.session_state:
    st.session_state["convo"] = [
        {"role": "system", "content": system_prompt}
    ]

for chat_message in st.session_state["convo"]:
    if chat_message["role"] == "system":
        continue
    elif chat_message["role"] == "user":
        message(chat_message["content"], is_user=True)
    else:
        message(chat_message["content"])

with st.form("input"):
    message = st.text_input("What do you want to say?")
    submitted = st.form_submit_button("Submit")
    if submitted and message != "":
        st.session_state["convo"].append({"role": "user", "content": message})

        api_call = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=st.session_state["convo"]
        )
        bot_message = api_call.choices[0].message.content

        st.session_state["convo"].append({"role": "assistant", "content": bot_message})

        st.rerun()