import streamlit as st
from ai import get_standard_response

system_prompt = "You are a translator and you will translate the sentance given from the input language to the output language."
st.title("The AI Translator")
st.write("Enter your input language and output language:")

with st.form("translator_form"):
    input_language = st.selectbox(
        "Choose your input language",
        [
            "Arabic",
            "Bengali",
            "Cantonese",
            "Dutch",
            "English",
            "French",
            "German",
            "Greek",
            "Hebrew",
            "Hindi",
            "Indonesian",
            "Italian",
            "Japanese",
            "Javanese",
            "Korean",
            "Mandarin Chinese",
            "Marathi",
            "Persian",
            "Polish",
            "Portuguese",
            "Punjabi",
            "Russian",
            "Spanish",
            "Swahili",
            "Tamil",
            "Telugu",
            "Thai",
            "Turkish",
            "Ukrainian",
            "Urdu",
            "Vietnamese",
            "Zulu"
        ]
    )
    output_language = st.selectbox(
        "Choose your output language",
        [
            "Arabic",
            "Bengali",
            "Cantonese",
            "Dutch",
            "English",
            "French",
            "German",
            "Greek",
            "Hebrew",
            "Hindi",
            "Indonesian",
            "Italian",
            "Japanese",
            "Javanese",
            "Korean",
            "Mandarin Chinese",
            "Marathi",
            "Persian",
            "Polish",
            "Portuguese",
            "Punjabi",
            "Russian",
            "Spanish",
            "Swahili",
            "Tamil",
            "Telugu",
            "Thai",
            "Turkish",
            "Ukrainian",
            "Urdu",
            "Vietnamese",
            "Zulu"
        ]
    )
    translating_sentance = st.text_input("Enter the Sentance you would like to translate.")
    
    is_submitted = st.form_submit_button("Submit")

    if is_submitted:

        user_prompt = ("My input language is " + input_language + ", my output language is " + output_language + ". Translate the sentance " + translating_sentance + ".")

        response = get_standard_response(system_prompt, user_prompt)
        
        st.write(response)

