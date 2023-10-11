import streamlit as st
import pandas as pd
import os
import random 
import json

st.set_page_config(page_title='TTS Shootout')
# Load the CSV data
@st.cache
def load_data():
    return pd.read_csv("data.csv")

data = load_data()

# Sidebar
pages = ["Overview"] + list(data["Service"].unique())
selected_page = st.sidebar.selectbox("Select a Page", pages)
services = ['Amazon Polly*', 'Eleven Labs*', 'Google Cloud TTS*', 'Coqui*', 'Wellsaid', 'Bark', 'Speechify', 'Facebook/mms-tts']

def render_overview_page(data):
    st.title("Overview")
    st.write("## Services Tested")
    for item in services:
        st.write(f"- {item}")
    st.write("\* View audio and  using dropdown to the left")

    st.write("## All Data")
    st.write(data)

    st.write("## Inputs Used")
    with open("inputs.json", "r") as file:
        js = json.load(file)
    st.json(js)

def render_service_page(data, service_selected):
    st.title(f"{service_selected} Details")

    # Filtering data by the selected service
    filtered_data = data[data["Service"] == service_selected]

    st.write("## Stats")
    # Display statistics for the selected service
    if service_selected == "Coqui":
        st.write(":red[Does not support CN and cannot handle multiligual synthesis.]")
        st.write("[Pricing](https://coqui.ai/pricing)")
    elif service_selected == "Eleven Labs":
        st.write("[Pricing](https://elevenlabs.io/pricing)")
    elif service_selected == "Google Cloud TTS":
        st.write("[Pricing](https://cloud.google.com/text-to-speech/pricing)")
    elif service_selected == "Amazon Polly":
        st.write("[Pricing](https://aws.amazon.com/polly/pricing/)")

    st.write('### Data')
    st.write(filtered_data)

    st.write('### Audio Samples')
    # Dropdown for voice selection
    voice_selected = st.selectbox("Select a Voice", filtered_data["Voice"].unique())
    filtered_data_voice = filtered_data[filtered_data["Voice"] == voice_selected]

    languages = filtered_data_voice["Language"].unique()
    for lang in languages:
        st.write(f"### Language: {lang}")
        lang_data = filtered_data_voice[filtered_data_voice["Language"] == lang]
        
        for index, row in lang_data.iterrows():
            row_display = ", ".join(row[1:].map(str).values)  # skip the ID for the display
            row_display = f"{row['Text']}; latency: {row['Latency (s)']} seconds"
            clicked = st.button(row_display)
            
            if clicked:
                if service_selected == "Coqui":
                    st.audio(f"https://content-intelligence-output-dev.s3.us-east-2.amazonaws.com/TTS/outputs/audio/Coqui/{row['ID']}.wav", format='audio/wav')
                elif service_selected != "Coqui": 
                    st.audio(f"https://content-intelligence-output-dev.s3.us-east-2.amazonaws.com/TTS/outputs/audio/{row['Service'].replace(' ', '+')}/{row['ID']}.mp3", format='audio/mp3')
                else:
                    st.write("Audio file not found.")

if selected_page == "Overview":
    render_overview_page(data)
else:
    render_service_page(data, selected_page)