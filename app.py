import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import os

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key = "AIzaSyCGkdMEeGp0vTajEcAWFcJqqF0Dh8Ym-4c")

# prompt = """you are youtube video summarizer. you will be taking the transcript text and summarizing the entire video and
# providing the important summary in points and also be succinct in your response. The transcript text will be appended here : """

def extract_transcript_details(Youtube_video_url):
    try:
        video_id = Youtube_video_url.split("=")[1]
        video_id = video_id.split("&")[0]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
        # print(transcript)
        return  transcript
    except Exception as e:
        raise e

# def generate_gemini_content(transcript_text, prompt):
#     model= genai.GenerativeModel("gemini-pro")
#     response = model.generate_content(prompt+transcript_text)
#     return response.text


st.title("Youtube Transcript to Detailed Notes Converter")

Youtube_video_url = st.text_input("Enter Youtube Video Link :")

if Youtube_video_url:
    video_id = Youtube_video_url.split("=")[1]
    video_id = video_id.split("&")[0]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width = True)



option = ["AI", "News", "Sports", "Movie", "Music or Song", "Comedy", "mythology", "Political", "Programing", "Others" ]
st.header("Select the Video Topic from below list")
selection = st.selectbox("Select Video Topic", option)


prompt = f"""you are youtube video summarizer. you will be taking the transcript text and summarizing the entire video and 
providing the important summary in points and also be succinct in your response, This youtube video transcript is related to "{selection}".
 The transcript text will be appended here : """

# print(prompt)
def generate_gemini_content(transcript_text, prompt):
    model= genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcript_text)
    return response.text


if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(Youtube_video_url)
    
    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Notes :")
        st.write(summary)
    