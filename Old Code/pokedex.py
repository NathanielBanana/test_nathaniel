import streamlit as st
from ai import get_standard_response
from ai import get_json_response


if 'pokedex' not in st.session_state:
    st.session_state['pokedex'] = []


system_prompt = """
You are a Pokemon Collector who is writing about the stats of a Pokemon that the user chooses.
Respond in a JSON in the following format:

{
        "name" : string of pokemon name 

        "type" : type

        "height" : height

        "weight" : weight
        
        "abilities" : abilities

        "health points" : HP

        "attack" : attack

        "defense" : defense

        "speed" : speed
        
        "evolutions" : list of things that the pokemon can evolve into which includes the name and ID number
        
}
"""


st.title("The Pokedex")

pokedex = st.session_state["pokedex"]

pokemon = st.selectbox(
    "Past Pokedex Enteries",
    pokedex
)

with st.form("pokedexform"):
    new_entry = st.text_input("New Pokedex Entry")

    is_pressed = st.form_submit_button("Submit")

if is_pressed:
    user_prompt = "Generate a new pokedox entry based on this pokemon" + new_entry

    response = get_json_response(system_prompt, user_prompt)

    st.session_state['pokedex'].append(response)

    pokemon = response

    st.rerun()

if pokemon:
    st.header(pokemon['name'])

    st.write(pokemon['type'])
