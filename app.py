import streamlit as st
import pandas as pd
import os
import random 
import json

st.set_page_config(page_title='TTS Shootout')
# Load the CSV data
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

data = load_data()
data['ID'] = [str(i) for i in data['ID']]


# Sidebar
pages = ["Overview"] + list(data["Service"].unique())
selected_page = st.sidebar.selectbox("Select a Page", pages)
services = ['Amazon Polly*', 'Eleven Labs*', 'Google Cloud TTS*', 'PlayHT*', 'Coqui*', 'Wellsaid', 'Bark', 'Speechify', 'Facebook/mms-tts']

def render_overview_page():
    st.title("Overview")
    st.write("Fastest: Amazon Polly")
    st.write("Most Natural Sounding: Eleven Labs")
    st.write("Current Overall Ranking (Subjective)")
    # Sample numbered list using markdown
    markdown_content = """
    1. Amazon Polly
    2. Google Cloud TTS
    3. Eleven Labs
    """

    st.markdown(markdown_content)

    st.write("## Services Tested")
    for item in services:
        st.write(f"- {item}")
    st.write("\* View audio and data using dropdown to the left")

    st.write("## All Data")
    csv = data.to_csv(index=False)
    csv_bytes = csv.encode()

    st.download_button(
        label="Download CSV",
        data=csv_bytes,
        file_name="data.csv",
        mime="text/csv"
    )

    st.write(data)

    st.write("## Inputs Used")
    with open("inputs.json", "r") as file:
        js = json.load(file)
    st.json(js)

def render_service_page(service_selected):
    st.title(f"{service_selected} Details")

    # Filtering data by the selected service
    filtered_data = data[data["Service"] == service_selected]

    languages = filtered_data["Language"].unique()

    st.write("## Stats")

    # Display statistics for the selected service
    if service_selected == "Coqui":
        st.write(":red[Does not support CN and cannot handle multiligual synthesis. + 250 Character Limit (async)]")
        st.write("[Pricing](https://coqui.ai/pricing)")
    elif service_selected == "PlayHT":
        st.write(":red[Only supports english voices as default (can add custom voices) + 200 Character Limit (async)]")
        st.write("[Pricing](https://play.ht/pricing/)")
    elif service_selected == "Eleven Labs":
        st.write("[Pricing](https://elevenlabs.io/pricing)")
    elif service_selected == "Google Cloud TTS":
        st.write("[Pricing](https://cloud.google.com/text-to-speech/pricing)")
    elif service_selected == "Amazon Polly":
        st.write("[Pricing](https://aws.amazon.com/polly/pricing/)")

    st.write("### Latency")
    # Average latency for the entire service
    avg_latency = filtered_data["Latency (s)"].mean()
    st.write(f"Average Latency for {service_selected} OVERALL: {avg_latency:.2f} seconds")
    latency_per_lang = filtered_data.groupby("Language")["Latency (s)"].mean()
    for lang, latency in latency_per_lang.items():
        st.write(f"{lang}: {latency:.2f} seconds")
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
            row_display = f"{row['Text']}; latency: {row['Latency (s)']} seconds"
            clicked = st.button(row_display, key=f"{row['ID']}-{index}")
            
            if clicked:
                if service_selected == "Coqui":
                    st.audio(f"https://content-intelligence-output-dev.s3.us-east-2.amazonaws.com/TTS/outputs/audio/Coqui/{row['ID']}.wav", format='audio/wav')
                elif service_selected == "PlayHT":
                    st.audio(f"https://content-intelligence-output-dev.s3.us-east-2.amazonaws.com/TTS/outputs/audio/PlayHT/{row['ID']}.wav", format='audio/wav')
                elif service_selected != "Coqui": 
                    st.audio(f"https://content-intelligence-output-dev.s3.us-east-2.amazonaws.com/TTS/outputs/audio/{row['Service'].replace(' ', '+')}/{row['ID']}.mp3", format='audio/mp3')
                else:
                    st.write("Audio file not found.")

if selected_page == "Overview":
    render_overview_page()
else:
    render_service_page(selected_page)