import streamlit as st
from ai import get_standard_response


# # system_prompt = "You are a recipe generator which generates recipes for a user's food."
# # st.title("Recipe Generator")
# # st.write(
# #     "Type in a food and AI will generate a recipe for you!👌👌👌"
# # )

# # user_topic = st.text_input("Enter Food")

# # is_clicked = st.button("Submit")

# # if is_clicked:
    
# #     response = get_standard_response(system_prompt, user_topic)

# #     st.write(response)

system_prompt = "You are an age guesser based off of questions the user answers, no matter if you have almost no context, always return a guess."

st.title("Age Guesser")
st.write("Answer the following questions to allow AI to guess your age!.")

with st.form("age_form"):
    fav_cartoon = st.selectbox(
        "What is a cartoon you watched in your childhood?",
        [
            "Spongebob",
            "The Simpsons",
            "Tom and Jerry",
            "Tiny Toon Adventures",
            "Scooby-Doo",
            "Other"
        ]    
    )

    num_input = st.slider("How old are your parents?", 35, 90, 35)

    is_submitted = st.form_submit_button("Submit")

    if is_submitted:

        user_prompt = "My favorite cartoon from my childhood is " + fav_cartoon + " and my parents are " + str(num_input) + " years old."
        response = get_standard_response(system_prompt, user_prompt)

        st.write(response)