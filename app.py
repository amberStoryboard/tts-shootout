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
pages = ["Overview"] + list(data["Service"].unique()) + ["ValleX"] + ["Other"]
selected_page = st.sidebar.selectbox("Select a Page", pages)
services = ['Amazon Polly*', 'Eleven Labs*', 'Google Cloud TTS*', 'PlayHT*', 'Coqui*', 'ValleX*', 'Wellsaid', 'Bark', 'Speechify', 'Facebook/mms-tts']

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
    if service_selected == "ValleX":
        st.write("[Storyboard Valle-X Clone on Hugging Face](https://huggingface.co/spaces/storyboard-fm/VALL-E-X)")
        st.write("[Valle-X on Hugging Face](https://huggingface.co/spaces/Plachta/VALL-E-X)")

        st.write('### Audio Samples')
        # Dropdown for voice selection
        st.write('These samples are all created using 2 different audio prompts of JP. Prompt is generated with less than 15 seconds of audio.')


        st.write("### Audio Prompt = JP1")
        st.write("##### preset=acou_2")
        st.audio(f"https://content-intelligence-output-dev.s3.us-east-2.amazonaws.com/TTS/outputs/audio/ValleX/english_OG_prompt/acou2.wav", format='audio/wav')
        st.write("#####  preset=neutral")
        st.audio(f"https://content-intelligence-output-dev.s3.us-east-2.amazonaws.com/TTS/outputs/audio/ValleX/english_OG_prompt/neutral.wav", format='audio/wav')
        st.write("#####  preset=Angry")
        st.audio(f"https://content-intelligence-output-dev.s3.us-east-2.amazonaws.com/TTS/outputs/audio/ValleX/english_OG_prompt/angry.wav", format='audio/wav')
        st.write("##### Long Text")
        st.audio(f"https://content-intelligence-output-dev.s3.us-east-2.amazonaws.com/TTS/outputs/audio/ValleX/english_OG_prompt/long_text.wav", format='audio/wav')
       
        st.write("### Audio Prompt = JP2")
        st.write("##### preset=acou_2")
        st.audio(f"https://content-intelligence-output-dev.s3.us-east-2.amazonaws.com/TTS/outputs/audio/ValleX/english_JP_2/acou_2.wav", format='audio/wav')
        st.write("#####  preset=neutral")
        st.audio(f"https://content-intelligence-output-dev.s3.us-east-2.amazonaws.com/TTS/outputs/audio/ValleX/english_JP_2/neutral.wav", format='audio/wav')
        st.write("#####  preset=Angry")
        st.audio(f"https://content-intelligence-output-dev.s3.us-east-2.amazonaws.com/TTS/outputs/audio/ValleX/english_JP_2/angry.wav", format='audio/wav')
        st.write("##### Long Text")
        st.audio(f"https://content-intelligence-output-dev.s3.us-east-2.amazonaws.com/TTS/outputs/audio/ValleX/english_JP_2/long_text.wav", format='audio/wav')
       

    else: 
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

def render_other_page():
    st.title('Other')
    st.write("# Bark")
    st.write(":red[These were generated using the HuggingFace model directly. Note the varied quality, voices, and sometimes word fragments.]")
    st.audio('https://content-intelligence-output-dev.s3.us-east-2.amazonaws.com/TTS/outputs/audio/Bark/2749614339936119285.wav', format='audio/wav')
    st.audio('https://content-intelligence-output-dev.s3.us-east-2.amazonaws.com/TTS/outputs/audio/Bark/6004853653590609627.wav', format='audio/wav')
    st.audio('https://content-intelligence-output-dev.s3.us-east-2.amazonaws.com/TTS/outputs/audio/Bark/3835215678970929748.mp3', format='audio/mp3')
    st.audio('https://content-intelligence-output-dev.s3.us-east-2.amazonaws.com/TTS/outputs/audio/Bark/4815884020050789919.mp3', format='audio/mp3')
    st.audio('https://content-intelligence-output-dev.s3.us-east-2.amazonaws.com/TTS/outputs/audio/Bark/6154106207730663268.mp3', format='audio/mp3')
    st.audio('https://content-intelligence-output-dev.s3.us-east-2.amazonaws.com/TTS/outputs/audio/Bark/6154106207730663268.wav', format='audio/wav')
    st.audio('https://content-intelligence-output-dev.s3.us-east-2.amazonaws.com/TTS/outputs/audio/Bark/6506613826820044038.wav', format='audio/wav')
    st.audio('https://content-intelligence-output-dev.s3.us-east-2.amazonaws.com/TTS/outputs/audio/Bark/8455871188536666885.wav', format='audio/wav')

    st.write("# Facebook MMS-TTS")
    st.write(":red[These were also generated using the HuggingFace model directly.]")
    st.audio('https://content-intelligence-output-dev.s3.us-east-2.amazonaws.com/TTS/outputs/audio/Facebook/MMS-TTS-ENG/1597225242755826339.mp3', format='audio/mp3')
    st.audio('https://content-intelligence-output-dev.s3.us-east-2.amazonaws.com/TTS/outputs/audio/Facebook/MMS-TTS-ENG/5603296773089309171.mp3', format='audio/mp3')
    st.audio('https://content-intelligence-output-dev.s3.us-east-2.amazonaws.com/TTS/outputs/audio/Facebook/MMS-TTS-ENG/8867981403509797570.mp3', format='audio/mp3')


    st.write("# Speechify and Wellsaid")
    st.write('Both Speechify and Wellsaid do not have public apis or exportable audio but audio is able to be generated using their studio interface on their website.')
    st.write('[Speechify](https://studio.speechify.com/dashboard)')
    st.write('- Seems optimized for documents and books')
    st.write('- :red[Only available on web and iOS]')
    st.write('[Wellsaid](https://studio.wellsaidlabs.com/dashboard/projects/personal)')
    st.write('- Use case seems to be better suited for scripts and promotional content')
if selected_page == "Overview":
    render_overview_page()
elif selected_page == "Other":
    render_other_page()
else:
    render_service_page(selected_page)