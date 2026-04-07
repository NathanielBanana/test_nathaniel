import streamlit as st
from ai import get_standard_response
from ai import get_json_response


system_prompt = """
You are a Wikipedia Page Maker for Roblox. You will first generate five different articles about "Popular Games", "History", "About the Developers", "Roblox Studio", and "Robux/Shop".

Respond in a JSON in the following format:

{
        "Name" : "the main topic of the article"
    
        "History" : "history description of the topic"

        "Characteristics" : "characteristics about the topic"
        
        "Trivia" : "fun facts"
        
}
"""

if 'articles' not in st.session_state:
    st.session_state['articles'] = [0] * 5
    user_prompt = "I want to read about the article Popular Games."

    popular_games_article = get_json_response(system_prompt, user_prompt)

    st.session_state['articles'][0] = popular_games_article

    user_prompt = "I want to read about the article Roblox Studio."

    roblox_studio_article = get_json_response(system_prompt, user_prompt)

    st.session_state['articles'][1] = roblox_studio_article

    user_prompt = "I want to read about the article Robux/Shop."

    robux_shop_article = get_json_response(system_prompt, user_prompt)

    st.session_state['articles'][2] = robux_shop_article

    user_prompt = "I want to read about the article About the Developers."

    about_the_devs_article = get_json_response(system_prompt, user_prompt)

    st.session_state['articles'][3] = about_the_devs_article

    user_prompt = "I want to read about the article History."

    history_article = get_json_response(system_prompt, user_prompt)

    st.session_state['articles'][4] = history_article


st.title("The Roblox Wiki")

current_topic = st.selectbox(
    "Choose a topic to learn about!",
    [
        "Popular Games",
        "Roblox Studio",
        "Robux/Shop",
        "About the Developers",
        "History"
    ]

)



if current_topic == "Popular Games":
    popular_games_dict = st.session_state['articles'][0]
    st.write(popular_games_dict["Name"])
    st.write("History")
    st.write(popular_games_dict["History"])
    st.write("Characteristics")
    st.write(popular_games_dict["Characteristics"])
    st.write("Trivia")
    st.write(popular_games_dict["Trivia"])

if current_topic == "Roblox Studio":
    roblox_studio_dict = st.session_state['articles'][1]
    st.write(roblox_studio_dict["Name"])
    st.write("History")
    st.write(roblox_studio_dict["History"])
    st.write("Characteristics")
    st.write(roblox_studio_dict["Characteristics"])
    st.write("Trivia")
    st.write(roblox_studio_dict["Trivia"])
if current_topic == "Robux/Shop":
    robux_shop_dict = st.session_state['articles'][2]
    st.write(robux_shop_dict["Name"])
    st.write("History")
    st.write(robux_shop_dict["History"])
    st.write("Characteristics")
    st.write(robux_shop_dict["Characteristics"])
    st.write("Trivia")
    st.write(robux_shop_dict["Trivia"])
if current_topic == "About the Developers":
    about_the_devs_dict = st.session_state['articles'][3]
    st.write(about_the_devs_dict["Name"])
    st.write("History")
    st.write(about_the_devs_dict["History"])
    st.write("Characteristics")
    st.write(about_the_devs_dict["Characteristics"])
    st.write("Trivia")
    st.write(about_the_devs_dict["Trivia"])
if current_topic == "History":
    history_dict = st.session_state['articles'][4]
    st.write(history_dict["Name"])
    st.write("History")
    st.write(history_dict["History"])
    st.write("Characteristics")
    st.write(history_dict["Characteristics"])
    st.write("Trivia")
    st.write(history_dict["Trivia"])